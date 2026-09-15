"""
Audit de qualité des données et calcul des valeurs de référence.

Rôle dans le projet
-------------------
1. Vérifier la qualité des fichiers bruts AVANT de construire le rapport Power BI
   (valeurs manquantes, doublons, clés orphelines, formats à corriger).
2. Calculer des indicateurs de référence de façon indépendante de Power BI.
   Ces valeurs servent à contrôler (réconcilier) les mesures DAX : si Power BI
   affiche le même chiffre que ce script, la mesure est considérée comme juste.

Exécution (depuis la racine du dépôt) :
    pip install -r analysis/requirements.txt
    python analysis/audit_donnees.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

DOSSIER_DONNEES = Path(__file__).resolve().parent.parent / "data" / "raw"

# Mêmes traductions que dans Power Query, pour comparer les chiffres à l'identique
CATEGORIES_FR = {
    "Art & Crafts": "Arts créatifs",
    "Electronics": "Électronique",
    "Games": "Jeux",
    "Sports & Outdoors": "Sports & plein air",
    "Toys": "Jouets",
}
EMPLACEMENTS_FR = {
    "Downtown": "Centre-ville",
    "Commercial": "Zone commerciale",
    "Residential": "Quartier résidentiel",
    "Airport": "Aéroport",
}
FENETRE_JOURS = 90  # période utilisée pour estimer la demande récente


def titre(texte: str) -> None:
    print(f"\n{'=' * 80}\n{texte}\n{'=' * 80}")


def charger_donnees():
    ventes = pd.read_csv(DOSSIER_DONNEES / "sales.csv", parse_dates=["Date"])
    produits = pd.read_csv(DOSSIER_DONNEES / "products.csv")
    magasins = pd.read_csv(DOSSIER_DONNEES / "stores.csv")
    stock = pd.read_csv(DOSSIER_DONNEES / "inventory.csv")
    calendrier = pd.read_csv(DOSSIER_DONNEES / "calendar.csv")
    return ventes, produits, magasins, stock, calendrier


def audit_qualite(ventes, produits, magasins, stock, calendrier) -> None:
    titre("1. AUDIT DE QUALITÉ DES DONNÉES")
    tables = {
        "sales": ventes,
        "products": produits,
        "stores": magasins,
        "inventory": stock,
        "calendar": calendrier,
    }
    for nom, table in tables.items():
        print(
            f"{nom:<10} {len(table):>8} lignes | "
            f"valeurs manquantes : {int(table.isna().sum().sum())} | "
            f"doublons : {int(table.duplicated().sum())}"
        )

    print("\nFormats à corriger :")
    print(f"  Prix au format texte (ex. '{produits.loc[0, 'Product_Price']}') -> conversion en nombre")
    print(f"  Dates du calendrier au format américain (ex. '{calendrier.loc[0, 'Date']}') -> culture en-US")
    villes_mal_orthographiees = magasins.loc[magasins["Store_City"].str.contains("Cuidad"), "Store_City"].unique()
    print(f"  Faute de frappe dans les villes : {list(villes_mal_orthographiees)} -> 'Ciudad de Mexico'")

    print("\nIntégrité référentielle :")
    print(f"  Ventes sans magasin connu : {(~ventes['Store_ID'].isin(magasins['Store_ID'])).sum()}")
    print(f"  Ventes sans produit connu : {(~ventes['Product_ID'].isin(produits['Product_ID'])).sum()}")
    print(f"  Identifiant de vente unique : {ventes['Sale_ID'].is_unique}")

    print("\nPérimètre :")
    print(f"  Période des ventes : {ventes['Date'].min():%d/%m/%Y} au {ventes['Date'].max():%d/%m/%Y}")
    print("  -> 2023 est une année partielle (janvier à septembre) : comparer à période égale")
    print(f"  Unités par vente : min {ventes['Units'].min()}, médiane {ventes['Units'].median():.0f}, max {ventes['Units'].max()}")

    couples_vendus = ventes[["Store_ID", "Product_ID"]].drop_duplicates()
    absents = couples_vendus.merge(stock, how="left", on=["Store_ID", "Product_ID"])["Stock_On_Hand"].isna().sum()
    print(f"\nStock (photo à une date unique, sans historique) :")
    print(f"  Couples magasin x produit en stock : {len(stock)}")
    print(f"  Couples avec stock à 0 : {(stock['Stock_On_Hand'] == 0).sum()}")
    print(f"  Couples déjà vendus mais absents de l'inventaire : {absents}")


def preparer(ventes, produits, magasins):
    """Reproduit les transformations Power Query."""
    produits = produits.copy()
    for colonne in ["Product_Cost", "Product_Price"]:
        produits[colonne] = produits[colonne].str.replace("$", "", regex=False).str.strip().astype(float)
    produits["Categorie"] = produits["Product_Category"].map(CATEGORIES_FR)

    magasins = magasins.copy()
    magasins["Store_City"] = magasins["Store_City"].replace("Cuidad de Mexico", "Ciudad de Mexico")
    magasins["Emplacement"] = magasins["Store_Location"].map(EMPLACEMENTS_FR)

    detail = ventes.merge(produits, on="Product_ID").merge(magasins, on="Store_ID")
    detail["CA"] = detail["Units"] * detail["Product_Price"]
    detail["Marge"] = detail["Units"] * (detail["Product_Price"] - detail["Product_Cost"])
    detail["Annee"] = detail["Date"].dt.year
    detail["Mois"] = detail["Date"].dt.month
    return detail, produits, magasins


def agreger(table: pd.DataFrame, par) -> pd.DataFrame:
    resultat = table.groupby(par).agg(
        CA=("CA", "sum"),
        Marge=("Marge", "sum"),
        Unites=("Units", "sum"),
        Ventes=("Sale_ID", "count"),
    )
    resultat["Taux_marge"] = resultat["Marge"] / resultat["CA"]
    return resultat


def comparer_periodes(detail: pd.DataFrame, par) -> pd.DataFrame:
    """Compare janvier-septembre 2023 à janvier-septembre 2022."""
    periode = detail[detail["Mois"] <= 9]
    table = agreger(periode, [par, "Annee"]).unstack("Annee")
    return pd.DataFrame({
        "CA 2022": table[("CA", 2022)],
        "CA 2023": table[("CA", 2023)],
        "Évol. CA %": table[("CA", 2023)] / table[("CA", 2022)] - 1,
        "Marge 2022": table[("Marge", 2022)],
        "Marge 2023": table[("Marge", 2023)],
        "Écart marge": table[("Marge", 2023)] - table[("Marge", 2022)],
        "Taux 2022": table[("Taux_marge", 2022)],
        "Taux 2023": table[("Taux_marge", 2023)],
    })


def indicateurs_ventes(detail: pd.DataFrame) -> None:
    titre("2. INDICATEURS DE RÉFÉRENCE : VENTES ET RENTABILITÉ")
    print("Total sur toute la période (janv. 2022 à sept. 2023) :")
    print(agreger(detail.assign(Total="Total"), "Total").round(3).to_string())

    print("\nComparaison à période égale (janvier à septembre) :")
    periode = agreger(detail[detail["Mois"] <= 9], "Annee")
    periode["CA_moyen_vente"] = periode["CA"] / periode["Ventes"]
    print(periode.round(3).to_string())
    evolution = periode.loc[2023] / periode.loc[2022] - 1
    print(f"\n  Évol. CA : {evolution['CA']:+.1%} | Évol. marge brute : {evolution['Marge']:+.1%} | "
          f"Évol. unités : {evolution['Unites']:+.1%}")
    print(f"  Écart taux de marge : {(periode.loc[2023, 'Taux_marge'] - periode.loc[2022, 'Taux_marge']) * 100:+.1f} pts")

    print("\nPar catégorie (janv.-sept.) :")
    print(comparer_periodes(detail, "Categorie").round(3).to_string())

    # Les prix et coûts unitaires sont fixes dans les données : la baisse du taux
    # de marge ne peut venir que du mix (poids des produits dans le CA).
    periode_cat = detail[detail["Mois"] <= 9]
    cat = agreger(periode_cat, ["Annee", "Categorie"])
    poids_2023 = cat.loc[2023, "CA"] / cat.loc[2023, "CA"].sum()
    taux_2022 = cat.loc[2022, "Taux_marge"]
    taux_theorique = (poids_2023 * taux_2022).sum()
    taux_reel_2022 = cat.loc[2022, "Marge"].sum() / cat.loc[2022, "CA"].sum()
    taux_reel_2023 = cat.loc[2023, "Marge"].sum() / cat.loc[2023, "CA"].sum()
    print("\nDécomposition de l'écart de taux de marge :")
    print(f"  Effet mix entre catégories      : {(taux_theorique - taux_reel_2022) * 100:+.1f} pts")
    print(f"  Effet mix au sein des catégories : {(taux_reel_2023 - taux_theorique) * 100:+.1f} pts")

    print("\nProduits : plus fortes variations de marge brute (janv.-sept.) :")
    produits = comparer_periodes(detail, "Product_Name").fillna(0).sort_values("Écart marge")
    colonnes = ["CA 2022", "CA 2023", "Écart marge", "Taux 2023"]
    print(pd.concat([produits.head(5), produits.tail(5)])[colonnes].round(3).to_string())

    print("\nProduits lancés en cours de période (première vente) :")
    premieres_ventes = detail.groupby("Product_Name")["Date"].min()
    print(premieres_ventes[premieres_ventes > "2022-01-31"].sort_values().dt.strftime("%d/%m/%Y").to_string())

    print("\nContribution des produits à la marge brute totale (top 5) :")
    contribution = agreger(detail, "Product_Name").sort_values("Marge", ascending=False)
    contribution["Part marge"] = contribution["Marge"] / contribution["Marge"].sum()
    contribution["Part CA"] = contribution["CA"] / contribution["CA"].sum()
    print(contribution.head(5)[["CA", "Marge", "Taux_marge", "Part CA", "Part marge"]].round(3).to_string())

    print("\nPar type d'emplacement :")
    emplacement = agreger(detail, "Emplacement")
    emplacement["Nb_magasins"] = detail.groupby("Emplacement")["Store_ID"].nunique()
    emplacement["CA_par_magasin"] = emplacement["CA"] / emplacement["Nb_magasins"]
    emplacement["Part CA"] = emplacement["CA"] / emplacement["CA"].sum()
    evol = comparer_periodes(detail, "Emplacement")["Évol. CA %"]
    emplacement["Évol. CA % (janv.-sept.)"] = evol
    print(emplacement.sort_values("CA_par_magasin", ascending=False).round(3).to_string())

    # Vue par défaut du rapport Power BI : janvier-septembre 2023
    print("\nPar type d'emplacement (janv.-sept. 2023, vue par défaut du rapport) :")
    annee = detail[detail["Annee"] == 2023]
    emplacement_2023 = agreger(annee, "Emplacement")
    emplacement_2023["CA_par_magasin"] = emplacement_2023["CA"] / annee.groupby("Emplacement")["Store_ID"].nunique()
    emplacement_2023["Part CA"] = emplacement_2023["CA"] / emplacement_2023["CA"].sum()
    print(emplacement_2023.sort_values("CA_par_magasin", ascending=False)[["CA", "CA_par_magasin", "Part CA"]].round(3).to_string())

    print("\nVilles (top 5 CA) :")
    villes = agreger(detail, "Store_City").sort_values("CA", ascending=False)
    villes["Part CA"] = villes["CA"] / villes["CA"].sum()
    print(villes.head(5)[["CA", "Marge", "Part CA"]].round(3).to_string())

    print("\nMagasins en recul (janv.-sept. 2023 vs 2022) :")
    magasins = comparer_periodes(detail, "Store_Name")
    print(magasins[magasins["Évol. CA %"] < 0][["CA 2022", "CA 2023", "Évol. CA %"]].round(3).to_string())
    print(f"  Magasins en croissance : {(magasins['Évol. CA %'] >= 0).sum()} sur {len(magasins)}")

    print("\nSaisonnalité : CA mensuel")
    mensuel = detail.pivot_table(index="Mois", columns="Annee", values="CA", aggfunc="sum")
    print(mensuel.round(0).to_string())

    print("\nCA moyen par jour selon le jour de la semaine (toute la période | janv.-sept. 2023) :")
    noms_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    resultats = {}
    for libelle, table in [("Toute la période", detail), ("Janv.-sept. 2023", detail[detail["Annee"] == 2023])]:
        jours = table.groupby(table["Date"].dt.dayofweek).agg(CA=("CA", "sum"), Jours=("Date", "nunique"))
        resultats[libelle] = (jours["CA"] / jours["Jours"]).set_axis(noms_jours)
    print(pd.DataFrame(resultats).round(0).to_string())


def indicateurs_stock(ventes, stock, produits, magasins) -> None:
    titre("3. INDICATEURS DE RÉFÉRENCE : STOCK ET RISQUE DE RUPTURE")
    date_reference = ventes["Date"].max()
    debut_fenetre = date_reference - pd.Timedelta(days=FENETRE_JOURS)
    recentes = ventes[ventes["Date"] > debut_fenetre]
    demande = recentes.groupby(["Store_ID", "Product_ID"])["Units"].sum().rename("Ventes_90j").reset_index()

    table = stock.merge(demande, how="left", on=["Store_ID", "Product_ID"]).fillna({"Ventes_90j": 0})
    table = table.merge(produits, on="Product_ID").merge(magasins, on="Store_ID")
    table["Ventes_jour"] = table["Ventes_90j"] / FENETRE_JOURS
    table["Couverture_jours"] = np.where(table["Ventes_jour"] > 0, table["Stock_On_Hand"] / table["Ventes_jour"], np.nan)
    table["Valeur_stock"] = table["Stock_On_Hand"] * table["Product_Cost"]

    # Même logique et mêmes seuils que la colonne calculée DAX [Statut stock]
    conditions = [
        (table["Stock_On_Hand"] == 0) & (table["Ventes_jour"] > 0),
        table["Stock_On_Hand"] == 0,
        table["Ventes_jour"] == 0,
        table["Couverture_jours"] < 7,
        table["Couverture_jours"] <= 90,
    ]
    statuts = ["Rupture", "Inactif", "Stock dormant", "Critique (< 7 j)", "Normal (7 à 90 j)"]
    table["Statut"] = np.select(conditions, statuts, default="Surstock (> 90 j)")
    table["CA_perdu_jour"] = np.where(table["Statut"] == "Rupture", table["Ventes_jour"] * table["Product_Price"], 0)

    print(f"Date de référence : {date_reference:%d/%m/%Y} | fenêtre de demande : {FENETRE_JOURS} jours")
    print(f"Stock total : {table['Stock_On_Hand'].sum():,.0f} unités | valeur au coût : {table['Valeur_stock'].sum():,.2f} $")

    print("\nRépartition par statut :")
    synthese = table.groupby("Statut").agg(
        Nb_references=("Store_ID", "size"),
        Valeur_stock=("Valeur_stock", "sum"),
        CA_perdu_jour=("CA_perdu_jour", "sum"),
    )
    synthese["Part"] = synthese["Nb_references"] / len(table)
    print(synthese.round(3).to_string())

    ca_jour_moyen = recentes.merge(produits, on="Product_ID").eval("Units * Product_Price").sum() / FENETRE_JOURS
    perte = table["CA_perdu_jour"].sum()
    print(f"\nCA potentiel perdu par jour (ruptures) : {perte:,.2f} $ soit {perte / ca_jour_moyen:.1%} du CA journalier récent")
    print(f"Estimation sur 30 jours : {perte * 30:,.0f} $")
    immobilise = table.loc[table["Statut"].isin(["Surstock (> 90 j)", "Stock dormant"]), "Valeur_stock"].sum()
    print(f"Valeur du stock immobilisé (surstock + dormant) : {immobilise:,.2f} $ soit {immobilise / table['Valeur_stock'].sum():.1%}")

    print("\nProduits les plus touchés par les ruptures :")
    ruptures = table[table["Statut"] == "Rupture"].groupby("Product_Name").agg(
        Magasins=("Store_ID", "nunique"), CA_perdu_jour=("CA_perdu_jour", "sum")
    )
    print(ruptures.sort_values("CA_perdu_jour", ascending=False).head(8).round(2).to_string())

    print("\nMagasins avec le plus de ruptures :")
    par_magasin = table[table["Statut"] == "Rupture"].groupby("Store_Name").agg(
        Ruptures=("Product_ID", "count"), CA_perdu_jour=("CA_perdu_jour", "sum")
    )
    print(par_magasin.sort_values("CA_perdu_jour", ascending=False).head(5).round(2).to_string())

    print("\nCouverture moyenne par catégorie :")
    categorie = table.groupby("Categorie").agg(Stock=("Stock_On_Hand", "sum"), Ventes_jour=("Ventes_jour", "sum"),
                                                Valeur_stock=("Valeur_stock", "sum"))
    categorie["Couverture_jours"] = categorie["Stock"] / categorie["Ventes_jour"]
    categorie["Part_stock"] = categorie["Stock"] / categorie["Stock"].sum()
    print(categorie.round(2).to_string())


def main() -> None:
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 20)
    ventes, produits, magasins, stock, calendrier = charger_donnees()
    audit_qualite(ventes, produits, magasins, stock, calendrier)
    detail, produits_prep, magasins_prep = preparer(ventes, produits, magasins)
    indicateurs_ventes(detail)
    indicateurs_stock(ventes, stock, produits_prep, magasins_prep)


if __name__ == "__main__":
    main()
