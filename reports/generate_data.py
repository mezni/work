import pandas as pd
import numpy as np

def process_reel(year, df_input, reel_file):
    # Create a copy of the dataframe to avoid modifying the original
    df_year = df_input.copy()

    # Replace the year in 'datedebutmois' with the current year
    df_year['datedebutmois'] = df_year['datedebutmois'].apply(lambda x: x.replace(year=year))

    # Ensure 'localisation' is treated as a string and format it as a 5-digit string (e.g., '00350')
    df_year['localisation'] = df_year['localisation'].apply(lambda x: str(int(x)).zfill(5))

    # Add a 'reel' column based on 'montantreel' with random variation for each year
    variation_factor = (year - 2020) * 0.2  # Increasing factor for each year
    df_year['reel'] = df_year['montantreel'] + np.random.uniform(-variation_factor, variation_factor, size=len(df_year)) * df_year['montantreel']

    # Drop 'montantreel' column before output
    df_year = df_year.drop(columns=['montantreel'])

    # Open the output CSV file in append mode
    with open(reel_file, 'a', newline='') as f:
        df_year.to_csv(f, header=f.tell() == 0, index=False)  # Write header only if file is empty


def process_budget(year, reel_file, budget_file):
    # Read the data from the reel file after it is generated
    df_reel = pd.read_csv(reel_file)

    # Ensure 'localisation' is treated as text (string) and format it as a 5-digit string (e.g., '00350')
    df_reel['localisation'] = df_reel['localisation'].apply(lambda x: str(int(x)).zfill(5))

    # Convert 'datedebutmois' to datetime format
    df_reel['datedebutmois'] = pd.to_datetime(df_reel['datedebutmois'])

    # Sort data by 'datedebutmois' to ensure correct ordering for the moving average calculation
    df_reel = df_reel.sort_values(by='datedebutmois')

    # Copy entries of the first 3 months of 2024 and replace year with 2025
    df_2024_first3months = df_reel[(df_reel['datedebutmois'].dt.year == 2024) & (df_reel['datedebutmois'].dt.month <= 3)].copy()

    # Replace the year 2024 with 2025 for these entries
    df_2024_first3months['datedebutmois'] = df_2024_first3months['datedebutmois'].apply(lambda x: x.replace(year=2025))

    # Append these modified entries to the original dataframe
    df_reel = pd.concat([df_reel, df_2024_first3months], ignore_index=True)

    # Calculate a 30-month moving average for the 'reel' column (no modification to reel here)
    df_reel['budget'] = df_reel['reel'].rolling(window=30, min_periods=1).mean()  # Use 'reel' for budget calculation

    # Replace NaN values in the 'budget' column with the values from the 'reel' column
    df_reel['budget'] = df_reel['budget'].fillna(df_reel['reel'])

    # Round 'budget' to 2 decimals
    df_reel['budget'] = df_reel['budget'].round(2)

    # Add a 'prevision' column based on a random variation around the 'budget' value
    variation_factor_prevision = 0.2  # 20% variation for 'prevision'
    df_reel['prevision'] = df_reel['budget'] + np.random.uniform(-variation_factor_prevision, variation_factor_prevision, size=len(df_reel)) * df_reel['budget']

    # Round 'prevision' to 2 decimals
    df_reel['prevision'] = df_reel['prevision'].round(2)

    # Drop 'montantreel' and 'reel' columns before output
    df_reel = df_reel.drop(columns=['reel'])

    # Open the output CSV file in append mode
    with open(budget_file, 'a', newline='') as f:
        df_reel.to_csv(f, header=f.tell() == 0, index=False)  # Write header only if file is empty


# Main script to process data for each year
def main():
    reference_file = 'data_ref_2010.csv'  # Reference file is 'reel_2010.csv'
    reel_file = 'reel.csv'  # Output file name is 'reel.csv'
    budget_file = 'budget.csv'  # Output file for budget

    # Read the reference CSV file once
    df_input = pd.read_csv(reference_file)

    # Convert 'datedebutmois' to datetime format if needed
    df_input['datedebutmois'] = pd.to_datetime(df_input['datedebutmois'])

    # Loop through each year and call the process_reel function to generate the 'reel' data
    for year in [2020, 2021, 2022, 2023, 2024]:
        process_reel(year, df_input, reel_file)

    # After generating the reel file, process the budget
    process_budget(2024, reel_file, budget_file)

if __name__ == "__main__":
    main()
