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
    with open(file_path, 'w') as file:
        file.write("#------------\n")

# Function to append DAX query to file
def write_dax_query_to_file(file_path, query, dax_measure):
    """Appends the DAX query to the specified file with a section header."""
    with open(file_path, 'a') as file:
        file.write(f"# {query}\n")
        file.write(dax_measure + '\n')
        file.write("#------------\n\n")

# Table and column definitions
calendar_table_name = "dimCalendrier"
calendar_date_column = "Date"

# Predefined DAX utilities
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
]

# DAX measure templates
dax_mesures_templates = {
    "SUM": """
    {mesure_name} = 
    VAR _amount = SUM({table_name}[{column_name}])
    RETURN IF(
        ISBLANK({mesure_format}),
        _amount,
        FORMAT(_amount, {mesure_format})
    )
    """,
    "SUM4FY": """
    {mesure_name} = 
    VAR _year_window = 4
    VAR _start_date = DATE(YEAR(TODAY()) - _year_window, 4, 1)
    VAR _end_date = IF(
        MONTH(TODAY()) >= 4,
        DATE(YEAR(TODAY()) + 1, 3, 31),
        DATE(YEAR(TODAY()), 3, 31)
    )
    RETURN
        CALCULATE(
            SUM({table_name}[{column_name}]),
            FILTER(
                {calendar_table},
                {calendar_table}[{date_column}] >= _start_date &&
                {calendar_table}[{date_column}] <= _end_date
            )
        )
    """,
    "SUMCFY": """
    {mesure_name} =
    VAR _start_date =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()), 4, 1), 
            DATE(YEAR(TODAY()) - 1, 4, 1)
        )
    VAR _end_date =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()) + 1, 3, 31), 
            DATE(YEAR(TODAY()), 3, 31)
        )
    RETURN
        CALCULATE(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}] >= _start_date &&
            {calendar_table}[{date_column}] <= _end_date
        )
    """,
    "CFYVS": """
    {mesure_name} =
    VAR _start_date =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()), 4, 1), 
            DATE(YEAR(TODAY()) - 1, 4, 1)
        )
    VAR _end_date =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()) + 1, 3, 31), 
            DATE(YEAR(TODAY()), 3, 31)
        )
    VAR _result1 = CALCULATE(
        SUM({table_name1}[{column_name1}]),
        {calendar_table}[{date_column}] >= _start_date &&
        {calendar_table}[{date_column}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({table_name2}[{column_name2}]),
        {calendar_table}[{date_column}] >= _start_date &&
        {calendar_table}[{date_column}] <= _end_date
    )
    RETURN
        _result1 - _result2
    """,
    "CMVS": """
    {mesure_name} =
    VAR _start_date = DATE(YEAR(TODAY()), MONTH(TODAY()), 1)
    VAR _end_date = EOMONTH(TODAY(), 0)
    VAR _result1 = CALCULATE(
        SUM({table_name1}[{column_name1}]),
        {calendar_table}[{date_column}] >= _start_date &&
        {calendar_table}[{date_column}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({table_name2}[{column_name2}]),
        {calendar_table}[{date_column}] >= _start_date &&
        {calendar_table}[{date_column}] <= _end_date
    )
    RETURN
        _result1 - _result2
    """,
}

# File path for output
file_path = 'dax_queries.txt'

# Load the YAML configuration
config = read_yaml_file("config.yaml")

# Create and open the file
create_output_file(file_path)

# Write the DAX utilities to the file
for query in dax_utils:
    query_name = query.split('=')[0].strip()
    write_dax_query_to_file(file_path, query_name, query)

# Define valid measure types
valid_mesure_types = dax_mesures_templates.keys()




# Write DAX measures from the YAML configuration
if "measures" in config:
    for measure in config["measures"]:
        # Extract measure details
        mesure_name = measure["mesure_name"]
        mesure_type = measure["mesure_type"]


        # Handle CFYVS type specifically
        if mesure_type in  ["CFYVS","CMVS"]:
            # Ensure table1 and table2 are present
            table_name1 = measure.get("table_name1")
            column_name1 = measure.get("column_name1")
            table_name2 = measure.get("table_name2")
            column_name2 = measure.get("column_name2")

            # Format the CFYVS template
            dax_measure = dax_mesures_templates[mesure_type].format(
                mesure_name=mesure_name,
                table_name1=table_name1,
                column_name1=column_name1,
                table_name2=table_name2,
                column_name2=column_name2,
                calendar_table=calendar_table_name,
                date_column=calendar_date_column
            )
        else:
            # Handle other measure types
            table_name = measure.get("table_name", "")
            column_name = measure.get("column_name", "")
            mesure_format = measure.get("mesure_format", "")

            # Format the template
            dax_measure = dax_mesures_templates[mesure_type].format(
                mesure_name=mesure_name,
                table_name=table_name,
                column_name=column_name,
                mesure_format=f'"{mesure_format}"' if mesure_format else '""',
                calendar_table=calendar_table_name,
                date_column=calendar_date_column
            )

        # Write the measure to the file
        write_dax_query_to_file(file_path, mesure_name, dax_measure)
else:
    print("Error: 'measures' key is missing in the YAML file.")

print("Finish")
