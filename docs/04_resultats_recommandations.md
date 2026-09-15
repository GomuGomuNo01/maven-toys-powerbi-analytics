# 4. Résultats et recommandations

> Période analysée : janvier 2022 à septembre 2023. Les évolutions comparent **janvier-septembre 2023** à **janvier-septembre 2022**.
> Tous les chiffres sont reproductibles avec [`analysis/audit_donnees.py`](../analysis/audit_donnees.py) et contrôlés dans Power BI.

## Synthèse pour la direction

> **La croissance 2023 est forte (+31 % de CA) mais deux fois moins rentable qu'elle n'en a l'air (+16 % de marge brute).**
> Elle repose sur des produits à faible marge, pendant que le produit le plus rentable de l'enseigne s'effondre.
> Les ruptures de stock coûtent environ 29 000 $ de CA par mois, alors que 49 000 $ de stock dorment en rayon.

| Indicateur | Janv.-sept. 2022 | Janv.-sept. 2023 | Évolution |
|---|---:|---:|---:|
| Chiffre d'affaires | 5 320 116 $ | 6 962 074 $ | **+30,9 %** |
| Marge brute | 1 572 037 $ | 1 824 242 $ | **+16,0 %** |
| Taux de marge | 29,5 % | 26,2 % | **-3,3 pts** |
| Unités vendues | 384 415 | 541 073 | +40,8 % |
| CA moyen par vente | 17,91 $ | 17,05 $ | -4,8 % |

## Enseignements

### 1. La croissance dilue la rentabilité

Le CA progresse deux fois plus vite que la marge brute. Les prix et coûts unitaires étant fixes dans les données, la baisse de 3,3 points du taux de marge est **entièrement un effet mix** :

- **-1,6 pt** vient du poids croissant des catégories peu rentables ;
- **-1,8 pt** vient du poids croissant des produits peu rentables à l'intérieur de chaque catégorie.

Le taux de marge baisse dans 4 catégories sur 5 (seule Sports & plein air progresse).

### 2. Deux dynamiques opposées expliquent la variation de marge

| Catégorie | Évol. CA | Écart de marge brute | Taux de marge 2023 |
|---|---:|---:|---:|
| Arts créatifs | +251,9 % | **+335 745 $** | 26,7 % |
| Sports & plein air | +25,1 % | +65 719 $ | 23,8 % |
| Jeux | +20,3 % | +33 805 $ | 29,6 % |
| Jouets | +14,2 % | +27 196 $ | 20,4 % |
| Électronique | -27,8 % | **-210 260 $** | 40,6 % |

- **Arts créatifs (moteur de croissance)** : le CA est multiplié par 3,5, porté par **Magic Sand** (lancé en juillet 2022, +865 000 $ de CA mais seulement 12,5 % de marge), **Barrel O' Slime** et **Etch A Sketch** (lancé en novembre 2022).
- **Électronique (frein)** : **Colorbuds** perd 264 000 $ de marge brute à lui seul. Ses volumes trimestriels ont chuté de 60 % en 18 mois (23 580 unités au T1 2022, 9 296 au T3 2023), alors qu'il reste vendu dans les 50 magasins et ne connaît aucune rupture. **Le problème est la demande, pas la disponibilité.**

### 3. Une forte dépendance à quelques produits

- **Colorbuds** : 10,8 % du CA mais **20,8 % de la marge brute** totale (taux de marge de 53 %). Son déclin est le principal risque pour la rentabilité.
- **Lego Bricks** : premier produit en CA (16,5 %), mais taux de marge de 12,5 % seulement.

### 4. Les aéroports sont les magasins les plus productifs

Janvier-septembre 2023 :

| Type d'emplacement | Magasins | Part du CA | CA moyen par magasin | Évol. CA vs N-1 |
|---|---:|---:|---:|---:|
| Aéroport | 3 | 9,2 % | **213 156 $** | **+37,5 %** |
| Centre-ville | 29 | 57,3 % | 137 670 $ | +33,4 % |
| Quartier résidentiel | 6 | 11,2 % | 129 653 $ | +24,8 % |
| Zone commerciale | 12 | 22,3 % | 129 356 $ | +25,2 % |

