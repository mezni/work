import pandas as pd
import numpy as np
from datetime import datetime

# Parameters for financial transactions
start_date = "2020-04-01"
end_date = "2026-03-31"
cost_centers = {
    "Quebec": 200000,       # Base transaction value for Quebec
    "Montreal": 100000,     # Base transaction value for Montreal
    "Trois-Rivières": 50000 # Base transaction value for Trois-Rivières
}

# Assign unique IDs to cost centers
cost_center_ids = {
    "Quebec": 1,
    "Montreal": 2,
    "Trois-Rivières": 3
}

# Generate date range for months
dates = pd.date_range(start=start_date, end=end_date, freq='M')

# Get the current date
current_date = datetime.today()

# Initialize empty lists to store data for financial transactions and previsions
data = []
previsions_data = []
budget_data = []

# Generate financial transaction data and previsions data for each cost center
for cost_center, base_value in cost_centers.items():
    # Smooth trend: linear growth + seasonality for MontantTrx
    trend = np.linspace(base_value * 0.8, base_value * 1.2, len(dates))  # Growth trend around the base value
    seasonality = (base_value * 0.1) * np.sin(np.linspace(0, 4 * np.pi, len(dates)))  # Seasonal variation
    noise = np.random.normal(0, base_value * 0.05, len(dates))  # Random noise
    
    # Calculate MontantTrx
    transactions = trend + seasonality + noise
    transactions = np.clip(transactions, 0, None)  # Ensure no negative values
    
    # Adjust MontantTrx for the current month
    for i, date in enumerate(dates):
        # If the month is the current month and the year is the current year
        if date.year == current_date.year and date.month == current_date.month:
            # Number of days in the current month up to today
            # Correctly calculate days in the current month
            if current_date.month == 12:
                # If it's December, next month is January of the next year
                next_month = 1
                next_month_year = current_date.year + 1
            else:
                next_month = current_date.month + 1
                next_month_year = current_date.year

            # Get the number of days in the current month
            days_in_month = (datetime(next_month_year, next_month, 1) - datetime(current_date.year, current_date.month, 1)).days
            days_passed = current_date.day
            # Adjust MontantTrx based on the days passed in the current month
            transactions[i] /= days_in_month / days_passed
        # If the month is after the current month, set MontantTrx to 0
        elif date.year > current_date.year or (date.year == current_date.year and date.month > current_date.month):
            transactions[i] = 0

    # For Montantprevisions, use a different trend
    provision_trend = np.linspace(base_value * 0.5, base_value * 1.5, len(dates))  # Different linear trend for previsions
    provision_seasonality = (base_value * 0.15) * np.sin(np.linspace(0, 3 * np.pi, len(dates)))  # Different seasonal effect
    provision_noise = np.random.normal(0, base_value * 0.1, len(dates))  # Different noise level
    
    # Calculate Montantprevisions
    previsions = provision_trend + provision_seasonality + provision_noise
    previsions = np.clip(previsions, 0, None)  # Ensure no negative values
    
    # Append data for each month
    for i, date in enumerate(dates):
        # Determine financial year
        if date.month < 4:  # January to March
            fy_start = date.year - 1
            fy_end = date.year
        else:  # April to December
            fy_start = date.year
            fy_end = date.year + 1
        
        financial_year = f"{str(fy_start)[-2:]}{str(fy_end)[-2:]}"
        
        # Add transaction data
        data.append({
            "UniteAdmID": cost_center_ids[cost_center],  # Cost Center ID
            "Annee": date.year,                         # Year
            "Mois": date.month,                        # Month
            "DateDebut": date.to_period('M').start_time,  # First Date of Month
            "AnneeFinanciere": financial_year,          # Financial Year
            "MontantTrx": int(transactions[i])      # Transaction Amount
        })
        
        # Add prevision data with the calculated Montantprevisions
        previsions_data.append({
            "UniteAdmID": cost_center_ids[cost_center],  # Cost Center ID
            "Annee": date.year,                         # Year
            "Mois": date.month,                        # Month
            "DateDebut": date.to_period('M').start_time,  # First Date of Month
            "AnneeFinanciere": financial_year,          # Financial Year
            "Montantprevisions": round(previsions[i])  # Previsions with the new trend
        })
        
        # Calculate MontantBudget for each month (base value multiplied by a random variation)
        base_monthly_budget = base_value  # Base monthly value (one month's worth)
        random_variation = np.random.uniform(0.95, 1.05)  # Random fluctuation between 95% and 105%
        montant_monthly_budget = base_monthly_budget * random_variation
        
        # Round the MontantBudget to the nearest thousand
        montant_monthly_budget_rounded = round(montant_monthly_budget / 1000) * 1000  # Rounds to nearest 1000
        
        # Add monthly budget data
        budget_data.append({
            "UniteAdmID": cost_center_ids[cost_center],
            "AnneeFinanciere": financial_year,
            "DateDebut": date.replace(day=1),  # Use the first day of the month as the start date
            "MontantBudget": montant_monthly_budget_rounded  # Monthly budget
        })

# Create DataFrame for transactions
df_transactions = pd.DataFrame(data)

# Sort the DataFrame by DateDebut (First Date of Month) and UniteAdmID (Cost Center ID)
df_transactions = df_transactions.sort_values(by=["DateDebut", "UniteAdmID"])

# Save the financial transactions to a CSV file
output_file = "transactions.csv"
df_transactions.to_csv(output_file, index=False)

# Create DataFrame for previsions
df_previsions = pd.DataFrame(previsions_data)

# Sort the DataFrame by DateDebut (First Date of Month) and UniteAdmID (Cost Center ID)
df_previsions = df_previsions.sort_values(by=["DateDebut", "UniteAdmID"])

# Save the previsions data to a CSV file
previsions_output_file = "previsions.csv"
df_previsions.to_csv(previsions_output_file, index=False)

# Prepare the data for UniteAdm and UniteAdmID (separate CSV)
uniteadm_data = [
    {"UniteAdmID": cost_center_ids[cost_center], "UniteAdm": cost_center}
    for cost_center in cost_centers
]

# Create a DataFrame for the UniteAdm and UniteAdmID data
df_uniteadm = pd.DataFrame(uniteadm_data)

# Save the UniteAdm and UniteAdmID data to a CSV file
uniteadm_output_file = "uniteadms.csv"
df_uniteadm.to_csv(uniteadm_output_file, index=False)

# Create DataFrame for Budgets data
df_budgets = pd.DataFrame(budget_data)

# Sort the DataFrame by DateDebut (First Date of Month) and UniteAdmID (Cost Center ID)
df_budgets = df_budgets.sort_values(by=["DateDebut", "UniteAdmID"])

# Save the Budgets data to a CSV file
budgets_output_file = "budgets.csv"
df_budgets.to_csv(budgets_output_file, index=False)

# Output paths
print(f"Financial transactions CSV saved at: {output_file}")
print(f"Previsions CSV saved at: {previsions_output_file}")
print(f"UniteAdmID and UniteAdm CSV saved at: {uniteadm_output_file}")
print(f"Budgets CSV saved at: {budgets_output_file}")
