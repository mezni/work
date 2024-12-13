def generate_pop(config):
    name = ""
    period = config.get("period", "Year")
    offset = config.get("offset", 1)  # Default offset is 1

    if period == "Year":
        start_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"
        end_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        over_start_date = f"DATE(YEAR(_start_date) - {offset}, MONTH(_start_date), DAY(_start_date))"
        over_end_date = f"DATE(YEAR(_end_date) - {offset}, MONTH(_end_date), DAY(_end_date))"
        name = "YoY"
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        over_start_date = f"EDATE(_start_date, -{offset})"
        over_end_date = f"EDATE(_end_date, -{offset})"
        name = "MoM"
    else:
        return "Unsupported period"

    # Generate the DAX measure template
    template = f"""
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    VAR _over_start_date = {over_start_date}
    VAR _over_end_date = {over_end_date}
    RETURN
        _start_date
    """
    return f"{name} = {template}"

# Example configuration
config = {"type": "POP", "period": "Year", "offset": 1}

# Generate the measure if the type matches "POP"
if config["type"] == "POP":
    measure = generate_pop(config)
    print(measure)
