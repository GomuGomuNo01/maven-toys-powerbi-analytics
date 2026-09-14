# 1. Cadrage du besoin

> Première étape de tout projet de Data Analyst : comprendre **qui** a besoin de **quoi**, et **pour quelle décision**.
> Sans cadrage, on produit des graphiques ; avec un cadrage, on produit des réponses.

## Contexte métier (mise en situation)

**Maven Toys** est une enseigne fictive de 50 magasins de jouets au Mexique (5 catégories, 35 produits).

Nous sommes début **octobre 2023**. Le comité de direction prépare deux échéances :

- **Les achats du 4e trimestre** : décembre est le mois le plus important de l'année (en 2022, il a pesé 1,5 fois un mois moyen).
- **Le budget 2024** : arbitrer entre les catégories, les produits et les magasins.

La croissance 2023 semble excellente, mais le contrôle de gestion signale que **la marge ne suit pas**. En parallèle, les directeurs de magasin remontent des **ruptures de stock** sur certains produits.

Le Data Analyst de l'équipe Performance commerciale est sollicité pour construire un **outil de pilotage** et une **analyse** qui éclairent ces décisions.

## Parties prenantes

| Interlocuteur | Besoin | Décision éclairée |
|---|---|---|
| Direction générale | Vision synthétique de la performance | Validation du budget 2024 |
| Direction commerciale | Rentabilité par catégorie et produit | Assortiment, mise en avant, prix |
| Direction des opérations | Performance des magasins | Priorités d'investissement, suivi des magasins en difficulté |
| Supply chain / achats | Ruptures et surstocks | Réapprovisionnement, commandes du 4e trimestre |

## Problématique

> **La croissance de Maven Toys en 2023 est-elle rentable et durable, et où agir en priorité (produits, magasins, stocks) avant la fin d'année ?**

## Questions d'analyse

| # | Question | Page du rapport |
|---|---|---|
| Q1 | Comment évoluent le CA, la marge et les volumes en 2023 par rapport à 2022, **à période égale** ? | Synthèse |
| Q2 | Quelles catégories et quels produits expliquent l'évolution de la marge ? | Synthèse, Produits |
| Q3 | Quels types d'emplacement et quels magasins performent le mieux **à taille comparable** ? | Magasins |
| Q4 | Quelles références sont en rupture ou à risque, combien cela coûte, et où le capital est-il immobilisé ? | Stocks |

## Indicateurs clés (KPI)

| KPI | Définition | Pourquoi cet indicateur |
|---|---|---|
| Chiffre d'affaires (CA) | Unités vendues x prix unitaire | Mesure l'activité |
| Marge brute | CA moins coût d'achat des produits vendus | Mesure ce que l'activité rapporte réellement |
| Taux de marge | Marge brute / CA | Mesure la qualité de la croissance |
| Évolution vs N-1 | (Période N - même période N-1) / N-1 | Neutralise la saisonnalité |
| CA moyen par magasin | CA / nombre de magasins actifs | Compare des groupes de tailles différentes |
| Couverture de stock (jours) | Stock / ventes moyennes journalières des 90 derniers jours | Anticipe l'épuisement du stock |
| CA potentiel perdu | Demande journalière des références en rupture x prix | Chiffre le coût des ruptures |
| Stock immobilisé | Valeur au coût des références en surstock ou sans vente | Chiffre le capital mal utilisé |

## Règles de gestion retenues

- **Comparaison à période égale** : les données s'arrêtent au 30/09/2023. On compare donc janvier à septembre 2023 avec janvier à septembre 2022, jamais une année partielle avec une année complète.
- **Seuils de stock** : rupture = stock nul avec une demande existante ; critique = moins de 7 jours de couverture ; surstock = plus de 90 jours ; dormant = stock sans aucune vente sur 90 jours.
- **Montants en dollars US**, comme dans la source.

## Livrables

1. Un rapport Power BI de 4 pages (synthèse, produits, magasins, stocks).
2. Un script Python d'audit qualité et de contrôle des chiffres.
3. Une synthèse des résultats et des recommandations ([04_resultats_recommandations.md](04_resultats_recommandations.md)).
