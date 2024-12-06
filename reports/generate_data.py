import pandas as pd
import numpy as np

def process_reel(year, df_input, reel_file_template):
    # Create a copy of the dataframe to avoid modifying the original
    df_year = df_input.copy()

    # Replace the year in 'datedebutmois' with the current year
    df_year['datedebutmois'] = df_year['datedebutmois'].apply(lambda x: x.replace(year=year))

    # Ensure 'localisation' is treated as text and format it as a 5-digit string
    df_year['localisation'] = df_year['localisation'].apply(lambda x: str(int(x)).zfill(5))

    # Add a 'reel' column based on 'montantreel' with random variation for each year
    variation_factor = (year - 2020) * 0.2  # Increasing factor for each year
    df_year['reel'] = df_year['montantreel'] + np.random.uniform(-variation_factor, variation_factor, size=len(df_year)) * df_year['montantreel']

    # Round 'reel' to 2 decimals
    df_year['reel'] = df_year['reel'].round(2)

    # Drop 'montantreel' column before output
    df_year = df_year.drop(columns=['montantreel'])

    # Generate the filename for the specific year
    year_file = reel_file_template.format(year=year)

    # Write the output CSV file for the specific year
    df_year.to_csv(year_file, index=False)


def process_budget(reel_file_template, budget_file_template):
    # Iterate over all the yearly reel files
    for year in range(2020, 2025):
        # Read the corresponding reel file
        reel_file = reel_file_template.format(year=year)
        df_reel = pd.read_csv(reel_file)

        # Ensure 'localisation' is treated as text and format it as a 5-digit string
        df_reel['localisation'] = df_reel['localisation'].apply(lambda x: str(int(x)).zfill(5))

        # Convert 'datedebutmois' to datetime format
        df_reel['datedebutmois'] = pd.to_datetime(df_reel['datedebutmois'])

        # Sort data by 'datedebutmois' to ensure correct ordering for the moving average calculation
        df_reel = df_reel.sort_values(by='datedebutmois')

        # Copy entries of the first 3 months of the current year and replace year with the next year
        df_year_first3months = df_reel[(df_reel['datedebutmois'].dt.month <= 3)].copy()

        # Replace the year with year + 1 for these entries
        df_year_first3months['datedebutmois'] = df_year_first3months['datedebutmois'].apply(lambda x: x.replace(year=x.year + 1))

        # Append these modified entries to the original dataframe
        df_reel = pd.concat([df_reel, df_year_first3months], ignore_index=True)

        # Calculate a 30-month moving average for the 'reel' column
        df_reel['budget'] = df_reel['reel'].rolling(window=30, min_periods=1).mean()

        # Replace NaN values in the 'budget' column with the values from the 'reel' column
        df_reel['budget'] = df_reel['budget'].fillna(df_reel['reel'])

        # Round 'budget' to 2 decimals
        df_reel['budget'] = df_reel['budget'].round(2)

        # Add a 'prevision' column based on a random variation around the 'budget' value
        variation_factor_prevision = 0.2  # 20% variation for 'prevision'
        df_reel['prevision'] = df_reel['budget'] + np.random.uniform(-variation_factor_prevision, variation_factor_prevision, size=len(df_reel)) * df_reel['budget']

        # Round 'prevision' to 2 decimals
        df_reel['prevision'] = df_reel['prevision'].round(2)

        # Drop 'reel' column before output
        df_reel = df_reel.drop(columns=['reel'])

        # Generate the filename for the specific year
        budget_file = budget_file_template.format(year=year)

        # Write the output CSV file for the specific year
        df_reel.to_csv(budget_file, index=False)


# Main script to process data for each year
def main():
    reference_file = 'data_ref_2010.csv'  # Reference file is 'reel_2010.csv'
    reel_file_template = 'reel_{year}.csv'  # Template for yearly reel files
    budget_file_template = 'budget_{year}.csv'  # Template for yearly budget files

    # Read the reference CSV file once
    df_input = pd.read_csv(reference_file)

    # Convert 'datedebutmois' to datetime format if needed
    df_input['datedebutmois'] = pd.to_datetime(df_input['datedebutmois'])

    # Loop through each year and call the process_reel function to generate the 'reel' data
    for year in range(2020, 2025):
        process_reel(year, df_input, reel_file_template)

    # After generating the reel files, process the budgets for all years
    process_budget(reel_file_template, budget_file_template)


if __name__ == "__main__":
    main()
