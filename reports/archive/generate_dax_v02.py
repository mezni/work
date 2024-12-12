# Define the list of measures with their properties, including table_name
measures = [
    {"measure_name": "Total Reel", "type": "sum", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Average Sales", "type": "avr", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Total Sales YTD", "type": "ytd", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Year-over-Year Sales", "type": "year_over_year", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Month-over-Month Sales", "type": "month_over_month", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Delta Sales LY", "type": "delta_last_year", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Delta Sales LY %", "type": "delta_last_year_percentage", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Delta Sales LM", "type": "delta_last_month", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "Delta Sales LM %", "type": "delta_last_month_percentage", "column_name": "reel", "table_name": "reel"}
]

# Templates for different DAX types
dax_templates = {
    "sum": """
{measure_name} = 
FORMAT(
    SUM('{table_name}'[{column_name}]), 
    "### ### ### $"
)
""",
    "avr": "{measure_name} = AVERAGE('{table_name}'[{column_name}])",
    "ytd": """
{measure_name} = 
CALCULATE(
    SUM('{table_name}'[{column_name}]),
    DATESYTD('{calendar_table}'[{date_column}])
)
""",
    "year_over_year": """
{measure_name} = 
CALCULATE(
    SUM('{table_name}'[{column_name}]),
    SAMEPERIODLASTYEAR('{calendar_table}'[{date_column}])
)
""",
    "month_over_month": """
{measure_name} = 
CALCULATE(
    SUM('{table_name}'[{column_name}]),
    DATEADD('{calendar_table}'[{date_column}], -1, MONTH)
)
""",
    "delta_last_year": """
{measure_name} = 
SUM('{table_name}'[{column_name}]) - 
CALCULATE(SUM('{table_name}'[{column_name}]), SAMEPERIODLASTYEAR('{calendar_table}'[{date_column}]))
""",
    "delta_last_year_percentage": """
{measure_name} = 
DIVIDE(
    SUM('{table_name}'[{column_name}]) - 
    CALCULATE(SUM('{table_name}'[{column_name}]), SAMEPERIODLASTYEAR('{calendar_table}'[{date_column}])),
    CALCULATE(SUM('{table_name}'[{column_name}]), SAMEPERIODLASTYEAR('{calendar_table}'[{date_column}]))
)
""",
    "delta_last_month": """
{measure_name} = 
SUM('{table_name}'[{column_name}]) - 
CALCULATE(SUM('{table_name}'[{column_name}]), DATEADD('{calendar_table}'[{date_column}], -1, MONTH))
""",
    "delta_last_month_percentage": """
{measure_name} = 
DIVIDE(
    SUM('{table_name}'[{column_name}]) - 
    CALCULATE(SUM('{table_name}'[{column_name}]), DATEADD('{calendar_table}'[{date_column}], -1, MONTH)),
    CALCULATE(SUM('{table_name}'[{column_name}]), DATEADD('{calendar_table}'[{date_column}], -1, MONTH))
)
"""
}

# Parameters for calendar table
calendar_table = "Calendar"
date_column = "Date"

# Generate DAX formulas
for measure in measures:
    template = dax_templates.get(measure["type"])
    if template:
        dax_formula = template.format(
            measure_name=measure["measure_name"],
            table_name=measure["table_name"],
            column_name=measure["column_name"],
            calendar_table=calendar_table,
            date_column=date_column
        )
        print(dax_formula)
        print("-" * 80)
    else:
        print(f"Unknown measure type: {measure['type']}")
        print("-" * 80)
