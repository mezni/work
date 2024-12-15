import re
def get_unicode_chars(metric_graphic):
    if metric_graphic == "arrows":
        return {"down_char": "UNICHAR(9660)", "steady_char": "UNICHAR(9679)", "up_char": "UNICHAR(9650)"}
    elif metric_graphic == "traffic_lights":
        return {"down_char": "UNICHAR(128308)", "steady_char": "UNICHAR(128993)", "up_char": "UNICHAR(128994)"}
    return None

def get_mesure_result(metric_type):
    return {
        "value": "_result1 - _result2",
        "percentage": "DIVIDE(_result1 - _result2, _result1, 0)",
        "status": "IF(_result1 - _result2 < 0, -1, IF(_result1 - _result2 > 0, 1, 0))",
        "graphic": "IF(_result1 - _result2 < 0, -1, IF(_result1 - _result2 > 0, 1, 0))",
    }.get(metric_type, None)

def get_mesure_expression(metric_type,metric_format, metric_graphic):
    if metric_type=="graphic":
        return f"""IF(_result < 0, _down_char, IF(_result > 0, _up_char, _steady_char))"""
    else:
        if metric_format and metric_graphic:
            return f"""IF(_result < 0, _down_char, IF(_result > 0, _up_char, _steady_char)) & " " & FORMAT(ABS(_result), "{metric_format}")"""
        if metric_format:
            return f"""FORMAT(_result, "{metric_format}")"""
    return "_result"

def generate_pop(config, output_file):
    default_date_table_name = "dimCalendrier"
    default_date_column_name = "Date"

    period = config.get("period", "Year")
    offset = config.get("offset", 1)
    table_name = config.get("table_name")
    column_name = config.get("column_name")
    date_table_name = config.get("date_table_name", default_date_table_name)
    date_column_name = config.get("date_column_name", default_date_column_name) 
    metrics = config.get("metrics", [{"type": "value"}]) 
    table_name_capt = table_name.capitalize()[:4]  
    column_name_capt = column_name.capitalize()[:4] 

    if period == "Year":
        start_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"
        end_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        over_start_date = f"DATE(YEAR(_start_date) - {offset}, MONTH(_start_date), DAY(_start_date))"
        over_end_date = f"DATE(YEAR(_end_date) - {offset}, MONTH(_end_date), DAY(_end_date))"
        prefix = "YoY"
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        over_start_date = f"EDATE(_start_date, -{offset})"
        over_end_date = f"EDATE(_end_date, -{offset})"
        prefix = "MoM"
    else:
        print("Unsupported period.")
        return

    with open(output_file, 'a') as file:
        for metric in metrics:
            metric_type = metric.get("type")  
            metric_graphic = metric.get("graphic") 
            metric_format = metric.get("format") 
            if metric_graphic:
                unicode_chars = get_unicode_chars(metric_graphic)
                down_char = unicode_chars["down_char"]
                steady_char = unicode_chars["steady_char"]
                up_char = unicode_chars["up_char"]

            result=get_mesure_result(metric_type)
            expression=get_mesure_expression(metric_type,metric_format,metric_graphic)

            graphics = """ """
            if metric_graphic:
                graphics = f""" 
    VAR _down_char = {down_char}
    VAR _steady_char = {steady_char}
    VAR _up_char = {up_char}"""

            template = f"""{graphics}
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    VAR _over_start_date = {over_start_date}
    VAR _over_end_date = {over_end_date}
    VAR _result1 = CALCULATE(
        SUM({table_name}[{column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({table_name}[{column_name}]),
        {date_table_name}[{date_column_name}] >= _over_start_date &&
        {date_table_name}[{date_column_name}] <= _over_end_date
    )
    VAR _result = {result}
    RETURN
        {expression}"""

            # Construct the measure name
            metric_initial = metric_type.upper()[:1]
            format_flag=""
            graphic_flag=""
            if metric_graphic:
                graphic_flag="G"
            elif metric_format:
                format_flag="F" 
                       
            name = f"{prefix}{table_name_capt}{column_name_capt}{period}{offset}{metric_initial}{graphic_flag}{format_flag}"

            # Write the generated measure to the file
            file.write(f"{name} = {template}\n\n")
            if format_flag=="":
                file.write(f"""{name}Cpt = 1 - [{name}]\n\n""")


