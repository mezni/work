# List of measures to generate
measures = [
    {"measure_name": "Total Sales", "aggregation_function": "SUM", "column_name": "SalesAmount"},
    {"measure_name": "Average Sales", "aggregation_function": "AVERAGE", "column_name": "SalesAmount"},
    {"measure_name": "Max Sales", "aggregation_function": "MAX", "column_name": "SalesAmount"}
]

# Template for DAX measures
template = """
{measure_name} = 
{aggregation_function}('{table_name}'[{column_name}])
"""

# Generate DAX for each measure
table_name = "SalesTable"
for measure in measures:
    dax_formula = template.format(
        measure_name=measure["measure_name"],
        aggregation_function=measure["aggregation_function"],
        table_name=table_name,
        column_name=measure["column_name"]
    )
    print(dax_formula)


# Template for a dynamic time-intelligence DAX measure
template = """
{measure_name} = 
CALCULATE(
    {aggregation_function}('{table_name}'[{column_name}]),
    DATESYTD('{calendar_table}'[{date_column}])
)
"""

# Parameters
params = {
    "measure_name": "Total Sales YTD",
    "aggregation_function": "SUM",
    "table_name": "SalesTable",
    "column_name": "SalesAmount",
    "calendar_table": "Calendar",
    "date_column": "Date"
}

# Generate the DAX formula
dax_formula = template.format(**params)
print(dax_formula)
