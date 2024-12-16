def print_mesure(name, mesure):
    print(f"{name} = {mesure}\n")

chars = { "down_char": "UNICHAR(9660)",
    "steady_char" : "UNICHAR(9679)",
    "up_char" : "UNICHAR(9650)"}



def generate_mesure(config):
    name = "test"
    table_name = config.get("table_name")
    column_name = config.get("column_name")
    
    # Example strings list for variables_section
    strings_list = ["VAR xxx"]
    
    variables_section = "\n"
    variables_section += "\n".join(f"  {line}" for line in strings_list)

    for key, value in chars.items():
        print(f"\t{key}: {value}")
        variables_section += f"\n  VAR {key} = {value}"

    # Create the mesure string
    mesure = f"""{variables_section}"""
    return name, mesure 

# Configuration dictionary
config = {
    "table_name": "test",
    "column_name": "ccc",
}

# Generate and print the measure
name, mesure = generate_mesure(config)
print_mesure(name, mesure)
