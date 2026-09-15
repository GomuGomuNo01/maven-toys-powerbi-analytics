// Requête : Ventes (table de faits)
// Grain : une ligne = un produit vendu dans un magasin à une date donnée
let
    // Lecture depuis GitHub (par défaut, fonctionne sur tout poste) ou depuis un dossier local
    Contenu =
        if Text.StartsWith(DossierDonnees, "http")
        then Web.Contents(DossierDonnees & "sales.csv")
        else File.Contents(DossierDonnees & "sales.csv"),
    Source = Csv.Document(
        Contenu,
        [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    EntetesPromues = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // Sale_ID est unique sur 829 262 lignes : aucune analyse ne l'utilise et une colonne
    // à valeurs toutes différentes se compresse très mal. La supprimer allège le modèle.
    ColonnesUtiles = Table.RemoveColumns(EntetesPromues, {"Sale_ID"}),

    // Culture "en-US" : le fichier source est au format américain
    TypesAppliques = Table.TransformColumnTypes(
        ColonnesUtiles,
        {
            {"Date", type date},
            {"Store_ID", Int64.Type},
            {"Product_ID", Int64.Type},
            {"Units", Int64.Type}
        },
        "en-US"
    ),
    ColonnesRenommees = Table.RenameColumns(
        TypesAppliques,
        {
            {"Store_ID", "ID magasin"},
            {"Product_ID", "ID produit"},
            {"Units", "Unités"}
        }
    )
in
    ColonnesRenommees
