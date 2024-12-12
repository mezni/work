def get_unicode_chars(graphics_type: str) -> dict:
    """
    Returns a dictionary of Unicode characters for traffic lights or arrows.

    Args:
        graphics_type (str): The type of graphics. Can be "traffic_lights" or "arrows".

    Returns:
        dict: A dictionary containing the Unicode characters for down, steady, and up.
    """

    if graphics_type == "traffic_lights":
        return {
            "_down_char": "UNICHAR ( 128308 )",  # Red circle
            "_steady_char": "UNICHAR ( 128993 )",  # Yellow circle
            "_up_char": "UNICHAR ( 128994 )",  # Green circle
        }
    elif graphics_type == "arrows":
        return {
            "_down_char": "UNICHAR ( 9660 )", #"UNICHAR ( 8595 )",  # Down arrow
            "_steady_char": "UNICHAR(9679)", #"UNICHAR ( 8596 )",  # Right arrow (used for steady)
            "_up_char": "UNICHAR ( 9650 )", #"UNICHAR ( 8593 )",  # Up arrow
        }
    else:
        raise ValueError("Invalid graphics type. Must be 'traffic_lights' or 'arrows'.")

def generate_dax_total_formula(
    measure_name: str = "Total",
    column_name: str = "reel",
    table_name: str = "reel",
    value_format: str = "### ### ### $",
) -> str:
    """
    Generates a DAX formula for calculating the total value.

    Args:
        measure_name (str, optional): The name of the measure. Defaults to "Total".
        column_name (str, optional): The name of the column. Defaults to "reel".
        table_name (str, optional): The name of the table. Defaults to "reel".
        value_format (str, optional): The format for the value. Defaults to "### ### ### $".

    Returns:
        str: The generated DAX formula.
    """

    formula = f"""
    {measure_name} = 
    VAR _value_format = "{value_format}"
    VAR _value = SUM({table_name}[{column_name}])
    RETURN 
        FORMAT ( _value, _value_format )
    """
    return formula

def generate_dax_yoy_formula(
    measure_name: str,
    measure_type: str,
    graphics_type: str = "arrows",
    year_offset: int = 1,
    ref_column_name: str = "reel",
    ref_table_name: str = "reel",
    over_column_name: str = "reel",
    over_table_name: str = "reel",
    date_column_name: str = "Date",
    date_table_name: str = "dimCalendrier",
    value_format: str = "### ### ### $",
    perc_format: str = "0 %",
) -> str:
    """
    Generates a DAX formula for calculating the year-over-year (YoY) difference.

    Args:
        measure_name (str): The name of the measure.
        measure_type (str): The type of the measure. Can be "value", "percentage", or "status".
        graphics_type (str): The type of graphics to use. Can be "traffic_lights" or "arrows".
        year_offset (int, optional): The year offset. Defaults to 1.
        ref_column_name (str, optional): The name of the reference column. Defaults to "reel".
        ref_table_name (str, optional): The name of the reference table. Defaults to "reel".
        over_column_name (str, optional): The name of the override column. Defaults to "reel".
        over_table_name (str, optional): The name of the override table. Defaults to "reel".
        date_column_name (str, optional): The name of the date column. Defaults to "Date".
        date_table_name (str, optional): The name of the date table. Defaults to "dimCalendrier".
        value_format (str, optional): The format for the value. Defaults to "### ### ### $".
        perc_format (str, optional): The format for the percentage. Defaults to "0 %".

    Returns:
        str: The generated DAX formula.
    """

    if measure_type not in ["value", "percentage", "status", "graphic"]:
        raise ValueError("Invalid measure type. Must be 'value', 'percentage', 'status', or 'graphic'")

    if graphics_type not in ["traffic_lights", "arrows"]:
        raise ValueError("Invalid graphics type. Must be 'traffic_lights' or 'arrows'")

    unicode_chars = get_unicode_chars(graphics_type)


    formula = f"""
    {measure_name} = 
    VAR _down_char = {unicode_chars["_down_char"]}
    VAR _steady_char = {unicode_chars["_steady_char"]}
    VAR _up_char = {unicode_chars["_up_char"]}
    VAR _measure_type = "{measure_type}"
    VAR _value_format = "{value_format}"
    VAR _perc_format = "{perc_format}"
    VAR _year_offset = {year_offset}

    VAR _ref_year_value = 
        SUM ( {ref_table_name}[{ref_column_name}] )

    VAR _over_year_value = 
        CALCULATE (
            SUM ( {over_table_name}[{over_column_name}] ),
            DATEADD ( {date_table_name}[{date_column_name}], -_year_offset, YEAR )
        )

    VAR _diff = 
        _ref_year_value - _over_year_value

    VAR _pct = 
        IF (
            _over_year_value = 0, 
            BLANK(), 
            DIVIDE ( _diff, _over_year_value )
        )

    RETURN 
        SWITCH (
            TRUE (),
            _measure_type = "value", FORMAT ( _diff, _value_format ),
            _measure_type = "percentage", FORMAT ( _pct, _perc_format ),
            _measure_type = "status", 
                IF ( _diff < 0, -1, 
                    IF ( _diff > 0, 1, 0 ) ),
            _measure_type = "graphic",  
                IF ( _diff < 0,  _down_char, 
                    IF ( _diff > 0, _up_char,  _steady_char )),    
            BLANK ()
        )
    """
    return formula






# Example usage:
formula = generate_dax_total_formula(
    measure_name="Total reel",
    column_name="reel",
    table_name="reel",
)
print(formula)


# Example usage:
formula = generate_dax_yoy_formula(
    measure_name="yoy graphic a3",
    year_offset=3,
    measure_type="graphic",
    ref_column_name="reel",
    ref_table_name="reel",
    over_column_name="reel",
    over_table_name="reel",
)
print(formula)

formula = generate_dax_yoy_formula(
    measure_name="yoy graphic a2",
    year_offset=2,
    measure_type="graphic",
    ref_column_name="reel",
    ref_table_name="reel",
    over_column_name="reel",
    over_table_name="reel",
)
print(formula)

formula = generate_dax_yoy_formula(
    measure_name="yoy graphic a1",
    year_offset=1,
    measure_type="graphic",
    ref_column_name="reel",
    ref_table_name="reel",
    over_column_name="reel",
    over_table_name="reel",
)


formula = generate_dax_yoy_formula(
    measure_name="yoy status a1",
    year_offset=1,
    measure_type="status",
    ref_column_name="reel",
    ref_table_name="reel",
    over_column_name="reel",
    over_table_name="reel",
)
print(formula)