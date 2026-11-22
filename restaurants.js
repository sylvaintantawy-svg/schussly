// Restaurants par station : [nom, type ('p' = sur les pistes, midi · 'v' = village, soir), prix moyen d'un repas par personne en CHF (plat + boisson), source du prix ('carte' = carte officielle, sinon estimation), note]
// Sources des noms : sites des stations et offices du tourisme (myswitzerland.com, alpesvaudoises.ch, fribourg.ch, ovronnaz.ch, leukerbad.ch, belalp.ch, loetschental.ch, legrandbornand.com, prazdelys-sommand.com, montagnes-du-jura.fr, hautesavoiemontblanc-tourisme.com, jura-tourism.com). Relevé nov. 2026.
window.RESTOS = {
  glacier3000: [['Restaurant Botta', 'p', 55, '', 'Scex Rouge 2971 m · cuisine soignée, réserver'], ['Restaurant Le 3', 'p', 30, '', 'Scex Rouge · ramen, burgers, curries'], ['Refuge de l’Espace', 'p', 30, '', 'Refuge sur le domaine'], ['Restaurant du Col du Pillon', 'v', 40, '', 'Au départ du téléphérique']],
  saasfee: [['Drehrestaurant Allalin', 'p', 35, '', 'Plus haut restaurant tournant du monde, 3500 m · 9 h–15 h 30'], ['Bergrestaurant Spielboden', 'p', 40, '', '2450 m, vue sur les 4000'], ['Fee Chäller', 'v', 40, '', 'Valaisan typique · fondue, rösti'], ['Schäferstube', 'v', 50, '', 'Rustique · spécialités d’agneau'], ['Del Ponte', 'v', 38, '', 'Pizzeria']],
  grimentz: [['Restaurant de Bendolla', 'p', 30, '', 'Self et service à table · 9 h–16 h'], ['Restaurant de Sorebois', 'p', 30, '', 'Côté Zinal · 9 h–16 h 30']],
  stluc: [['Restaurant de Tignousa', 'p', 30, '', 'Self et service à table'], ['Cabane Illhorn', 'p', 35, '', 'Côté Chandolin'], ['Gîte du Prilet', 'p', 38, '', 'Fondue']],
  vercorin: [['Restaurant du Crêt-du-Midi', 'p', 28, '', 'Plats autour de 20–30'], ['L’Étable de Sigeroulaz', 'p', 32, '', 'Sur les pistes'], ['La Brentaz', 'v', 42, '', 'Au village']],
  anzere: [['Pas de Maimbré', 'p', 30, '', '2362 m · service ou self'], ['Le Tsalan', 'p', 30, '', '1951 m'], ['Le Grenier de Zalan', 'v', 40, '', 'Au village']],
  arolla: [['Buvette 3000', 'p', 25, '', 'Sur le domaine'], ['La Cambuse', 'v', 40, '', 'Fondue']],
  evolene: [['La Paix & La Grange', 'v', 45, '', 'Au cœur d’Evolène'], ['La Taverne Evolénarde', 'v', 40, '', 'Cuisine valaisanne'], ['Pension d’Evolène', 'v', 40, '', 'Simple et familial']],
  nax: [['Restaurant Tsébetta', 'p', 28, '', 'Espace Mont-Noble'], ['Restaurant de la Dzorniva', 'p', 28, '', 'Sur le domaine'], ['Le Vieux Chalet', 'v', 42, '', 'Nax village']],
  gstaad: [['Bergrestaurant Saanerslochgrat', 'p', 30, '', 'Self-service'], ['Rinderberg-Spitz', 'p', 35, '', '2011 m'], ['Berghotel Hornberg', 'p', 40, '', 'Terrasse au soleil'], ['Hotel Restaurant Hornfluh', 'p', 38, '', 'Sur les pistes']],
  eggli: [['Bergrestaurant Eggli', 'p', 35, '', 'Arrivée de la télécabine'], ['La Videmanette', 'p', 35, '', '2200 m · plats au fromage, menu du jour']],
  villars: [['Bretaye 1808', 'p', 32, '', 'Col de Bretaye'], ['Rocco Cantina Italiana', 'p', 35, '', 'Roc d’Orsay'], ['Restaurant du Col de Soud', 'p', 30, '', 'Sur les pistes'], ['Les Mazots', 'p', 32, '', 'Les Diablerets, Meilleret'], ['L’Étable', 'v', 45, '', 'Gryon']],
  leysin: [['Le Kuklos', 'p', 40, '', 'Restaurant tournant, Berneuse 2048 m · fromage, rösti'], ['Click & Go 2048', 'p', 20, '', 'Self au rez du Kuklos, repas légers']],
  mosses: [['Self La Drosera', 'p', 22, '', 'Pied des pistes des Mosses'], ['Buvette de l’Arsat', 'p', 30, '', 'Viande sur l’ardoise, fondue, raclette'], ['Buvette des Eraisis', 'p', 20, '', 'La Lécherette · self']],
  laberra: [['Chalet de la Berra', 'p', 30, '', '1640 m · produits frais de saison'], ['Gîte d’Allières', 'p', 35, '', '1485 m · fondue, jambon · ouvert le soir']],
  moleson: [['Plan-Francey', 'p', 26, 'carte', '1520 m · plats 21.50–32 CHF (carte officielle)'], ['Restaurant Le Sommet', 'p', 35, '', '2002 m · fondue avec vue']],
  charmey: [['Le Vounetz (Dents-Vertes)', 'p', 32, '', 'Arrivée télécabine · terroir fribourgeois'], ['Auberge de Tissiniva', 'p', 35, '', '20 min du sommet'], ['Le Vigousse', 'v', 40, '', 'Au pied des pistes']],
  jaun: [['Buvette Gastlosen', 'p', 15, '', 'Arrivée du télésiège · petite restauration'], ['Hotel-Restaurant Wasserfall', 'v', 45, '', 'Produits régionaux'], ['Hotel zur Hochmatt', 'v', 42, '', 'Jaun village']],
  belalp: [['Hotel Belalp', 'p', 42, '', 'Aletschbord 2137 m · vue glacier d’Aletsch'], ['Restaurant Sparrhorn', 'p', 32, '', 'Spécialités valaisannes'], ['Restaurant Aletschhorn', 'p', 30, '', 'Pizzeria familiale'], ['Hamilton Lodge', 'v', 45, '', 'Blatten · fondue, burgers']],
  lauchernalp: [['Panoramarestaurant Zudili', 'p', 28, '', 'Arrivée du téléphérique · self'], ['Berghaus Lauchernalp', 'p', 32, '', '2150 m · valaisan et pizzas'], ['Restaurant Bärgsunna', 'p', 30, '', 'Au-dessus de la gare']],
  leukerbad: [['Rinderhütte', 'p', 30, '', '2350 m · self, buffet salades'], ['Restaurant Briand', 'p', 35, '', 'Terrasse plein sud · Torrentalp'], ['Alpengruss', 'p', 35, '', 'Pistes boisées']],
  ovronnaz: [['Restaurant de Jorasse', 'p', 28, '', '1940 m · self et salle servie · cuisine chaude 11 h 30–15 h'], ['Buvette de Petit Pré', 'p', 18, '', '2225 m · snacks, grillades'], ['La Promenade', 'v', 42, '', 'Ovronnaz village'], ['Hostellerie de l’Ardève', 'v', 45, '', 'Terrasse']],
  meiringen: [['Bergrestaurant Käserstatt', 'p', 32, '', '1840 m · servi, grande terrasse'], ['Bergrestaurant Mägisalp', 'p', 30, '', '1710 m · fondue ou raclette le soir'], ['Alpen Tower', 'p', 35, '', 'Planplatten 2250 m']],
  jsl: [['Bistrot du Chalet des Tuffes', 'p', 20, 'carte', 'Croûte jurassienne 18 € (carte officielle)']],
  hirmentaz: [['Les Pivottes', 'p', 30, '', 'Spécialités fromagères'], ['Les Skieurs', 'p', 28, '', 'Pied des pistes · crêpes, savoyard'], ['Auberge de Miribel', 'p', 35, '', 'Habère-Lullin · braserade, feu de cheminée']],
  grandbornand: [['La Taverne du Chinaillon', 'p', 32, '', 'Ancienne ferme, terrasse panoramique · 9 h 30–17 h'], ['Le Repaire', 'p', 32, '', 'Restaurant d’alpage, la Culaz'], ['Le Châtillon', 'p', 30, '', 'Plateau du Rosay'], ['Le Chamois', 'v', 38, '', 'Chinaillon, pied des pistes'], ['La Bournerie', 'v', 50, '', 'Chinaillon · menu soigné']],
  prazdelys: [['Le Zilda', 'p', 30, '', 'Entre Sommand et Praz de Lys · vue Mont-Blanc'], ['La Grande Ourse', 'p', 22, '', 'Self le midi, savoyard le soir'], ['Auberge du Lys Blanc', 'p', 30, '', 'Matouille, fondue, raclette']],
  metabief: [['Le Comptoir du Morond', 'p', 18, '', 'Sommet du Morond · snack'], ['Oh Rond-Point des pistes', 'p', 25, '', 'Front de neige · ambiance après-ski'], ['Le Chamois', 'v', 35, '', 'Pied des pistes · plats copieux'], ['La Taverne Comtoise', 'v', 30, '', 'Cuisine comtoise']]
};
// Adresses plutôt gastronomiques (cuisine soignée, prix élevés) — d'après les descriptions des offices du tourisme
window.RESTO_GASTRO = ['Restaurant Botta', 'Schäferstube', 'Hotel Belalp', 'La Bournerie', 'La Paix & La Grange', 'Le Kuklos', 'Bergrestaurant Spielboden'];
// Option végétarienne confirmée sur la carte officielle
window.RESTO_VEGE = ['Plan-Francey'];
