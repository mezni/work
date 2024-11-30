import csv
import random
from datetime import datetime, timedelta

def generate_dates(start_date, end_date):
    current_date = start_date.replace(day=1)  # Start from the first day of the month
    results = []

    while current_date <= end_date:
        year_curr=str(current_date.year)[-2:]
        year_prev=str(current_date.year-1)[-2:]
        year_next=str(current_date.year+1)[-2:]
        if current_date.month >= 4:  
            financial_year = f"{year_curr}{year_next}"
        else: 
            financial_year = f"{year_prev}{year_curr}"
        month=str(current_date.month)
        
        results.append({"financial_year":financial_year, "month":month})
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (1 if current_date.month == 12 else 0)
        current_date = current_date.replace(year=next_year, month=next_month)
    return results


start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

dates=generate_dates(start_date,end_date)


transactions = []
for d in dates:
    transaction_financial_year = d["financial_year"]
    transaction_month = d["month"]
    transaction_amount = random.randint(0, 1000)  
    transactions.append([transaction_financial_year,transaction_month,transaction_amount])

filename="transactions.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Financial Year", "Financial Month", "Transaction Sum"])
    writer.writerows(transactions)