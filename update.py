#!/usr/bin/env python3
"""Schussly — actualisation des données (à lancer 2 fois par jour, 7 h et 12 h).

Produit, dans le dossier de l'app :
  live.js      état live des stations (remontées et km de pistes ouverts) relevé sur magicpass.ch
  snapshot.js  météo au sommet sur 8 jours (Open-Meteo, secours met.no) + route depuis Lausanne (OSRM)

Usage : python3 update.py [dossier_de_l_app]
"""
import json, math, os, re, html, subprocess, sys, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

APP = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("Europe/Zurich")
UA = "Schussly/1.0 (+https://schussly.ch)"
ORIGIN = {"name": "Lausanne", "lat": 46.5168, "lon": 6.6291}
# Points de départ précalculés (l'app hors ligne s'en sert quand on change de ville)
ORIGINS = [ORIGIN] + [
    {"name": n, "lat": la, "lon": lo} for n, la, lo in [
        ("Genève", 46.2102, 6.1424), ("Sion", 46.2273, 7.3591), ("Fribourg", 46.8032, 7.1513), ("Neuchâtel", 46.9965, 6.9358),
        ("Berne", 46.9490, 7.4392), ("Montreux", 46.4353, 6.9104), ("Vevey", 46.4627, 6.8432), ("Morges", 46.5098, 6.4981),
        ("Nyon", 46.3833, 6.2397), ("Yverdon-les-Bains", 46.7810, 6.6406), ("Renens", 46.5370, 6.5880), ("Martigny", 46.1028, 7.0727),
        ("Bulle", 46.6181, 7.0569), ("Monthey", 46.2550, 6.9540), ("Aigle", 46.3188, 6.9690), ("Zurich", 47.3779, 8.5403)]]

# Correspondance stations de l'app -> fiches magicpass.ch (plusieurs fiches = additionnées)
MP = {
    "glacier3000": ["glacier-3000-85"], "saasfee": ["saas-fee-600"], "grimentz": ["grimentz-zinal-18"],
    "stluc": ["st-luc--chandolin-33"], "vercorin": ["vercorin-35"], "anzere": ["anzere-4"],
    "arolla": ["espace-dent-blanche-arolla-118"], "evolene": ["espace-dent-blanche-evolene-88"],
    "nax": ["nax--mt-noble-29"], "gstaad": ["bergbahnen-gstaad-4447"], "eggli": ["bergbahnen-gstaad-4447"],
    "villars": ["villars-gryon-37", "les-diablerets-22"], "leysin": ["leysin-26"],
    "mosses": ["les-mosses-la-lecherette-24"], "laberra": ["la-berra-20"], "moleson": ["moleson-28"],
    "charmey": ["charmey-14"], "jaun": ["jaun-19"], "belalp": ["blatten-belalp-4445"],
    "lauchernalp": ["lauchernalp-2771"], "leukerbad": ["leukerbad-torrent-gemmi-602"], "ovronnaz": ["ovronnaz-30"],
    "meiringen": ["meiringen-hasliberg-4451"], "jsl": ["jura-sur-leman-transfrontalier-3608"],
    "hirmentaz": ["hirmentaz-3590", "les-haberes-3607"], "grandbornand": ["le-grand-bornand-4448"],
    "prazdelys": ["praz-de-lys-sommand-4454"], "metabief": ["metabief-1794"],
}


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def load_js(path, var):
    """Lit window.VAR = {...} d'un fichier .js via node."""
    if not os.path.exists(path):
        return None
    code = f"global.window={{}};require({json.dumps(path)});process.stdout.write(JSON.stringify(window.{var}||null))"
    return json.loads(subprocess.check_output(["node", "-e", code]))


# ---------------------------------------------------------------- live (magicpass.ch)
def magicpass_live():
    page = get("https://www.magicpass.ch/fr/stations")
    out = {}
    starts = list(re.finditer(r'<a href="/fr/stations/([a-z0-9-]+)" aria-label="([^"]+)"[^>]*class="rounded-aio-block', page))
    for k, m in enumerate(starts):
        blk = page[m.start(): starts[k + 1].start() if k + 1 < len(starts) else m.start() + 8000]
        lifts = re.search(r'ico-cabin[^>]*>\s*<span[^>]*>\s*(\d+)\s*/\s*(\d+)', blk)
        km = re.search(r'skieur[^>]*>\s*<span[^>]*>\s*([\d.]+)\s*/\s*([\d.]+)\s*<small>km', blk)
        text = re.sub(r"<[^>]+>", " ", blk)
        out[m.group(1)] = {
            "liftsOpen": int(lifts.group(1)) if lifts else None, "liftsTotal": int(lifts.group(2)) if lifts else None,
            "kmOpen": float(km.group(1)) if km else None, "kmTotal": float(km.group(2)) if km else None,
            "open": bool(re.search(r"\bOuvert\b", text)),
        }
    if len(out) < 50:
        raise RuntimeError(f"magicpass.ch : seulement {len(out)} stations lues, structure changée ?")
    res = {}
    for sid, slugs in MP.items():
        rows = [out[s] for s in slugs if s in out]
        if not rows:
            continue
        add = lambda k: sum(r[k] for r in rows if r[k] is not None) if any(r[k] is not None for r in rows) else None
        res[sid] = {"liftsOpen": add("liftsOpen"), "liftsTotal": add("liftsTotal"),
                    "kmOpen": add("kmOpen"), "kmTotal": add("kmTotal"), "open": any(r["open"] for r in rows),
                    "shared": len(set(slugs)) == 1 and sum(1 for v in MP.values() if v == slugs) > 1}
    return res


