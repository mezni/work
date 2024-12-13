def generate_params(config):
    # Extract values from the config, defaulting format to an empty string
    measure_name = config["name"]
    measure_value = config["value"]
    measure_format = config.get("format", "")  # Default to an empty string if format is not provided
    formula = f"""
{measure_name} = FORMAT({measure_value}, {measure_format})
    """
    print(formula)

# Example list of dictionaries
configs = [
    {"type": "param", "name": "prm date courante", "value": 'TODAY()', "format": '"dd mmm yyyy", "fr-FR"'},
    {"type": "param", "name": "prm mois courant", "value": 'DATE(YEAR(TODAY()), MONTH(TODAY()), 1)', "format": '"dd mmm yyyy", "fr-FR"'},
    {"type": "param", "name": "prm premier jour AF", "value": 'IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))', "format": '"dd mmm yyyy", "fr-FR"'},
    {"type": "param", "name": "prm dernier jour AF", "value": 'IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY())+1, 3, 31), DATE(YEAR(TODAY()) , 3, 31))',"format":  '"dd mmm yyyy", "fr-FR"'},
]

# Iterate over the list and call generate_params for matching dictionaries
for item in configs:
    if item.get("type") == "param":
        generate_params(item)
