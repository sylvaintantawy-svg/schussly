// Garde l'app et le dernier calcul hors ligne (en voiture, au col).
const C = 'schussly-v2';
const SHELL = ['./', './index.html', './stations.js', './snapshot.js', './live.js', './restaurants.js', './manifest.json', './icon.svg'];
self.addEventListener('install', (e) => e.waitUntil(caches.open(C).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener('activate', (e) => e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== C).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then((r) => { const copy = r.clone(); if (r.ok) caches.open(C).then((c) => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request)));
});
