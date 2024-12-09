# Define the components of the DAX query
filtre_compte_table_name = "dimCarteCompte"
filtre_compte_column1 = "Description"
filtre_compte_column2 = "TypeCompteCtb_CentreCoutCode"
filtre_compte_filter_values = {"5-0500", "5-1000", "5-3020", "5-3030"}

# Initialize an empty list to hold the DAX queries
dax_queries = []

# Define the current date variable
dax_current_date = 'Current Date = FORMAT(TODAY(), "dd mmm yyyy", "fr-FR")'

# Append the current_date to dax_queries
dax_queries.append(dax_current_date)

# First Day FY
dax_fisrt_day_fy = 'First Day FY = FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)), "dd mmm yyyy", "fr-FR")'
dax_queries.append(dax_fisrt_day_fy)

# Last Day FY
dax_last_day_fy = 'Last Day FY = FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 3, 31), DATE(YEAR(TODAY()) - 1, 3, 31)), "dd mmm yyyy", "fr-FR")'
dax_queries.append(dax_last_day_fy)

# Month Progression Percentage
dax_month_progression_percentage = """
Month Progression Percentage = 
VAR _DaysElapsed = TODAY() - DATE(YEAR(TODAY()), MONTH(TODAY()), 1) + 1
VAR _TotalDaysInMonth = EOMONTH(TODAY(), 0) - DATE(YEAR(TODAY()), MONTH(TODAY()), 1) + 1
RETURN
    DIVIDE(_DaysElapsed, _TotalDaysInMonth, 0) * 100
"""
dax_queries.append(dax_month_progression_percentage)

# Generate the DAX query for FiltreCompte
dax_filtre_compte = f"""
FiltreCompte = 
SUMMARIZE(
    FILTER(
        {filtre_compte_table_name},
        {filtre_compte_table_name}[{filtre_compte_column2}] IN {"{" + ', '.join(f'"{value}"' for value in filtre_compte_filter_values) + "}"}
    ), 
    {filtre_compte_table_name}[{filtre_compte_column1}], 
    {filtre_compte_table_name}[{filtre_compte_column2}]
)
"""
dax_queries.append(dax_filtre_compte)

# Add FiltreAtelier query
dax_filtre_atelier = """
FiltreAtelier = 
SUMMARIZE(
    FILTER(
        dimUniteAdm,
        dimUniteAdm[estAtelier] = 1 
    ), 
    dimUniteAdm[UniteAdmId],
    dimUniteAdm[Nom]
)
"""
dax_queries.append(dax_filtre_atelier)

# Print all the DAX queries in the list
for query in dax_queries:
    print("#------------")
    print(query)
