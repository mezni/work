import re
def generate_standard(name, params):
    template = params.pop()
    placeholders = re.findall(r"\{(.*?)\}", template)

    measure = template
    for i, placeholder in enumerate(placeholders):
        if i < len(params):
            measure = measure.replace(f"{{{placeholder}}}", str(params[i]))

    return f"{name} = {measure}"

def generate_agg(name, measure_type, params):
    if measure_type == "SUM":
        tablename = params[0]
        columnname = params[1]
        measure = f"SUM({tablename}[{columnname}])"
        return f"{name} = {measure}"

def generate_date(name, measure_type, params):
    if  len(params) == 1:
        date_format = default_date_format
    else:
        date_format = params.pop()
    expression = params[0]   
    measure = f"FORMAT({expression},{date_format})"
    return f"{name} = {measure}"


def gen():
    frequency="Year"
    comparaison=""
    if frequency=="Year":
        start_date="IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)"
        end_date="IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
    date_table_name = "dimCalendrier"
    date_column_name = "Date"
    src_table_name = "reel"
    src_column_name = "reel"
    dst_table_name = "budget_prevision"
    dst_column_name = "budget"
    template=f"""
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    VAR _result1 = CALCULATE(
        SUM({src_table_name}[{src_column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({dst_table_name}[{dst_column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    """

    print (template)
default_date_format='"dd mmm yyyy", "fr-FR"'
mesures = [
    {"name": "MsrTotalReel", "type": "SUM", "params": ["reel", "reel"]},
    {"name": "MsrTotalBudget", "type": "SUM", "params": ["budget_prevision", "budget"]},
    {"name": "MsrTotalPrevision", "type": "SUM", "params": ["budget_prevision", "prevision"]},
    {"name": "ClcDateCourante", "type": "DATE", "params": ["TODAY()"]},
    {"name": "ClcMoisCourant", "type": "DATE", "params": ["TODAY()", '"mmm yyyy", "fr-FR"']},
    {"name": "ClcPremierJourAF", "type": "DATE", "params": ["IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"]},
    {"name": "ClcDernierJourAF", "type": "DATE", "params": ["IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 3, 31), DATE(YEAR(TODAY()) - 1, 3, 31))"]},
    {"name": "LblSuiviCumulatif", "type": "STD", "params": ["[ClcPremierJourAF]","[ClcDernierJourAF]","Suivi cumulatif du {first} au {last}"]},
    {"name": "LblSuiviCumulCompar", "type": "STD", "params": ["[ClcDernierJourAF]","Cumulatif et comparatif au {last}"]},
    {"name": "LblSuiviMoisEncours", "type": "STD", "params": ["[ClcMoisCourant]", "Suivi pour le mois en cours ({mois})"]},
    {"name": "LblEnDate", "type": "STD", "params": ["[ClcDateCourante]", "En date du {date}"]},
]



for item in mesures:
    name = item["name"]
    measure_type = item["type"]
    params = item["params"]

    if measure_type in ["SUM"]:
        result = generate_agg(name, measure_type, params)  
    elif measure_type in ["DATE"]:
        result = generate_date(name, measure_type, params)  
    elif measure_type in ["STD"]:
        result = generate_standard(name, params)  
#    print(f"{result}")

gen()