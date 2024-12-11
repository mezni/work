# Define the calendar table name and date column for use in templates
calendar_table_name = "dimCalendrier"
calendar_date_column = "Date"

# Define the DAX templates as a dictionary, each for a specific measure_type
dax_templates = {
    "Mesure": """
    {name} = {value}
    """,
    "Prompt": """
    {name} = {value}
    """,
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
    "SumCurrentFinancialYearVS": """
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
    "SumCurrentFinancialYearVS%": """
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
        DIVIDE (_result1 - _result2,_result1,0)
    """,
    "SumCurrentFinancialYearVSLastYear": """
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
    VAR _start_date_last_year =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY())-1, 4, 1), 
            DATE(YEAR(TODAY()) - 2, 4, 1)
        )
    VAR _end_date_last_year =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()) , 3, 31), 
            DATE(YEAR(TODAY())-1, 3, 31)
        )
    VAR _result1 = CALCULATE(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}] >= _start_date &&
            {calendar_table}[{date_column}] <= _end_date
    )
    VAR _result2 = CALCULATE(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}] >= _start_date_last_year &&
            {calendar_table}[{date_column}] <= _end_date_last_year
    )
    RETURN
        _result1 - _result2 	
    """,
    "SumCurrentFinancialYearVSLastYear%": """
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
    VAR _start_date_last_year =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY())-1, 4, 1), 
            DATE(YEAR(TODAY()) - 2, 4, 1)
        )
    VAR _end_date_last_year =
        IF(
            MONTH(TODAY()) >= 4, 
            DATE(YEAR(TODAY()) , 3, 31), 
            DATE(YEAR(TODAY())-1, 3, 31)
        )
    VAR _result1 = CALCULATE(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}] >= _start_date &&
            {calendar_table}[{date_column}] <= _end_date
    )
    VAR _result2 = CALCULATE(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}] >= _start_date_last_year &&
            {calendar_table}[{date_column}] <= _end_date_last_year
    )
    RETURN
        DIVIDE (_result1 - _result2,_result1,0)	
    """,
}

# Separate the params_list into three lists based on measure_type

params_tables = [
    {
        "measure_name": "FiltreAtelier",  
        "measure_type": "Table",  
        "table_name": "dimUniteAdm",
        "filter_column": "estAtelier",
        "filter_value": "= 1",
        "columns": ["UniteAdmId", "Nom"]  
    },
    {
        "measure_name": "FiltreCompte",  
        "measure_type": "Table",  
        "table_name": "dimCarteCompte",
        "filter_column": "TypeCompteCtb_CentreCoutCode",
        "filter_value": ' IN {"5-3020", "5-3030", "5-1000", "5-0500"}',
        "columns": ["Description", "TypeCompteCtb_CentreCoutCode"]  
    },
]

params_utils = [
    {
        "measure_name": "Date courante",  
        "measure_type": "Prompt",  
        "name": "Date courante",
        "value": 'FORMAT(TODAY(), "dd mmm yyyy", "fr-FR")'
    },
    {
        "measure_name": "Premier jour AF",  
        "measure_type": "Prompt",  
        "name": "Premier jour AF",
        "value": 'FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)), "dd mmm yyyy", "fr-FR")'
    },
    {
        "measure_name": "Dernier jour AF",  
        "measure_type": "Prompt",  
        "name": "Dernier jour AF",
        "value": 'FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 3, 31), DATE(YEAR(TODAY()) - 1, 3, 31)), "dd mmm yyyy", "fr-FR")'
    },
    {
        "measure_name": "Annee courante",  
        "measure_type": "Prompt",  
        "name": "Annee courante",
        "value": 'FORMAT(DATE(YEAR(TODAY()), MONTH(TODAY()), 1), "mmm yyyy", "fr-FR")'
    },
]

params_mesures = [
    {
        "measure_name": "Réel AEC",  
        "measure_type": "SumCurrentFinancialYear",  
        "table_name": "reel",
        "column_name": "reel"
    },
    {
        "measure_name": "AEC vs budget",  
        "measure_type": "SumCurrentFinancialYearVS",  
        "table_name1": "reel",
        "column_name1": "reel",
        "table_name2": "budget_prevision",
        "column_name2": "budget"
    },
    {
        "measure_name": "AEC vs budget %",  
        "measure_type": "SumCurrentFinancialYearVS%",  
        "table_name1": "reel",
        "column_name1": "reel",
        "table_name2": "budget_prevision",
        "column_name2": "budget"
    },
    {
        "measure_name": "AEC vs prevision",  
        "measure_type": "SumCurrentFinancialYearVS",  
        "table_name1": "reel",
        "column_name1": "reel",
        "table_name2": "budget_prevision",
        "column_name2": "prevision"
    },
    {
        "measure_name": "AEC vs prevision %",  
        "measure_type": "SumCurrentFinancialYearVS%",  
        "table_name1": "reel",
        "column_name1": "reel",
        "table_name2": "budget_prevision",
        "column_name2": "prevision"
    },
    {
        "measure_name": "AEC vs APR",  
        "measure_type": "SumCurrentFinancialYearVSLastYear",  
        "table_name": "reel",
        "column_name": "reel",
    },
    {
        "measure_name": "AEC vs APR %",  
        "measure_type": "SumCurrentFinancialYearVSLastYear%",  
        "table_name": "reel",
        "column_name": "reel",
    },
]

params_prompts = [
    {
        "measure_name": "Réel AEC Affichage",  
        "measure_type": "Prompt",  
        "name": "Réel AEC Affichage",
        "value": 'FORMAT ([Réel AEC],  "### ### ### $")'
    }, 
    {
        "measure_name": "AEC vs budget % Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs budget Affichage",
        "value": 'FORMAT ([AEC vs budget %],  "0%")'
    }, 
    {
        "measure_name": "AEC vs budget Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs budget Affichage",
        "value": 'FORMAT ([AEC vs budget],  "### ### ### $")'
    }, 
    {
        "measure_name": "AEC vs prevision % Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs prevision Affichage",
        "value": 'FORMAT ([AEC vs prevision %],  "0%")'
    }, 
    {
        "measure_name": "AEC vs prevision Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs prevision Affichage",
        "value": 'FORMAT ([AEC vs prevision],  "### ### ### $")'
    }, 
    {
        "measure_name": "AEC vs APR % Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs APR Affichage",
        "value": 'FORMAT ([AEC vs prevision %],  "0%")'
    }, 
    {
        "measure_name": "AEC vs APR Affichage",  
        "measure_type": "Prompt",  
        "name": "AEC vs APR Affichage",
        "value": 'FORMAT ([AEC vs APR],  "### ### ### $")'
    }, 
]

params_titres = [
    {
        "measure_name": "Réel AEC Titre",  
        "measure_type": "Prompt",  
        "name": "Réel AEC Titre",
        "value": '"Réel AEC"'
    },
    {
        "measure_name": "Réel vs 1 an Titre",  
        "measure_type": "Prompt",  
        "name": "Réel vs 1 an Titre",
        "value": '"Δ 1 an"'
    },
    {
        "measure_name": "Réel vs Budget Titre",  
        "measure_type": "Prompt",  
        "name": "Réel vs Budget Titre",
        "value": '"vs Budget"'
    },
    {
        "measure_name": "Réel vs Prévision Titre",  
        "measure_type": "Prompt",  
        "name": "Réel vs Prévision Titre",
        "value": '"vs Prévision"'
    },
    {
        "measure_name": "Suivi cumulatif Titre",  
        "measure_type": "Prompt",  
        "name": "Suivi cumulatif Titre",
        "value": '"Suivi cumulatif du " & [Premier jour AF] & " au " & [Dernier jour AF]'
    },
    {
        "measure_name": "Suivi pour le mois Titre",  
        "measure_type": "Prompt",  
        "name": "Suivi cumulatif Titre",
        "value": '"Suivi pour le mois en cours (" & [Annee courante] & ")"'
    },
]

# Now, you can iterate over each list and generate DAX queries as needed.

for params_list in [params_tables , params_utils  , params_mesures ,  params_prompts ,params_titres] :
    print("---------")
    for params in  params_list:
        # Check the measure_type and select the appropriate template
        if params["measure_type"] in dax_templates:
            selected_template = dax_templates[params["measure_type"]]
            
            # Create the DAX query based on measure_type
            if params["measure_type"] == "Table":
                summarize_columns = ", ".join([f"{params['table_name']}[{col}]" for col in params['columns']])
                dax_query = selected_template.format(
                    measure_name=params["measure_name"],
                    table_name=params["table_name"],
                    filter_column=params["filter_column"],
                    filter_value=params["filter_value"],
                    summarize_columns=summarize_columns
                )
            elif params["measure_type"] in ["Mesure", "Prompt"]:
                dax_query = selected_template.format(
                    name=params["name"],
                    value=params["value"]
                )
            elif params["measure_type"] in [ "SumCurrentFinancialYear", "SumCurrentFinancialYearVSLastYear", "SumCurrentFinancialYearVSLastYear%"]:
                dax_query = selected_template.format(
                    measure_name=params["measure_name"],
                    table_name=params["table_name"],
                    column_name=params["column_name"],
                    calendar_table=calendar_table_name,
                    date_column=calendar_date_column
                )
            elif params["measure_type"]  in ["SumCurrentFinancialYearVS", "SumCurrentFinancialYearVS%"]:
                dax_query = selected_template.format(
                    measure_name=params["measure_name"],
                    table_name1=params["table_name1"],
                    column_name1=params["column_name1"],
                    table_name2=params["table_name2"],
                    column_name2=params["column_name2"],
                    calendar_table=calendar_table_name,
                    date_column=calendar_date_column
                )        
            # Print the generated DAX query
            
            print(dax_query)
        else:
            print(f"Skipping {params['measure_name']} as its measure_type '{params['measure_type']}' is not supported.\n")
