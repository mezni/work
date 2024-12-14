def generate_pop(config):
    graphics=""
    date_table_name="dimCalendrier"
    date_column_name="Date"
    period = config.get("period", "Year")
    offset = config.get("offset", 1)
    table_name = config.get("table_name")  
    column_name = config.get("column_name")  
    date_table_name = config.get("date_table_name", date_table_name)
    date_column_name = config.get("date_column_name", date_column_name)
    metrics = config.get("metrics",["diff"])
    table_name_capt=table_name.capitalize()

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
        return "Unsupported period"

    for metric in metrics:
        if metric=="diff":
            expression="_result1 - _result2"
        elif metric=="perct":
            expression="DIVIDE (_result1 - _result2, _result1, 0)"
        elif metric=="status":
            expression="IF ( _result1 - _result2 < 0, -1, IF ( _result1 - _result2 > 0, 1, 0 ))"
        elif metric=="graphic":
            expression="IF ( _result1 - _result2 < 0, _down_char, IF ( _result1 - _result2 > 0, _up_char, _steady_char ))"
            graphics=f""" 
        VAR _down_char = UNICHAR(9660)
        VAR _steady_char = UNICHAR(9679)
        VAR _up_char = UNICHAR(9650)"""
    
        # Generate the DAX measure template
        template = f""" {graphics}
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
            _result 
        """
        metric_initial = metric.upper()[:1]
        name = f"{prefix}{table_name_capt}{period}{offset}{metric_initial}"
        mesure = f"{name} = {template}"
        print (mesure)

# Example configuration
config = {
    "type": "POP",
    "period": "Year",
    "offset": 1,
    "table_name": "reel",
    "column_name": "reel",
    "metrics":["diff","status","perct","graphic"]
}

# Generate the measure if the type matches "POP"
if config["type"] == "POP":
    generate_pop(config)
