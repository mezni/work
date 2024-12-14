
def get_unicode_chars(metric_graphic):
    if metric_graphic and metric_graphic=="arrows":
        return {
            "down_char":"UNICHAR(9660)",
            "steady_char":"UNICHAR(9679)",
            "up_char":"UNICHAR(9650)"
        }
    elif metric_graphic and metric_graphic=="traffic_lights":
        return {
            "down_char":"UNICHAR(128308)",
            "steady_char":"UNICHAR(128993)",
            "up_char":"UNICHAR(128994)"
        }
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
    table_name_capt = table_name.capitalize() if table_name else "Table"

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
            if metric_graphic:
                unicode_chars = get_unicode_chars(metric_graphic)
                down_char = unicode_chars["down_char"]
                steady_char = unicode_chars["steady_char"]
                up_char = unicode_chars["up_char"]

            graphics = """ """
            if metric_graphic:
                graphics = f""" 
    VAR _down_char = {down_char}
    VAR _steady_char = {steady_char}
    VAR _up_char = {up_char}"""

            if metric_type == "value":
                expression = "_result1 - _result2"
            elif metric_type == "percentage":
                expression = "DIVIDE(_result1 - _result2, _result1, 0)"
            elif metric_type == "status":
                expression = "IF(_result1 - _result2 < 0, -1, IF(_result1 - _result2 > 0, 1, 0))"

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
    VAR _result = {expression}
    RETURN
        _result"""

            # Construct the measure name
            metric_initial = metric_type.upper()[:1]
            name = f"{prefix}{table_name_capt}{period}{offset}{metric_initial}"

            # Write the generated measure to the file
            file.write(f"{name} = {template}\n\n")

configs = [
    {
    "type": "POP",
    "period": "Year",
    "offset": 1,
    "table_name": "reel",
    "column_name": "reel",
    "metrics": [{"type": "value", "graphic": "arrows"},{"type": "percentage", "graphic": "arrows"},{"type": "status"}]
    },
    {
    "type": "POP",
    "period": "Month",
    "offset": 1,
    "table_name": "reel",
    "column_name": "reel",
    "metrics": [{"type": "value", "graphic": "arrows"},{"type": "percentage", "graphic": "arrows"},{"type": "status"}]
    },
]

for config in configs:
    if config.get("type") == "POP":
        generate_pop(config, output_file="dax_measures.txt")