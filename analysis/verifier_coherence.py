"""
Contrôle de cohérence entre le code lisible et le modèle Power BI.

Rôle dans le projet
-------------------
Le modèle Power BI (dossier powerbi/MavenToys_Pilotage.SemanticModel, format TMDL)
fait foi. Les fichiers powerbi/dax/*.dax et powerbi/power-query/*.pq en sont une
version commentée, pratique à lire sur GitHub. Si l'on modifie une mesure dans
Power BI sans reporter la modification, les deux versions divergent.

Ce script compare automatiquement :
  - les mesures de 02_mesures.dax et celles du modèle ;
  - les colonnes calculées de 01_colonnes_calculees_stock.dax ;
  - la table calculée de 03_table_constats.dax ;
  - les requêtes Power Query (.pq) et les partitions des tables ;
  - le paramètre DossierDonnees.

Exécution (depuis la racine du dépôt) :
    python analysis/verifier_coherence.py

Code retour 0 si tout est cohérent, 1 sinon (utilisable en intégration continue).
"""

import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DAX = RACINE / "powerbi" / "dax"
PQ = RACINE / "powerbi" / "power-query"
MODELE = RACINE / "powerbi" / "MavenToys_Pilotage.SemanticModel" / "definition"

REQUETES = {
    "01_Ventes.pq": "Ventes",
    "02_Produits.pq": "Produits",
    "03_Magasins.pq": "Magasins",
    "04_Stock.pq": "Stock",
    "05_Calendrier.pq": "Calendrier",
}


def normaliser(code: str) -> str:
    """Compare le code sans tenir compte des espaces, tabulations et retours à la ligne."""
    return re.sub(r"\s+", "", code)


def lire(chemin: Path) -> str:
    return chemin.read_text(encoding="utf-8").replace("\r\n", "\n")


def nettoyer_fin(lignes: list[str]) -> str:
    """Retire les lignes vides et les commentaires qui suivent une expression."""
    while lignes and (not lignes[-1].strip() or lignes[-1].strip().startswith("//")):
        lignes.pop()
    return "\n".join(lignes)


# --- Lecture des fichiers lisibles ---------------------------------------------
def mesures_dax() -> dict[str, str]:
    corps = lire(DAX / "02_mesures.dax").split("DEFINE", 1)[1].split("// ====", 1)[0]
    mesures, courante = {}, None
    for ligne in corps.splitlines():
        entete = re.match(r"^    MEASURE '_Mesures'\[(.+)\] =\s*$", ligne)
        if re.match(r"^    // \d\. ", ligne):
            courante = None
        elif entete:
            courante = entete.group(1)
            mesures[courante] = []
        elif courante is not None:
            mesures[courante].append(ligne)
    return {nom: nettoyer_fin(lignes) for nom, lignes in mesures.items()}


def colonnes_dax() -> dict[str, str]:
    colonnes, courante = {}, None
    for ligne in lire(DAX / "01_colonnes_calculees_stock.dax").splitlines():
        entete = re.match(r"^([^/\s].*?) =\s*$", ligne)
        if entete:
            courante = entete.group(1)
            colonnes[courante] = []
        elif courante is not None:
            colonnes[courante].append(ligne)
    return {nom: nettoyer_fin(lignes) for nom, lignes in colonnes.items()}


# --- Lecture du modèle TMDL ------------------------------------------------------
def nom_tmdl(brut: str) -> str:
    brut = brut.strip()
    if brut.startswith("'") and brut.endswith("'"):
        return brut[1:-1].replace("''", "'")
    return brut


def objets_tmdl(fichier: Path, mot_cle: str) -> dict[str, str]:
    """Extrait les expressions des objets « mot_cle nom = expression » d'un fichier TMDL."""
    objets, courant = {}, None
    for ligne in lire(fichier).splitlines():
        entete = re.match(rf"^\t{mot_cle} (.+?) =\s*(.*)$", ligne)
        if entete:
            courant = nom_tmdl(entete.group(1))
            objets[courant] = [entete.group(2)] if entete.group(2) else []
        elif courant is not None and ligne.startswith("\t\t\t"):
            objets[courant].append(ligne)
        elif courant is not None and (ligne.startswith("\t\t") or ligne.startswith("\t") or not ligne.strip()):
            if ligne.strip():
                courant = None
    return {nom: "\n".join(lignes) for nom, lignes in objets.items()}


def source_partition(fichier: Path) -> str:
    lignes, dans_source = [], False
    for ligne in lire(fichier).splitlines():
        if re.match(r"^\t\tsource =\s*$", ligne):
            dans_source = True
        elif dans_source and ligne.startswith("\t\t\t"):
            lignes.append(ligne)
        elif dans_source and ligne.strip():
            break
    return "\n".join(lignes)


# --- Comparaisons ------------------------------------------------------------------
def comparer(libelle: str, reference: dict[str, str], modele: dict[str, str]) -> int:
    erreurs = 0
    absents_modele = sorted(set(reference) - set(modele))
    absents_fichier = sorted(set(modele) - set(reference))
    differents = sorted(n for n in set(reference) & set(modele) if normaliser(reference[n]) != normaliser(modele[n]))
    for nom in absents_modele:
        print(f"  [ÉCART] {libelle} « {nom} » présent dans le fichier mais absent du modèle")
    for nom in absents_fichier:
        print(f"  [ÉCART] {libelle} « {nom} » présent dans le modèle mais absent du fichier")
    for nom in differents:
        print(f"  [ÉCART] {libelle} « {nom} » : formule différente entre le fichier et le modèle")
    erreurs = len(absents_modele) + len(absents_fichier) + len(differents)
    statut = "OK" if erreurs == 0 else f"{erreurs} écart(s)"
    print(f"{libelle:<28} {len(reference):>3} dans les fichiers | {len(modele):>3} dans le modèle | {statut}")
    return erreurs


def main() -> int:
    erreurs = 0
    print("Contrôle de cohérence : code lisible (.dax / .pq) vs modèle Power BI (TMDL)\n")

    erreurs += comparer("Mesures", mesures_dax(), objets_tmdl(MODELE / "tables" / "_Mesures.tmdl", "measure"))
    erreurs += comparer("Colonnes calculées", colonnes_dax(), objets_tmdl(MODELE / "tables" / "Stock.tmdl", "column"))

    constats = lire(DAX / "03_table_constats.dax").split("Constats =", 1)[1]
    erreurs += comparer("Table Constats", {"Constats": constats},
                        {"Constats": source_partition(MODELE / "tables" / "Constats.tmdl")})

    requetes_fichiers = {table: lire(PQ / fichier) for fichier, table in REQUETES.items()}
    requetes_modele = {table: source_partition(MODELE / "tables" / f"{table}.tmdl") for table in REQUETES.values()}
    erreurs += comparer("Requêtes Power Query", requetes_fichiers, requetes_modele)

    parametre_fichier = [l for l in lire(PQ / "00_DossierDonnees.pq").splitlines() if l.strip() and not l.startswith("//")]
    parametre_modele = re.search(r"^expression DossierDonnees = (.+)$", lire(MODELE / "expressions.tmdl"), re.M)
    erreurs += comparer("Paramètre DossierDonnees", {"DossierDonnees": parametre_fichier[0] if parametre_fichier else ""},
                        {"DossierDonnees": parametre_modele.group(1) if parametre_modele else ""})

    print("\nRésultat : " + ("tout est cohérent." if erreurs == 0 else f"{erreurs} écart(s) à corriger."))
    return 0 if erreurs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
