def format_string(template, **kwargs):
    """Formats a given template with the provided keyword arguments."""
    return template.format(**kwargs)

# Define templates
templates_mesures = {
    "template_date": '{name} = {valeur}',  
}
templates_affichage = {
    "template_titre": '{name} = {prompt}',  
}

# Data for measures
data_mesures = [
    {
        "name": "Date Courante",
        "valeur": 'FORMAT(TODAY(), "dd mmm yyyy", "fr-FR")',
        "template": templates_mesures["template_date"]
    },
    {
        "name": "Mois Courant",
        "valeur": 'FORMAT(TODAY(), "mmm yyyy", "fr-FR")',
        "template": templates_mesures["template_date"]
    },
    {
        "name": "Date Premier Jour AF",
        "valeur": 'FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1)), "dd mmm yyyy", "fr-FR")',
        "template": templates_mesures["template_date"]
    },
    {
        "name": "Date Dernier Jour AF",
        "valeur": 'FORMAT(IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 3, 31), DATE(YEAR(TODAY()) - 1, 3, 31)), "dd mmm yyyy", "fr-FR")',
        "template": templates_mesures["template_date"]
    },
]
				
# Data for affichage
data_affichage = [
    {
        "name": "Suivi cumulatif titre",
        "prompt": '"Suivi cumulatif du " & [Date Premier Jour AF] & " au " & [Date Dernier Jour AF]',
        "template": templates_affichage["template_titre"]
    },
    {
        "name": "Suivi mois titre",
        "prompt": '"Suivi pour le mois en cours (" & [Mois Courant] & ")"',
        "template": templates_affichage["template_titre"]
    },
    {
        "name": "Réel AEC titre",
        "prompt": 'Réel AEC',
        "template": templates_affichage["template_titre"]
    },
    {
        "name": "vs 1 an titre",
        "prompt": 'Δ 1 an',
        "template": templates_affichage["template_titre"]
    },
    {
        "name": "vs Budget titre",
        "prompt": 'vs Budget',
        "template": templates_affichage["template_titre"]
    },
    {
        "name": "vs Prévision titre",
        "prompt": 'vs Prévision',
        "template": templates_affichage["template_titre"]
    },
]


# Generate and print formatted strings for measures
for item in data_mesures:
    template = item.pop("template")
    formatted_string = format_string(template, **item)
    print(formatted_string)

# Generate and print formatted strings for affichage
for item in data_affichage:
    template = item.pop("template")
    formatted_string = format_string(template, **item)
    print(formatted_string)
