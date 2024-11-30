import csv
import random
from datetime import datetime, timedelta

def generate_dates(start_date, end_date):
    current_date = start_date.replace(day=1)  # Start from the first day of the month
    results = []

    while current_date <= end_date:
        year_curr = str(current_date.year)[-2:]
        year_prev = str(current_date.year - 1)[-2:]
        year_next = str(current_date.year + 1)[-2:]

        # Determine financial year
        if current_date.month >= 4:
            financial_year = f"{year_curr}{year_next}"
        else:
            financial_year = f"{year_prev}{year_curr}"
        
        month = f"{current_date.month:02d}"  # Format month as 2 digits
        results.append({"financial_year": financial_year, "month": month})

        # Move to the next month
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (1 if current_date.month == 12 else 0)
        current_date = current_date.replace(year=next_year, month=next_month)

    return results

def generate_transactions(dates, current_fy, current_month, filename):
    transactions = []

    # Convert current_fy and current_month to integers for comparison
    current_fy_int = int(current_fy)
    current_month_int = int(current_month)

    for unite_adm in range(2):  # Two administrative units
        for d in dates:
            transaction_financial_year = d["financial_year"]
            transaction_month = d["month"]

            # Convert financial year and month to integers for proper comparison
            transaction_fy_int = int(transaction_financial_year)
            transaction_month_int = int(transaction_month)

            transaction_amount = 0

            # Generate transaction amount based on financial year and month
            if current_fy_int > transaction_fy_int or (current_fy_int == transaction_fy_int and current_month_int >= transaction_month_int):
                transaction_amount = random.randint(0, 1000)

            transactions.append([transaction_financial_year, transaction_month, unite_adm + 1, transaction_amount])

    # Sort the transactions by "AnneeFinanciere", "MoisFinancier", and "UniteAdm"
    transactions_sorted = sorted(transactions, key=lambda x: (x[0], x[1], x[2]))

    # Write sorted transactions to CSV
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["AnneeFinanciere", "MoisFinancier", "UniteAdm", "SommeTransactions"])
        writer.writerows(transactions_sorted)

# Current date and financial year calculation
current_date = datetime.now().date()
if current_date.month >= 4:
    current_fy = f"{str(current_date.year)[-2:]}{str(current_date.year + 1)[-2:]}"
else:
    current_fy = f"{str(current_date.year - 1)[-2:]}{str(current_date.year)[-2:]}"
current_month = str(current_date.month)

# Generate dates and transactions
start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 12, 31)
dates = generate_dates(start_date, end_date)
filename = "transactions.csv"
generate_transactions(dates, current_fy, current_month, filename)

print(f"CSV file '{filename}' generated successfully.")
