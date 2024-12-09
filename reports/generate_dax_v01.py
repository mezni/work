import yaml
from datetime import datetime

# Define constants
AmountFormat = '"### ### ### $"'
first_month_calendar_year = 4  # April
financial_year_last_day = '"03-31"' 

# DAX calendar template
dax_calendar_template = """
{calendar_table_name} = 
ADDCOLUMNS(
    CALENDAR({calendar_start_date}, {calendar_end_date}),
    "AnneeFinanciere", 
        VAR _AnneeFinanciere = 
            IF (
                MONTH([Date]) >= {first_month_calendar_year}, 
                RIGHT(YEAR([Date]), 2) & RIGHT(YEAR([Date]) + 1, 2),
                RIGHT(YEAR([Date]) - 1, 2) & RIGHT(YEAR([Date]), 2)
            )
    RETURN _AnneeFinanciere,
    "AnneeMois", 
        VAR _AnneeMois = FORMAT([Date], "YYYY") & "-" & FORMAT([Date], "MM")
        RETURN _AnneeMois,
    "Mois", 
        SWITCH(
            TRUE(),
            MONTH([Date]) = 1, "JAN",
            MONTH([Date]) = 2, "FEV",
            MONTH([Date]) = 3, "MAR",
            MONTH([Date]) = 4, "AVR",
            MONTH([Date]) = 5, "MAI",
            MONTH([Date]) = 6, "JUN",
            MONTH([Date]) = 7, "JUI",
            MONTH([Date]) = 8, "AOU",
            MONTH([Date]) = 9, "SEP",
            MONTH([Date]) = 10, "OCT",
            MONTH([Date]) = 11, "NOV",
            MONTH([Date]) = 12, "DEC",
            BLANK()
        )
)
"""

# DAX measures templates
dax_mesures_template = {
    "SUMFYRW": """
{mesure_name} = 
VAR _start_date = DATE(YEAR(TODAY()) - 3, {first_month_calendar_year}, 1)  
VAR _end_date = 
    IF(
        MONTH(TODAY()) > {first_month_calendar_year} - 1,  
        DATE(YEAR(TODAY()) + 1, 3, 31),  
        DATE(YEAR(TODAY()), 3, 31)  
    )
RETURN
    CALCULATE(
        SUM({table_name}[{column_name}]),  
        FILTER(
            {calendar_table_name},
            {calendar_table_name}[{calendar_column_name}] >= _start_date 
            && {calendar_table_name}[{calendar_column_name}] <= _end_date
        )
    )
""",
    "SUMFYOY": """
{mesure_name} = 
VAR _year_offset = {year_offset}  
VAR _start_date = 
    DATE(
        YEAR(TODAY()) - _year_offset - IF(MONTH(TODAY()) < {first_month_calendar_year}, 1, 0), 
        {first_month_calendar_year}, 
        1
    )  
VAR _end_date = 
    DATE(
        YEAR(TODAY()) - _year_offset + IF(MONTH(TODAY()) >= {first_month_calendar_year}, 1, 0), 
        3, 
        31
    )  
RETURN
    CALCULATE(
        SUM({table_name}[{column_name}]),
        FILTER(
            {calendar_table_name},
            {calendar_table_name}[{calendar_column_name}] >= _start_date &&
            {calendar_table_name}[{calendar_column_name}] <= _end_date
        )
    )
""",
    "YOYFYCR": """
{mesure_name} = 
VAR _year_offset = {year_offset}
VAR _year_0 = 
    CALCULATE(
        SUM({table_name}[{column_name}]),
        FILTER(
            {calendar_table_name},
            {calendar_table_name}[{calendar_column_name}] >= DATE(
                YEAR(TODAY()) - _year_offset - IF(MONTH(TODAY()) < {first_month_calendar_year}, 1, 0), 
                {first_month_calendar_year}, 
                1
            ) &&
            {calendar_table_name}[{calendar_column_name}] <= DATE(
                YEAR(TODAY()) - _year_offset + IF(MONTH(TODAY()) >= {first_month_calendar_year}, 1, 0), 
                3, 
                31
            )
        )
    )
VAR _year_1 = 
    CALCULATE(
        SUM({table_name}[{column_name}]),
        FILTER(
            {calendar_table_name},
            {calendar_table_name}[{calendar_column_name}] >= DATE(
                YEAR(TODAY()) - (_year_offset + 1) - IF(MONTH(TODAY()) < {first_month_calendar_year}, 1, 0), 
                {first_month_calendar_year}, 
                1
            ) &&
            {calendar_table_name}[{calendar_column_name}] <= DATE(
                YEAR(TODAY()) - (_year_offset + 1) + IF(MONTH(TODAY()) >= {first_month_calendar_year}, 1, 0), 
                3, 
                31
            )
        )
    )
RETURN
    _year_0 - _year_1
"""
}