def generate_gap(config, output_file):
    default_date_table_name = "dimCalendrier"
    default_date_column_name = "Date"

    period = config.get("period", "Year")
    src_table_name = config.get("src_table_name")
    src_column_name = config.get("src_column_name")
    dst_table_name = config.get("dst_table_name")
    dst_column_name = config.get("dst_column_name")
    date_table_name = config.get("date_table_name", default_date_table_name)
    date_column_name = config.get("date_column_name", default_date_column_name) 
    metrics = config.get("metrics", [{"type": "value"}]) 
    src_table_name_capt = src_table_name.replace("_","").capitalize()[:4] 
    dst_table_name_capt = dst_table_name.replace("_","").capitalize()[:4] 
    dst_column_name_capt = dst_column_name.capitalize()[:4] 

    if period == "Year":
        start_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"
        end_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        prefix = "GoPY"
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        prefix = "GoPM"
    else:
        print("Unsupported period.")
        return

    with open(output_file, 'a') as file:
        for metric in metrics:
            metric_type = metric.get("type")  
            metric_graphic = metric.get("graphic") 
            metric_format = metric.get("format") 
            if metric_graphic:
                unicode_chars = get_unicode_chars(metric_graphic)
                down_char = unicode_chars["down_char"]
                steady_char = unicode_chars["steady_char"]
                up_char = unicode_chars["up_char"]

            result=get_mesure_result(metric_type)
            expression=get_mesure_expression(metric_type,metric_format,metric_graphic)

            graphics = """ """
            if metric_graphic:
                graphics = f""" 
    VAR _down_char = {down_char}
    VAR _steady_char = {steady_char}
    VAR _up_char = {up_char}"""

            template = f"""{graphics}
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
    VAR _result = {result}
    RETURN
        {expression}"""

            # Construct the measure name
            metric_initial = metric_type.upper()[:1]
            format_flag=""
            graphic_flag=""
            if metric_graphic:
                graphic_flag="G"
            elif metric_format:
                format_flag="F"    
            name = f"{prefix}{src_table_name_capt}{dst_table_name_capt}{dst_column_name_capt}{period}{metric_initial}{graphic_flag}{format_flag}"

            # Write the generated measure to the file
            file.write(f"{name} = {template}\n\n")
            if format_flag=="":
                file.write(f"""{name}Cpt = 1 - [{name}]\n\n""")

def generate_flt(config, output_file):
    default_date_table_name = "dimCalendrier"
    default_date_column_name = "Date"

    period = config.get("period", "Year")
    offset = config.get("offset", 1)
    date_table_name = config.get("date_table_name", default_date_table_name)
    date_column_name = config.get("date_column_name", default_date_column_name) 

    if period == "Year":
        start_date = f"IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) - {offset} , 4, 1), DATE(YEAR(TODAY()) - {offset} - 1, 4, 1))"
        end_date = f"IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        prefix = "FltY"
        offset_flag=offset
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        prefix = "FltM"
        offset_flag=offset
    else:
        print("Unsupported period.")
        return

    with open(output_file, 'a') as file:
        template = f"""
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    RETURN
    IF(
        AND(
            MAX({date_table_name}[{date_column_name}]) >= _start_date,
            MAX({date_table_name}[{date_column_name}]) < _end_date
        ),
        1,
        0
    )"""
  
        name = f"{prefix}{offset_flag}"

        # Write the generated measure to the file
        file.write(f"{name} = {template}\n\n")


def generate_utl(config, output_file):
    name = config.get("name")
    template = config.get("template")
    params = config.get("params")
    placeholders = re.findall(r"\{(.*?)\}", template)

    mesure = template
    for i, placeholder in enumerate(placeholders):
        if i < len(params):
            mesure = mesure.replace(f"{{{placeholder}}}", str(params[i]))
    
    with open(output_file, 'a') as file:
        file.write(f"{name} = {mesure}\n\n")

def generate_lbl(config, output_file):
    name = config.get("name")
    template = config.get("template")
    params = config.get("params")
    placeholders = re.findall(r"\{(.*?)\}", template)

    parts = re.split(r"(\{.*?\})", template) 
    template = ""
    for i, part in enumerate(parts):
        if part.startswith("{") and part.endswith("}"):
            template = template + " & " + part + " & " 
        else:
            template = template + f'"{part}"'

    mesure = template
    for i, placeholder in enumerate(placeholders):
        if i < len(params):
            mesure = mesure.replace(f"{{{placeholder}}}", str(params[i]))
          
    with open(output_file, 'a') as file:
        file.write(f"{name} = {mesure}\n\n")

