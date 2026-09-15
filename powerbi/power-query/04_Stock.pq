// Requête : Stock (table de faits "photo")
// Grain : une ligne = un produit dans un magasin, à la date de fin des données
// Attention : pas de date dans cette table. Ce n'est pas un historique mais un état
// instantané. Elle ne sera donc PAS reliée au calendrier.
let
    // Lecture depuis GitHub (par défaut, fonctionne sur tout poste) ou depuis un dossier local
    Contenu =
        if Text.StartsWith(DossierDonnees, "http")
        then Web.Contents(DossierDonnees & "inventory.csv")
        else File.Contents(DossierDonnees & "inventory.csv"),
    Source = Csv.Document(
        Contenu,
        [Delimiter = ",", Columns = 3, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    EntetesPromues = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TypesAppliques = Table.TransformColumnTypes(
        EntetesPromues,
        {
            {"Store_ID", Int64.Type},
            {"Product_ID", Int64.Type},
            {"Stock_On_Hand", Int64.Type}
        },
        "en-US"
    ),
    ColonnesRenommees = Table.RenameColumns(
        TypesAppliques,
        {
            {"Store_ID", "ID magasin"},
            {"Product_ID", "ID produit"},
            {"Stock_On_Hand", "Stock disponible"}
        }
    )
in
    ColonnesRenommees
