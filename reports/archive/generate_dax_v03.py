"""
CalendrierFinancier = 
    ADDCOLUMNS(
        FILTER(
            CALENDAR(DATE(2019, 1, 1), DATE(2025, 12, 31)),
            DAY([Date]) = 1
        ),
        "AnneeFinanciere", 
            VAR Annee_Fin_Calc = 
                IF (
                    MONTH([Date]) >= 4, 
                    RIGHT(YEAR([Date]) , 2) & RIGHT(YEAR([Date])+1, 2),
                    RIGHT(YEAR([Date])-1, 2) & RIGHT(YEAR([Date]), 2)
                )
            RETURN Annee_Fin_Calc,
        "AnneeMois", 
            VAR AnneeMois = FORMAT([Date], "YYYY") & "-" & FORMAT([Date], "MM")
            RETURN AnneeMois
)
"""
# Define the list of measures with their properties, including table_name and OffsetYear
measures = [
    {"measure_name": "Total Reel", "type": "sum", "column_name": "reel", "table_name": "reel"},
    {"measure_name": "YTD reel (0)", "type": "ytd_fy", "column_name": "reel", "table_name": "reel", "OffsetYear": 0},
    {"measure_name": "YTD reel (1)", "type": "ytd_fy", "column_name": "reel", "table_name": "reel", "OffsetYear": 1}, 
    {"measure_name": "YTD reel (2)", "type": "ytd_fy", "column_name": "reel", "table_name": "reel", "OffsetYear": 2}, 
    {"measure_name": "YTD reel (3)", "type": "ytd_fy", "column_name": "reel", "table_name": "reel", "OffsetYear": 3}, 
    {"measure_name": "YOY reel (0)", "type": "yoy_fy", "column_name": "reel", "table_name": "reel", "OffsetYear": 0}, 
]

# Templates for different DAX types
dax_templates = {
    "sum": """
{measure_name} = 
FORMAT(
    SUM({table_name}[{column_name}]), 
    "### ### ### $"
)
""",
    "ytd_fy": """
{measure_name} = 
VAR OffsetYear = {OffsetYear} 
RETURN
FORMAT(
    CALCULATE(
        TOTALYTD(
            SUM({table_name}[{column_name}]),
            {calendar_table}[{date_column}],
            "03/31"
        ),
        {calendar_table}[{date_column}] >= DATE(
            IF(MONTH(TODAY()) >= 4, YEAR(TODAY()) - OffsetYear, YEAR(TODAY()) - OffsetYear - 1),
            4,
            1
        ) &&
        {calendar_table}[{date_column}] <= DATE(
            IF(MONTH(TODAY()) >= 4, YEAR(TODAY()) - OffsetYear, YEAR(TODAY()) - OffsetYear - 1) + 1,
            3,
            31
        )
    ),
    "### ### ### $"
)
""",
    "yoy_fy": """
{measure_name} = 
VAR _OffsetYear = {OffsetYear}
VAR_yoy = SWITCH(
        _OffsetYear,
        0,[YTD reel (0)] - [YTD reel (1)],
        1,[YTD reel (1)] - [YTD reel (2)]
  )
RETURN FORMAT( _yoy, 
    "### ### ### $"
)
"""
}

# Parameters for calendar table
calendar_table = "CalendrierFinancier"
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
            date_column=date_column,
            OffsetYear=measure.get("OffsetYear", 0)  # Default to 0 if no OffsetYear is provided
        )
        print(dax_formula)
        print("-" * 80)
    else:
        print(f"Unknown measure type: {measure['type']}")
        print("-" * 80)
