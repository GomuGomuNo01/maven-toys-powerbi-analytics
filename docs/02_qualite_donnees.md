# 2. Données et audit de qualité

> Avant de construire un rapport, on vérifie que les données sont fiables.
> Un indicateur calculé sur des données mal comprises est plus dangereux qu'une absence d'indicateur.

Script utilisé : [`analysis/audit_donnees.py`](../analysis/audit_donnees.py)

## Source

Jeu de données **Mexico Toy Sales** de [Maven Analytics](https://mavenanalytics.io/data-playground) (données fictives, libres d'utilisation à des fins pédagogiques). Fichiers dans [`data/raw/`](../data/raw).

| Fichier | Lignes | Grain (que représente une ligne ?) | Rôle dans le modèle |
|---|---:|---|---|
| `sales.csv` | 829 262 | Un produit vendu dans un magasin à une date | Table de faits |
| `inventory.csv` | 1 593 | Le stock d'un produit dans un magasin, à une date unique | Table de faits (photo) |
| `products.csv` | 35 | Un produit | Dimension |
| `stores.csv` | 50 | Un magasin | Dimension |
| `calendar.csv` | 638 | Un jour, du 01/01/2022 au 30/09/2023 | Dimension de dates |

## Résultats de l'audit

### Ce qui est sain

- Aucune valeur manquante, aucun doublon.
- Aucune vente rattachée à un magasin ou un produit inconnu (intégrité référentielle respectée).
- Calendrier continu, sans jour manquant (condition nécessaire aux calculs N-1).

### Ce qui doit être corrigé ou pris en compte

| Constat | Risque si on l'ignore | Traitement |
|---|---|---|
| Prix stockés en texte (`"$15.99 "`) | Calculs impossibles | Suppression de `$` et des espaces, conversion en nombre (Power Query) |
| Formats américains (point décimal, dates `1/31/2022`) | Sur un Windows français : prix multipliés par 100 ou dates en erreur | Conversion de type avec la culture `en-US` |
| Faute de frappe : `Cuidad de Mexico` | Ville mal nommée dans tous les visuels | Remplacement par `Ciudad de Mexico` |
| Année 2023 partielle (janvier à septembre) | Fausse impression de chute d'activité au 4e trimestre | Comparaisons à période égale uniquement |
| Stock = photo à une date, sans historique | Impossible d'analyser l'évolution du stock | Stock non relié au calendrier, date de référence affichée |
| 41 couples magasin x produit vendus mais absents de l'inventaire | Risque de rupture non détecté | Documenté comme limite |
| `Sale_ID` unique sur 829 262 lignes, inutilisé | Modèle plus lourd (colonne peu compressible) | Colonne supprimée au chargement |
| Prix et coûts unitaires fixes (pas d'historique de prix) | Mauvaise interprétation de la baisse de marge | Toute variation du taux de marge est un **effet mix** |
| 11 produits lancés en cours de période | Évolutions en % trompeuses (base N-1 faible ou nulle) | Analyse en valeur (écart de marge) plutôt qu'en % |

## Écarts constatés avec l'ancienne version du projet

L'audit a aussi permis de corriger l'existant :

- Le fichier `.pbix` du dépôt était **vide** (2 octets) : le rapport a été entièrement reconstruit.
- Le graphique « par mois » cumulait 2022 et 2023 sur les mêmes mois : la « chute » d'octobre à décembre venait uniquement de l'absence de données 2023 sur ces mois.
- La conclusion « le centre-ville génère 2,5 fois plus de CA » était un effet de taille : 29 magasins sur 50 y sont situés. **Par magasin, ce sont les aéroports qui performent le mieux.**
- La recommandation « augmenter le stock d'électronique » n'était pas étayée : la couverture de l'électronique (16 jours) est dans la moyenne et son meilleur produit ne connaît aucune rupture. Le recul vient de la **demande**.