Le centre-ville domine en volume uniquement parce qu'il concentre 29 magasins. **Par magasin, un aéroport génère 1,5 fois plus de CA** qu'un magasin de centre-ville et croît le plus vite. Le constat est identique sur toute la période (430 000 $ par magasin d'aéroport contre 283 000 $).

47 magasins sur 50 progressent. Trois reculent : **Monterrey 1** (-16,6 %), **Guadalajara 4** (-4,2 %) et **Aguascalientes 1** (-2,6 %).

### 5. Une activité concentrée en fin de semaine et en décembre

- En 2023, le samedi génère en moyenne **35 764 $ par jour** et le vendredi 34 682 $, contre 19 172 $ le lundi (x 1,9).
- Décembre 2022 a pesé **1,5 fois un mois moyen** : le 4e trimestre 2023 sera décisif.

### 6. Les stocks sont mal répartis : ruptures d'un côté, capital immobilisé de l'autre

Photo au 30/09/2023, demande estimée sur les 90 derniers jours :

| Statut | Références | Part | Impact |
|---|---:|---:|---|
| Rupture | 77 | 4,8 % | **969 $ de CA potentiel perdu par jour (29 069 $ sur 30 jours, soit 4,2 % du CA journalier récent)** |
| Critique (< 7 jours) | 289 | 18,1 % | Ruptures probables à court terme |
| Normal (7 à 90 jours) | 1 018 | 63,9 % | |
| Surstock (> 90 jours) | 116 | 7,3 % | 32 590 $ immobilisés |
| Stock dormant (aucune vente) | 93 | 5,8 % | 16 657 $ immobilisés |

- **Playfoam**, lancé le 17/08/2023, est déjà **en rupture dans 13 magasins et critique dans 14 autres** (27 magasins sur 49) : le lancement a été sous-dimensionné.
- Ruptures les plus coûteuses : **Dino Egg** (170 $/jour), **Playfoam** (148 $/jour), **Mini Ping Pong Set** (110 $/jour). **Hot Wheels 5-Pack** manque dans 12 magasins.
- Stock à rentabiliser : **Dinosaur Figures** (surstock dans 11 magasins), **PlayDoh Playset** et **Supersoaker Water Gun** (sans vente dans 13 magasins chacun).
- 16,4 % de la valeur du stock est immobilisée (49 246 $ sur 300 210 $).

## Recommandations

| Priorité | Recommandation | Destinataire | Indicateur de suivi |
|---|---|---|---|
| 1 | **Réapprovisionner en urgence** les 77 références en rupture, en commençant par Dino Egg, Playfoam et Mini Ping Pong Set, avant le pic de décembre | Supply chain | Nb ruptures, CA potentiel perdu |
| 2 | **Revoir l'allocation des nouveaux produits** : dimensionner les stocks de lancement sur les ventes réelles des 2 premières semaines (cas Playfoam) | Achats | Couverture des produits lancés |
| 3 | **Diagnostiquer le déclin de Colorbuds** (concurrence, prix, obsolescence) et préparer un produit de remplacement à forte marge | Direction commerciale | Marge brute Électronique |
| 4 | **Protéger la marge des produits moteurs** : tester une hausse de prix modérée ou des offres groupées sur Magic Sand et Lego Bricks (fort volume, marge faible) | Direction commerciale | Taux de marge par produit |
| 5 | **Écouler le stock immobilisé** (promotions, transferts entre magasins) : 49 000 $ de trésorerie à libérer | Supply chain | Valeur stock immobilisé |
| 6 | **Étudier l'ouverture de points de vente en aéroport**, format le plus productif | Direction générale | CA moyen par magasin |
| 7 | **Analyser les 3 magasins en recul**, en priorité Monterrey 1 (-16,6 %) | Direction des opérations | Évol. CA par magasin |
| 8 | **Renforcer les effectifs et les livraisons le vendredi et le samedi** | Direction des opérations | CA moyen par jour |

## Limites

- **Données fictives** : les conclusions illustrent une démarche, elles ne décrivent pas une entreprise réelle.
- **Pas d'historique de prix, de promotions ni de coûts** : impossible de distinguer un effet prix d'un effet volume, ou de mesurer l'impact d'une promotion.
- **Stock = photo unique** : impossible de savoir depuis quand une référence est en rupture ni de calculer une rotation de stock sur la période.
- **Demande sous-estimée pour les ruptures** : une référence en rupture depuis plusieurs semaines a peu vendu sur 90 jours, donc son CA perdu est probablement sous-estimé.
- **41 couples magasin x produit vendus mais absents de l'inventaire** : leur risque de rupture n'est pas mesuré.
- **Marge brute uniquement** : pas de loyers, salaires ou frais logistiques, donc pas de rentabilité nette par magasin.
- **Seuils (7 et 90 jours) fixés par hypothèse** : à valider avec la supply chain selon les délais réels de réapprovisionnement.
- **Évolutions en % trompeuses pour les produits lancés en 2022** (ex. Magic Sand : +24 825 %, sa base de janvier-septembre 2022 étant quasi nulle) : l'écart de marge en valeur est l'indicateur de référence.

## Pistes d'amélioration

- **Prévision des ventes** du 4e trimestre 2023 (saisonnalité 2022) pour dimensionner les commandes.
- **Page d'analyse du lancement de produits** (courbe des ventes depuis la première vente).
- **Segmentation ABC** des produits (20 % des produits qui font 80 % de la marge).
- **Publication sur Power BI Service** avec actualisation planifiée et sécurité par ligne (RLS) : chaque directeur de magasin ne voit que son magasin.
- **Intégration continue** : valider automatiquement le modèle TMDL et le rapport PBIR à chaque commit (GitHub Actions), et comparer les KPI au script Python de référence.
- **Alimentation depuis une base SQL** plutôt que des CSV, pour se rapprocher d'un environnement d'entreprise.