# ---------------------------------------------------------------- météo
def compact_day(times, H, d):
    """Agrège 9 h–16 h d'un jour au format [soleil min, rafale max, neige jour, hauteur 9 h, fraîche 72 h, heures]."""
    idx = [i for i, t in enumerate(times) if t.startswith(d) and 9 <= int(t[11:13]) <= 16]
    if len(idx) < 8:
        return None
    s0 = idx[0]
    sun = sum(H["sun"][i] or 0 for i in idx)
    gust = max(H["gust"][i] or 0 for i in idx)
    snow = sum(H["snow"][i] or 0 for i in idx)
    depth = H["depth"][s0] if H["depth"][s0] is not None else 0
    fresh = sum(H["snow"][i] or 0 for i in range(max(0, s0 - 72), s0))
    hrs = []
    for h in (9, 11, 13, 15):
        i = idx[h - 9]
        hrs.append([f"{h:02d}", round(H["temp"][i] or 0), round(H["sun"][i] or 0), round(H["gust"][i] or 0), round(H["snow"][i] or 0, 1)])
    return [round(sun), round(gust), round(snow, 1), round(depth, 2), round(fresh, 1), hrs]


def openmeteo(S, dates):
    P = [s.get("wx") or [s["lat"], s["lon"]] for s in S]
    url = ("https://api.open-meteo.com/v1/forecast?latitude=" + ",".join(str(p[0]) for p in P) +
           "&longitude=" + ",".join(str(p[1]) for p in P) + "&elevation=" + ",".join(str(s["elev"]) for s in S) +
           "&hourly=temperature_2m,sunshine_duration,wind_gusts_10m,snowfall,snow_depth&timezone=Europe%2FZurich&past_days=3&forecast_days=8")
    j = json.loads(get(url, 60))
    if not isinstance(j, list):
        raise RuntimeError(j.get("reason", "Open-Meteo indisponible"))
    out = []
    for x in j:
        h = x["hourly"]
        H = {"temp": h["temperature_2m"], "sun": [v / 60 if v is not None else 0 for v in h["sunshine_duration"]],
             "gust": h["wind_gusts_10m"], "snow": h["snowfall"], "depth": h["snow_depth"]}
        out.append({d: v for d in dates if (v := compact_day(h["time"], H, d))})
    return out


