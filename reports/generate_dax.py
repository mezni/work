def generate_dax_yoy_formula(
    measure_name: str,
    measure_type: str,
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

    if measure_type not in ["value", "percentage", "status"]:
        raise ValueError("Invalid measure type. Must be 'value', 'percentage', or 'status'.")

    formula = f"""
    {measure_name} = 
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
            BLANK ()
        )
    """
    return formula

# Example usage:
formula = generate_dax_yoy_formula(
    measure_name="yoy",
    measure_type="value",
    ref_column_name="reel",
    ref_table_name="reel",
    over_column_name="reel",
    over_table_name="reel",
)
print(formula)