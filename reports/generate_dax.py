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
        print(f"{result}")
    elif measure_type in ["DATE"]:
        result = generate_date(name, measure_type, params)  
        print(f"{result}")
    elif measure_type in ["STD"]:
        result = generate_standard(name, params)  
        print(f"{result}")