def load_yaml_config(file_path):
    """Load and return the configuration data from a YAML file."""
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def format_date_as_dax(date_string):
    """Convert a date string (YYYY-MM-DD) into a DAX-compatible DATE(YYYY, MM, DD) format."""
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return f"DATE({date_obj.year}, {date_obj.month}, {date_obj.day})"

def get_calendar_config(config):
    """Retrieve and validate calendar configuration."""
    calendar_config = config.get("calendar", {})
    
    if calendar_config.get('generate', True):
        calendar_config['calendar_start_date'] = format_date_as_dax(calendar_config.get('calendar_start_date', "2020-01-01"))
        calendar_config['calendar_end_date'] = format_date_as_dax(calendar_config.get('calendar_end_date', "2025-12-31"))
    else:
        calendar_config['calendar_start_date'] = None
        calendar_config['calendar_end_date'] = None

    calendar_config['first_month_calendar_year'] = first_month_calendar_year
    calendar_config['generate'] = calendar_config.get('generate', True)
    return calendar_config

def generate_dax_calendar(config):
    """Generate DAX calendar formula."""
    calendar_config = get_calendar_config(config)
    if calendar_config.get('generate', False):
        calendar_formula = dax_calendar_template.format(
            calendar_table_name=calendar_config['calendar_table_name'],
            calendar_start_date=calendar_config['calendar_start_date'],
            calendar_end_date=calendar_config['calendar_end_date'],
            first_month_calendar_year=calendar_config['first_month_calendar_year']
        )
        return calendar_formula
    else:
        return "-- Calendar generation skipped."

def generate_dax_mesures(config):
    """Generate DAX measures."""
    mesures = config.get("mesures", [])
    dax_mesures = []

    for mesure in mesures:
        mesure_name = mesure["mesure_name"]
        mesure_type = mesure["mesure_type"]
        table_name = mesure["table_name"]
        column_name = mesure["column_name"]
        year_offset = mesure.get("year_offset", 0)
        
        # Fetch the appropriate template
        dax_mesure_template = dax_mesures_template.get(mesure_type)
        if dax_mesure_template:
            dax_mesure = dax_mesure_template.format(
                mesure_name=mesure_name,
                table_name=table_name,
                column_name=column_name,
                year_offset=year_offset,
                AmountFormat=AmountFormat,
                calendar_table_name=calendar_table_name,
                calendar_column_name=calendar_column_name,
                financial_year_last_day=financial_year_last_day,
                first_month_calendar_year=first_month_calendar_year
            )
        else:
            dax_mesure = f"-- Unsupported mesure type: {mesure_type}"
        
        dax_mesures.append(dax_mesure)
    
    return "\n".join(dax_mesures)

def write_to_file(content, file_name):
    """Write content to a specified file."""
    with open(file_name, "w") as file:
        file.write(content)

# Main script
if __name__ == "__main__":
    calendar_table_name="dimCalendrier"
    calendar_column_name="Date"
    config_file_path = "config.yaml"  # Adjust path as necessary
    config = load_yaml_config(config_file_path)

    # Generate the DAX measures
    generated_dax_mesures = generate_dax_mesures(config)
    write_to_file(generated_dax_mesures, "DAX_Measures.dax")
    print("DAX Measures written to DAX_Measures.dax")
