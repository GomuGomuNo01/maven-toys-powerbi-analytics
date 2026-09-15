// Paramètre : DossierDonnees
// ---------------------------------------------------------------------------
// Emplacement des fichiers CSV. Il DOIT se terminer par une barre oblique.
//
// Valeur par défaut : le dossier data/raw du dépôt GitHub public. Le rapport
// s'actualise ainsi sur n'importe quel ordinateur, sans rien modifier.
// (Au premier chargement, Power BI demande le type d'accès : choisir « Anonyme ».)
//
// Pour travailler hors connexion, remplacer par le chemin local du dossier,
// terminé par une barre oblique inverse, par exemple :
//   D:\...\maven-toys-powerbi-analytics\data\raw\
//
// Création : Accueil > Transformer les données > Gérer les paramètres > Nouveau
//   Nom : DossierDonnees | Type : Texte | Valeur actuelle : (URL ou chemin ci-dessous)

"https://raw.githubusercontent.com/GomuGomuNo01/maven-toys-powerbi-analytics/main/data/raw/" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
