# Define the components of the DAX query
table_name = "dimCarteCompte"
column1 = "Description"
column2 = "TypeCompteCtb_CentreCoutCode"
filter_values = {"5-0500", "5-1000", "5-3020", "5-3030"}

# Initialize an empty list to hold the DAX queries
dax_queries = []

# Define the current date variable
dax_current_date = 'Actual Date = FORMAT(TODAY(), "dd, mmmm", "fr-FR")'

# Append the current_date to dax_queries
dax_queries.append(dax_current_date)

# Generate the DAX query for FiltreCompte
dax_filtre_compte = f"""
FiltreCompte = 
SUMMARIZE(
    FILTER(
        '{table_name}',
        '{column2}' IN ("{', '.join([f'"{value}"' for value in filter_values])}")
    ), 
    '{column1}', 
    '{column2}'
)
"""

# Add the generated query to the list
dax_queries.append(dax_filtre_compte)

# Print all the DAX queries in the list
for query in dax_queries:
    print("#------------")
    print(query)
