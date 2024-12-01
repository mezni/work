import csv
import random
from datetime import datetime

# Define the start and end years
start_year = 2020  # Adjust as needed
end_year = 2025    # Adjust as needed

# Get the current year and month for comparison
current_year = datetime.now().year
current_month = datetime.now().month

# Create a list to hold the data
data = []

# Generate data with an additional loop for unitadm
for unitadm in range(2):
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            financial_year_start = year if month >= 4 else year - 1
            financial_year_end = financial_year_start + 1
            financial_year_str = f"{str(financial_year_start)[-2:]}{str(financial_year_end)[-2:]}"
            
            # Set MontantTrx to 0 if month > current_month and year > current_year
            if (year > current_year) or (year == current_year and month > current_month):
                montant_trx = 0
            else:
                # Otherwise, generate a random number between 100 and 1000
                montant_trx = random.randint(100, 1000)
            
            # Add the data to the list
            data.append([unitadm + 1, year, month, financial_year_str, montant_trx])

# Sort the data by year, month, and then unitadm
data.sort(key=lambda x: (x[1], x[2], x[0]))

# Write data to a CSV file
file_name = "transactions.csv"
with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write the header in French, including the new column "MontantTrx"
    writer.writerow(["UniteAdm", "Annee", "Mois", "AnneeFinanciere", "MontantTrx"])
    # Write the sorted data rows
    writer.writerows(data)

print(f"CSV file '{file_name}' has been created successfully!")
