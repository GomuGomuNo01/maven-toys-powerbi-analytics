// Requête : Magasins (dimension)
// Grain : une ligne = un magasin (50 magasins)
let
    Source = Csv.Document(
        File.Contents(DossierDonnees & "stores.csv"),
        [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    EntetesPromues = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TypesAppliques = Table.TransformColumnTypes(
        EntetesPromues,
        {
            {"Store_ID", Int64.Type},
            {"Store_Name", type text},
            {"Store_City", type text},
            {"Store_Location", type text},
            {"Store_Open_Date", type date}
        },
        "en-US"
    ),

    // Correction d'une faute de frappe dans la source ("Cuidad" au lieu de "Ciudad").
    // Sans cette correction, la ville serait mal nommée dans tous les visuels.
    VilleCorrigee = Table.ReplaceValue(
        TypesAppliques, "Cuidad de Mexico", "Ciudad de Mexico", Replacer.ReplaceValue, {"Store_City"}
    ),

    EmplacementsTraduits = Table.TransformColumns(
        VilleCorrigee,
        {
            {
                "Store_Location",
                each Record.FieldOrDefault(
                    [
                        Downtown = "Centre-ville",
                        Commercial = "Zone commerciale",
                        Residential = "Quartier résidentiel",
                        Airport = "Aéroport"
                    ],
                    _,
                    _
                ),
                type text
            }
        }
    ),
    ColonnesRenommees = Table.RenameColumns(
        EmplacementsTraduits,
        {
            {"Store_ID", "ID magasin"},
            {"Store_Name", "Magasin"},
            {"Store_City", "Ville"},
            {"Store_Location", "Type d'emplacement"},
            {"Store_Open_Date", "Date d'ouverture"}
        }
    )
in
    ColonnesRenommees