configs = [
    {
        "type": "UTL",
        "name": "UtlDateCourante",        
        "template": "FORMAT(TODAY(),{format})",
        "params":['"dd mmm yyyy", "fr-FR"']       
    },
    {
        "type": "UTL",
        "name": "UtlMoisCourant",        
        "template": "FORMAT(TODAY(),{format})",
        "params":['"mmm yyyy", "fr-FR"']       
    },
    {
        "type": "UTL",
        "name": "UtlPremierJourAF",        
        "template": "FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)),{format})",
        "params":['"dd mmm yyyy", "fr-FR"']       
    },
    {
        "type": "UTL",
        "name": "UtlDernierJourAF",        
        "template": "FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) +1, 3, 31), DATE(YEAR(TODAY()) , 3, 31)),{format})",
        "params":['"dd mmm yyyy", "fr-FR"']       
    }, 
    {
        "type": "LBL",
        "name": "LblSuiviCumulatif",        
        "template": "Suivi cumulatif du {first} au {last}",
        "params":["[UtlPremierJourAF]","[UtlDernierJourAF]"]       
    },
    {
        "type": "LBL",
        "name": "LblSuiviCumulCompar",        
        "template": "Cumulatif et comparatif au {last}",
        "params":["[UtlDernierJourAF]"]       
    },
    {
        "type": "LBL",
        "name": "LblSuiviMoisEncours",        
        "template": "Suivi pour le mois en cours ({mois})",
        "params":["[UtlMoisCourant]"]       
    },
    {
        "type": "LBL",
        "name": "LblEnDate",        
        "template": "En date du {date}",
        "params":["[UtlDateCourante]"]       
    },   
    {
        "type": "UTL",
        "name": "TotalReel",        
        "template": "SUM({table_name}[{column_name}])",
        "params":["reel", "reel"]       
    },
    {
        "type": "UTL",
        "name": "TotalBudget",        
        "template": "SUM({table_name}[{column_name}])",
        "params":["budget_prevision", "budget"]       
    },
    {
        "type": "UTL",
        "name": "TotalPrevision",        
        "template": "SUM({table_name}[{column_name}])",
        "params":["budget_prevision", "prevision"]       
    },
    {
        "type": "UTL",
        "name": "TotalReelF",        
        "template": "FORMAT(SUM({table_name}[{column_name}]),{format})",
        "params":["reel", "reel", '"### ### ### $"']       
    },
    {
        "type": "POP",
        "period": "Year",
        "offset": 1,
        "table_name": "reel",
        "column_name": "reel",
        "metrics": [
            {"type": "value", "format": "### ### ### $", "graphic": "arrows"},
            {"type": "percentage", "format": "0 %", "graphic": "arrows"},
            {"type": "status"}
        ]
    },
    {
        "type": "GAP",
        "period": "Year",
        "src_table_name": "reel",
        "src_column_name": "reel",
        "dst_table_name": "budget_prevision",
        "dst_column_name": "budget",
        "metrics": [
            {"type": "value", "format": "### ### ### $", "graphic": "arrows"},
            {"type": "percentage", "format": "0 %", "graphic": "arrows"},
            {"type": "status"}
        ]
    },
    {
        "type": "GAP",
        "period": "Year",
        "src_table_name": "reel",
        "src_column_name": "reel",
        "dst_table_name": "budget_prevision",
        "dst_column_name": "prevision",
        "metrics": [
            {"type": "value", "format": "### ### ### $", "graphic": "arrows"},
            {"type": "percentage", "format": "0 %", "graphic": "arrows"},
            {"type": "status"}
        ]
    },
    {
        "type": "FLT",
        "period": "Year",
        "offset": 3
    },
    {
        "type": "FLT",
        "period": "Month",
        "offset": 1
    },
    {
        "type": "GAP",
        "period": "Month",
        "src_table_name": "reel",
        "src_column_name": "reel",
        "dst_table_name": "budget_prevision",
        "dst_column_name": "budget",
        "metrics": [
            {"type": "percentage"}
        ]
    },
    {
        "type": "GAP",
        "period": "Month",
        "src_table_name": "reel",
        "src_column_name": "reel",
        "dst_table_name": "budget_prevision",
        "dst_column_name": "prevision",
        "metrics": [
            {"type": "percentage"}
        ]
    },
    {
        "type": "UTL",
        "name": "ProgressionJournees",        
        "template": "DIVIDE(DAY(TODAY()), DAY(EOMONTH(TODAY(), 0)), 0)"     
    },
    {
        "type": "UTL",
        "name": "ProgressionJourneesCpt",        
        "template": "1 - [ProgressionJournees]"     
    },
]


# Output file
output_file = "dax_measures.txt"
with open(output_file, 'w') as file:
    file.write("")  # Clear the file

# Generate measures
for config in configs:
    if config.get("type") == "UTL":
        generate_utl(config, output_file)
    elif config.get("type") == "LBL":
        generate_lbl(config, output_file)
    elif config.get("type") == "FLT":
        generate_flt(config, output_file)
    elif config.get("type") == "POP":
        generate_pop(config, output_file)
    elif config.get("type") == "GAP":
        generate_gap(config, output_file)