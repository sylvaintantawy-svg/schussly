# Schussly — où skier ce week-end

Une web app mobile (HTML + JS, sans serveur) qui classe les stations Magic Pass pour les jours choisis et prépare le week-end : programme, plan B, liens Booking et Airbnb.

## Écrans

- **Recherche** : point de départ, jours, format (journée / 1 nuit / 2 nuits) et route maximum.
- **Classement** : un onglet par jour. Chaque station a son score sur 100 et sa météo, avec Booking et Airbnb accessibles directement depuis la carte.
- **Fiche station** : météo heure par heure et détail du score, heure de départ, hébergement, liens de vérification (météo officielle, webcams, ouvertures). On peut aussi corriger soi-même l'état ouvert / fermé.
- **Mon week-end** : programme jour par jour, hébergement, plan B en un tap et partage.

## Mettre en ligne (météo et route en direct)

1. Va sur https://app.netlify.com/drop
2. Glisse ce dossier dans la page.
3. Ouvre l'adresse sur ton téléphone, puis « Ajouter à l'écran d'accueil ».

Pour tester sur ton ordinateur : lance `python3 -m http.server` dans le dossier, puis ouvre http://localhost:8000.

Une fois en ligne, l'app va chercher la météo (Open-Meteo, avec les modèles MeteoSwiss) et la route (OSRM). Si ces services ne répondent pas, elle utilise `snapshot.js` (prévisions relevées le 22.11.2026).

## Données live (2 fois par jour)

`update.py` relève sur magicpass.ch les remontées et les km de pistes ouverts de chaque station (`live.js`). Il récupère aussi la météo au sommet (Open-Meteo, ou met.no en secours) et la route depuis Lausanne, avec durée et km (OSRM) : c'est `snapshot.js`.

- Version claude.ai : une tâche planifiée Claude lance le script à 7 h 47 et 11 h 47, puis republie l'app.
- Version hébergée sur GitHub : `.github/workflows/live.yml` fait la même chose à 7 h et 12 h.
- À la main : `python3 update.py .`

Les données live ne concernent que le jour même. Pour les jours suivants, l'app s'appuie sur le calendrier d'ouverture des stations.

## Fichiers

- `index.html` : l'app (les quatre écrans, la navigation par adresse `#/…` et le calcul du score).
- `stations.js` : les 28 stations, avec altitudes, dates d'ouverture et liens officiels. À mettre à jour à chaque saison.
- `snapshot.js` : météo et route actualisées (secours si les services en direct ne répondent pas).
- `live.js` : remontées et pistes ouvertes du jour (magicpass.ch).
- `restaurants.js` : restaurants recommandés par station (midi sur les pistes, soir au village) et prix moyen d'un repas.
- `update.py` : script d'actualisation.

## Avant de commercialiser

- Open-Meteo n'est gratuit que pour un usage non commercial : prends la licence, ou passe directement à MeteoSwiss Open Data.
- OSRM public est un service de démonstration : utilise OpenRouteService (clé gratuite) ou Google Routes.
- Remplace les liens Booking par tes liens d'affiliation.
