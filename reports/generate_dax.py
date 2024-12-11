# Define the calendar table name and date column for use in templates
calendar_table_name = "dimCalendrier"
calendar_date_column = "Date"

# Define the DAX templates as a dictionary, each for a specific measure_type
dax_templates = {
    "Table": """
    {measure_name} =
    (
        SUMMARIZE(
            FILTER(
                {table_name},
                {table_name}[{filter_column}] {filter_value}
            ), 
            {summarize_columns}
        )
    )
    """,
    "SumCurrentFinancialYear": """
    {measure_name} =
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
    "Prompt": """
    {name} = {value}
    """,
}

# List of parameters for both measures
params_list = [
    {
        "measure_name": "FiltreAtelier",  # First measure name
        "measure_type": "Table",  # Using Table as measure_type
        "table_name": "dimUniteAdm",
        "filter_column": "estAtelier",
        "filter_value": "= 1",
        "columns": ["UniteAdmId", "Nom"]  # List of columns for Filter1
    },
    {
        "measure_name": "FiltreCompte",  # Second measure name
        "measure_type": "Table",  # Using Table as measure_type
        "table_name": "dimCarteCompte",
        "filter_column": "TypeCompteCtb_CentreCoutCode",
        "filter_value": ' IN {"5-3020", "5-3030", "5-1000", "5-0500"}',
        "columns": ["Description", "TypeCompteCtb_CentreCoutCode"]  # List of columns for Filter2
    },
    {
        "measure_name": "Réel AEC",  # Third measure name
        "measure_type": "SumCurrentFinancialYear",  # Using Measure type
        "table_name": "reel",
        "column_name": "reel"
    },
    {
        "measure_name": "Réel AEC Affichage",  # Third measure name
        "measure_type": "Prompt",  # Using Measure type
        "name": "Réel AEC Affichage",
        "value": 'FORMAT ([Réel AEC],  "### ### ### $")'
    }, 
    {
        "measure_name": "Réel AEC Titre",  # Third measure name
        "measure_type": "Prompt",  # Using Measure type
        "name": "Réel AEC Titre",
        "value": '"Réel AEC"'
    }, 
    {
        "measure_name": "Réel vs 1 an Titre",  # Third measure name
        "measure_type": "Prompt",  # Using Measure type
        "name": "Réel vs 1 an Titre",
        "value": '"Δ 1 an"'
    },   
    {
        "measure_name": "Réel vs Budget Titre",  # Third measure name
        "measure_type": "Prompt",  # Using Measure type
        "name": "Réel vs Budget Titre",
        "value": '"vs Budget"'
    },
    {
        "measure_name": "Réel vs Prévision Titre",  # Third measure name
        "measure_type": "Prompt",  # Using Measure type
        "name": "Réel vs Prévision Titre",
        "value": '"vs Prévision"'
    },
]



# Generate and print DAX queries for all measures in the list
for params in params_list:
    # Check the measure_type and select the appropriate template
    if params["measure_type"] in dax_templates:
        selected_template = dax_templates[params["measure_type"]]
        
        # Use kwargs to pass parameters dynamically
        if params["measure_type"] == "Table":
            # Create the summarize_columns string for Table type
            summarize_columns = ", ".join([f"{params['table_name']}[{col}]" for col in params['columns']])
            
            # Prepare kwargs for the format
            kwargs = {
                "measure_name": params["measure_name"],
                "table_name": params["table_name"],
                "filter_column": params["filter_column"],
                "filter_value": params["filter_value"],
                "summarize_columns": summarize_columns
            }
            # Format the DAX query using kwargs
            dax_query = selected_template.format(**kwargs)
        
        elif params["measure_type"] == "SumCurrentFinancialYear":
            # Prepare kwargs for Measure type
            kwargs = {
                "measure_name": params["measure_name"],
                "table_name": params["table_name"],
                "column_name": params["column_name"],
                "calendar_table": calendar_table_name,
                "date_column": calendar_date_column
            }
            # Format the DAX query using kwargs
            dax_query = selected_template.format(**kwargs)
        elif params["measure_type"] == "Prompt":
            # Prepare kwargs for Measure type
            kwargs = {
                "measure_name": params["measure_name"],
                "name": params["name"],
                "value": params["value"]
            }
            # Format the DAX query using kwargs
            dax_query = selected_template.format(**kwargs)
        # Output the generated DAX query
        print(f"-- Generated Measure: {params['measure_name']}")
        print(dax_query)
    else:
        print(f"Skipping {params['measure_name']} as its measure_type '{params['measure_type']}' is not supported.\n")
