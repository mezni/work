import pandas as pd
import numpy as np

# Parameters for financial transactions
start_date = "2020-01-01"
end_date = "2025-12-31"
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

# Initialize empty lists to store data for financial transactions and previsions
data = []
previsions_data = []

# Generate financial transaction data and previsions data for each cost center
for cost_center, base_value in cost_centers.items():
    # Smooth trend: linear growth + seasonality for MontantTrx
    trend = np.linspace(base_value * 0.8, base_value * 1.2, len(dates))  # Growth trend around the base value
    seasonality = (base_value * 0.1) * np.sin(np.linspace(0, 4 * np.pi, len(dates)))  # Seasonal variation
    noise = np.random.normal(0, base_value * 0.05, len(dates))  # Random noise
    
    # Calculate MontantTrx
    transactions = trend + seasonality + noise
    transactions = np.clip(transactions, 0, None)  # Ensure no negative values
    
    # For Montantprevisions, use a different trend
    provision_trend = np.linspace(base_value * 0.5, base_value * 1.5, len(dates))  # Different linear trend for previsions
    provision_seasonality = (base_value * 0.15) * np.sin(np.linspace(0, 3 * np.pi, len(dates)))  # Different seasonal effect
    provision_noise = np.random.normal(0, base_value * 0.1, len(dates))  # Different noise level
    
    # Calculate Montantprevisions
    previsions = provision_trend + provision_seasonality + provision_noise
    previsions = np.clip(previsions, 0, None)  # Ensure no negative values
    
    # Append data for each month
    for date, total_transactions, total_previsions in zip(dates, transactions, previsions):
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
            "MontantTrx": int(total_transactions)      # Transaction Amount
        })
        
        # Add prevision data with the calculated Montantprevisions
        previsions_data.append({
            "UniteAdmID": cost_center_ids[cost_center],  # Cost Center ID
            "Annee": date.year,                         # Year
            "Mois": date.month,                        # Month
            "DateDebut": date.to_period('M').start_time,  # First Date of Month
            "AnneeFinanciere": financial_year,          # Financial Year
            "Montantprevisions": round(total_previsions)  # previsions with the new trend
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

# Prepare the data for Budgets (UniteAdmID, AnneeFinanciere, Financial Year Start Date, and MontantBudget)
budget_data = []

for cost_center, base_value in cost_centers.items():
    for year in range(2020, 2026):  # Iterate over the financial years in the range
        if year < 2023:  # For years before 2023, the financial year is the previous one
            fy_start = year - 1
            fy_end = year
        else:  # For years from 2023 onwards, the financial year starts in April
            fy_start = year
            fy_end = year + 1
        
        financial_year = f"{str(fy_start)[-2:]}{str(fy_end)[-2:]}"
        fy_start_date = pd.Timestamp(f"{fy_start}-04-01")  # April 1st of the start year
        
        # Calculate the budget with slight variation
        base_budget = base_value * 12  # Monthly base value multiplied by 12 months
        random_variation = np.random.uniform(0.95, 1.05)  # Random fluctuation between 95% and 105%
        montant_budget = base_budget * random_variation
        
        # Round the MontantBudget to the nearest thousand
        montant_budget_rounded = round(montant_budget / 1000) * 1000  # Rounds to nearest 1000
        
        budget_data.append({
            "UniteAdmID": cost_center_ids[cost_center],
            "AnneeFinanciere": financial_year,
            "DateDebut": fy_start_date,
            "MontantBudget": montant_budget_rounded  # Use the rounded value
        })

# Create a DataFrame for the Budgets data
df_budgets = pd.DataFrame(budget_data)
df_budgets = df_budgets.sort_values(by=["DateDebut", "UniteAdmID"])

# Save the Budgets data to a CSV file
budgets_output_file = "budgets.csv"
df_budgets.to_csv(budgets_output_file, index=False)

# Output paths
print(f"Financial transactions CSV saved at: {output_file}")
print(f"Previsions CSV saved at: {previsions_output_file}")
print(f"UniteAdmID and UniteAdm CSV saved at: {uniteadm_output_file}")
print(f"Budgets CSV saved at: {budgets_output_file}")


print(f"Budgets CSV saved at: {budgets_output_file}")