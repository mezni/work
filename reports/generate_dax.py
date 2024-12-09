import yaml

# Function to read YAML file
def read_yaml_file(file_path):
    """Reads a YAML file and returns its content as a Python dictionary."""
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config

# Function to create the output file
def create_output_file(file_path):
    """Creates the output file and writes a section header."""
    with open(file_path, 'w') as file:  # Open the file in write mode (this creates the file)
        file.write("#------------\n")  # Initial section header

# Function to append DAX query to file
def write_dax_query_to_file(file_path, query, dax_measure):
    """Appends the DAX query to the specified file with a section header"""
    with open(file_path, 'a') as file:
        file.write(f"# {query} starts here\n")
        file.write(dax_measure + '\n')
        file.write("#------------\n\n")

# Define the components for the FiltreCompte query
filtre_compte_table_name = "dimCarteCompte"
filtre_compte_column1 = "Description"
filtre_compte_column2 = "TypeCompteCtb_CentreCoutCode"
filtre_compte_filter_values = {"5-0500", "5-1000", "5-3020", "5-3030"}

# Define the calendar table components
calendar_table_name = "CalendrierFinancier"
calendar_column_name = "Date"

# Define the list of DAX queries (now renamed to dax_utils), without explicit names
dax_utils = [
    '''
    Current Date = 
    FORMAT(TODAY(), "dd mmm yyyy", "fr-FR")''',
    '''
    First Day FY = 
    FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)), "dd mmm yyyy", "fr-FR")''',
    '''
    Last Day FY = 
    FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 3, 31), DATE(YEAR(TODAY()) - 1, 3, 31)), "dd mmm yyyy", "fr-FR")''',
    '''
    Month Progression Percentage = 
    VAR _DaysElapsed = TODAY() - DATE(YEAR(TODAY()), MONTH(TODAY()), 1) + 1
    VAR _TotalDaysInMonth = EOMONTH(TODAY(), 0) - DATE(YEAR(TODAY()), MONTH(TODAY()), 1) + 1
    RETURN
        DIVIDE(_DaysElapsed, _TotalDaysInMonth, 0) * 100
    ''',
    f'''
    FiltreCompte = 
    SUMMARIZE(
        FILTER(
            {filtre_compte_table_name},
            {filtre_compte_table_name}[{filtre_compte_column2}] IN {"{" + ', '.join(f'"{value}"' for value in filtre_compte_filter_values) + "}"}
        ), 
        {filtre_compte_table_name}[{filtre_compte_column1}], 
        {filtre_compte_table_name}[{filtre_compte_column2}]
    )
    ''',
    '''
    FiltreAtelier = 
    SUMMARIZE(
        FILTER(
            dimUniteAdm,
            dimUniteAdm[estAtelier] = 1 
        ), 
        dimUniteAdm[UniteAdmId],
        dimUniteAdm[Nom]
    )
    '''
]

# Initialize an empty dictionary for DAX measure templates (dax_mesures_templates)
dax_mesures_templates = {
    "SUM": """
{mesure_name} = 
VAR _amount = SUM({table_name}[{column_name}])
VAR _format = IF(ISBLANK({mesure_format}), _amount, FORMAT(_amount, {mesure_format}))
RETURN 
    _format
"""
}

# Define the file path
file_path = 'dax_queries.txt'  # File to store the queries

# Load the YAML configuration
config = read_yaml_file("config.yaml")

# Create and open the file first, then loop through dax_utils
create_output_file(file_path)

# Write the DAX queries (dax_utils) to the file
for query in dax_utils:
    # Extract the query name based on a pattern or a portion of the query (e.g., the first line)
    query_name = query.split('=')[0].strip()

    # Use the function to write the query to the file
    write_dax_query_to_file(file_path, query_name, query)

# Function to create and write the DAX measures from the YAML configuration
if "measures" in config:
    for measure in config["measures"]:
        # Extract values for the current measure
        query = measure["mesure_name"]
        measure_type = measure["mesure_type"]
        table_name = measure["table_name"]
        column_name = measure["column_name"]
        
        # Get the mesure_format from the measure if available, else use an empty string
        mesure_format = measure.get("mesure_format", "")  # Default to empty string if not provided

        # Check if the measure type is available in dax_templates
        if measure_type in dax_mesures_templates:
            dax_measure_template = dax_mesures_templates[measure_type]

            # Format the template with measure details
            dax_measure = dax_measure_template.format(
                mesure_name=query,
                table_name=table_name,
                column_name=column_name,
                mesure_format=f'"{mesure_format}"' if mesure_format else '""'  # Ensure it is surrounded by quotes
            )

            # Use the function to write the measure to the file
            write_dax_query_to_file(file_path, query, dax_measure)

else:
    print("Error: 'measures' key is missing in the YAML file.")

print("Finish")
