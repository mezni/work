def format_string(template, **kwargs):
    """Formats a given template with the provided keyword arguments."""
    return template.format(**kwargs)

# Define the templates as a dictionary for easier access
templates_affichage = {
    "template_titre": '{name} = "{prompt}"',
    "template_test": '{name} = "{xxxx} test"'
}

# Placeholder data for each entry
data_affichage = [
    {"name": "vs 1 an titre", "prompt": "Δ 1 an", "template": templates_affichage["template_titre"]},
    {"name": "vs Budget titre", "prompt": "vs Budget", "template": templates_affichage["template_titre"]},
    {"name": "vs Prévision titre", "prompt": "vs Prévision", "template": templates_affichage["template_titre"]},
    {"name": "test", "xxxx": "vs Prévision", "template": templates_affichage["template_test"]}
]

# Generate and print formatted strings
for item in data_affichage:
    template = item.pop("template")
    formatted_string = format_string(template, **item)
    print(formatted_string)
