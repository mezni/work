import yaml

# Define the format as a string
AmountFormat = '"### ### ### $"'

calendar_table_name = "CalendrierFinancier"
calendar_column_name = "Date"

financial_year_last_day = '"03-31"' 

# Define DAX templates
dax_templates = {
    "SUM": """
{measure_name} = 
VAR _amount = SUM({table_name}[{column_name}])
RETURN 
    FORMAT(_amount, {AmountFormat})
""",
    "YTD": """
{measure_name} = 
VAR _amount = CALCULATE(
    SUM({table_name}[{column_name}]),
    DATESYTD(
        {calendar_table_name}[{calendar_column_name}],
        {financial_year_last_day}  
    ),
    FILTER(
        ALL({calendar_table_name}[{calendar_column_name}]),
        {calendar_table_name}[{calendar_column_name}] >= DATE(YEAR(TODAY()) - 4, 4, 1)
    )
)
RETURN 
    FORMAT(_amount, {AmountFormat})
"""
}

# Load the YAML configuration file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Iterate through the measures in the YAML
for measure in config["measures"]:
    # Extract values for the current measure
    measure_name = measure["mesure_name"]  # Changed from 'name' to 'measure_name'
    measure_type = measure["mesure_type"]  # Changed from 'type' to 'measure_type'
    table_name = measure["table_name"]
    column_name = measure["column_name"]

    # Check if the measure type is available in the dax_templates dictionary
    if measure_type in dax_templates:
        # Get the appropriate template
        dax_measure_template = dax_templates[measure_type]

        # Format the template with the measure details, including calendar table info
        dax_measure = dax_measure_template.format(
            measure_name=measure_name,  # Use 'measure_name' variable
            table_name=table_name,
            column_name=column_name,
            AmountFormat=AmountFormat,  # Pass the format as a string
            calendar_table_name=calendar_table_name,  # Include calendar table name
            calendar_column_name=calendar_column_name,  # Include calendar column name
            financial_year_last_day=financial_year_last_day  # Include the financial year end
        )

        # Print the generated DAX measure
        print(dax_measure)
        print("-" * 80)  # Separator for readability
    else:
        raise ValueError(f"Unsupported measure type: {measure_type}")
