import pandas as pd

# Read the TSV file
df = pd.read_csv('reelMensuel.txt', sep='\t')

# Ensure 'localisation' is treated as a string (text)
df['localisation'] = df['localisation'].astype(str)

# Convert 'datedebutmois' to datetime format
df['datedebutmois'] = pd.to_datetime(df['datedebutmois'])

# Apply absolute value to 'montantreel' and round to 2 decimal places
df['montantreel'] = df['montantreel'].abs().round(2)

# Filter out rows where 'categoriecode' is empty or NaN
df = df[df['categoriecode'].notna() & (df['categoriecode'] != '')]

# Filter the data for the year 2010
df_2010 = df[df['datedebutmois'].dt.year == 2010]

# Sort the data by the specified columns
df_2010 = df_2010.sort_values(by=['datedebutmois', 'localisation', 'typecomptectb_centrecoutcode', 'atelierbtid', 'categoriecode'])

# Write the filtered and sorted data to a CSV file
df_2010.to_csv('data_ref_2010.csv', index=False)