def metno(S, dates, prev):
    """Secours : met.no (gratuit, CC BY 4.0). Soleil estimé par la couverture nuageuse, neige = précipitations sous 1 °C."""
    out = []
    for k, s in enumerate(S):
        lat, lon = s.get("wx") or [s["lat"], s["lon"]]
        j = json.loads(get(f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat:.4f}&lon={lon:.4f}&altitude={s['elev']}"))
        ts = j["properties"]["timeseries"]
        pts = [(datetime.fromisoformat(t["time"].replace("Z", "+00:00")).astimezone(TZ), t["data"]) for t in ts]
        def at(dt):
            return min(pts, key=lambda p: abs((p[0] - dt).total_seconds()))[1]
        prev_s = prev[k] if prev and k < len(prev) else {}
        last_depth = 0.0
        if prev_s:
            last_depth = prev_s[sorted(prev_s)[-1]][3]
        res = {}
        for d in dates:
            hrs_all = []
            for h in range(9, 17):
                dt = datetime.fromisoformat(f"{d}T{h:02d}:00").replace(tzinfo=TZ)
                if dt < pts[0][0] - timedelta(hours=1) or dt > pts[-1][0] + timedelta(hours=3):
                    break
                data = at(dt)
                det = data["instant"]["details"]
                temp = det.get("air_temperature", 0)
                cloud = det.get("cloud_area_fraction", 100)
                gust = max(det.get("wind_speed_of_gust", 0), det.get("wind_speed", 0) * 1.6) * 3.6
                nxt = data.get("next_1_hours") or data.get("next_6_hours") or {}
                pr = (nxt.get("details") or {}).get("precipitation_amount", 0)
                if "next_6_hours" in data and "next_1_hours" not in data:
                    pr = pr / 6
                snow = pr if temp < 1 else 0
                hrs_all.append([h, temp, 60 * (1 - cloud / 100), gust, snow])
            if len(hrs_all) < 8:
                continue
            if d in prev_s:
                depth, fresh = prev_s[d][3], prev_s[d][4]
            else:
                depth, fresh = last_depth, 0
            res[d] = [round(sum(x[2] for x in hrs_all)), round(max(x[3] for x in hrs_all)), round(sum(x[4] for x in hrs_all), 1),
                      depth, fresh, [[f"{x[0]:02d}", round(x[1]), round(x[2]), round(x[3]), round(x[4], 1)] for x in hrs_all if x[0] in (9, 11, 13, 15)]]
        out.append(res)
    return out


# ---------------------------------------------------------------- route
def osrm(S):
    n = len(ORIGINS)
    coords = ";".join([f"{o['lon']},{o['lat']}" for o in ORIGINS] + [f"{s['lon']},{s['lat']}" for s in S])
    src = ";".join(str(i) for i in range(n))
    dst = ";".join(str(i) for i in range(n, n + len(S)))
    j = json.loads(get(f"https://router.project-osrm.org/table/v1/driving/{coords}?sources={src}&destinations={dst}&annotations=duration,distance"))
    if j.get("code") != "Ok":
        raise RuntimeError("OSRM indisponible")
    routes = {}
    for k, o in enumerate(ORIGINS):
        routes[o["name"]] = {"lat": o["lat"], "lon": o["lon"],
                             "drive": [round(x / 60 * 1.2) if x is not None else None for x in j["durations"][k]],
                             "dist": [round(x / 1000) if x is not None else None for x in j["distances"][k]]}
    return routes


def main():
    S = load_js(os.path.join(APP, "stations.js"), "STATIONS")
    prev = load_js(os.path.join(APP, "snapshot.js"), "SNAPSHOT") or {}
    now = datetime.now(TZ)
    stamp = now.strftime("%d.%m.%Y à %H:%M")
    dates = [(now.date() + timedelta(days=i)).isoformat() for i in range(8)]
    report = []

    # météo
    days = None
    for attempt in range(3):
        try:
            days, wsrc = openmeteo(S, dates), "Open-Meteo"
            break
        except Exception as e:
            report.append(f"Open-Meteo (essai {attempt + 1}) : {e}")
            import time; time.sleep(30)
    if days is None:
        try:
            days, wsrc = metno(S, dates, prev.get("days")), "met.no"
        except Exception as e2:
            report.append(f"met.no : {e2}")
            days, wsrc = prev.get("days"), prev.get("weatherSource", "précédent")
            stamp = prev.get("generatedAt", stamp)
    # route
    try:
        routes = osrm(S)
    except Exception as e:
        report.append(f"OSRM : {e}")
        routes = prev.get("routes") or {ORIGIN["name"]: {"lat": ORIGIN["lat"], "lon": ORIGIN["lon"], "drive": prev.get("drive"), "dist": prev.get("dist")}}
    base = routes.get(ORIGIN["name"], {})

    snap = {"generatedAt": stamp, "weatherSource": wsrc, "origin": ORIGIN, "drive": base.get("drive"), "dist": base.get("dist"), "routes": routes, "days": days}
    with open(os.path.join(APP, "snapshot.js"), "w") as f:
        f.write("// Généré par update.py — météo au sommet (" + wsrc + "), route depuis Lausanne (OSRM, +20 %).\n")
        f.write("window.SNAPSHOT = " + json.dumps(snap, ensure_ascii=False, separators=(",", ":")) + ";\n")

    # live
    try:
        live = {"fetchedAt": now.strftime("%Y-%m-%dT%H:%M"), "date": now.date().isoformat(), "source": "magicpass.ch", "stations": magicpass_live()}
        with open(os.path.join(APP, "live.js"), "w") as f:
            f.write("// Généré par update.py — état des stations relevé sur https://www.magicpass.ch/fr/stations\n")
            f.write("window.LIVE = " + json.dumps(live, ensure_ascii=False, separators=(",", ":")) + ";\n")
        n_open = sum(1 for v in live["stations"].values() if v["open"] and (v["kmOpen"] or 0) > 0)
        report.append(f"live : {len(live['stations'])} stations lues, {n_open} avec des pistes ouvertes")
    except Exception as e:
        report.append(f"magicpass.ch : {e}")

    report.insert(0, f"météo : {wsrc}, {sum(1 for d in (days or []) if d)} stations, relevé {stamp}")
    print("\n".join(report))


if __name__ == "__main__":
    main()
