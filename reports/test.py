def print_mesure(name, mesure):
    print(f"{name} = {mesure}\n")

def generate_mesure(config):
    name = "test"
    table_name = config.get("table_name")
    column_name = config.get("column_name")
    
    # Example strings list for variables_section
    strings_list = ["VAR xxx", "VAR ccc", "VAR vvv"]
    
    variables_section = "\n"
    variables_section += "\n".join(f"  {line}" for line in strings_list)
    
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
