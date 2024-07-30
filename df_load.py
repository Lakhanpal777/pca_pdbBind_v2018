import pandas as pd

# Load the DataFrame from the Excel file
df = pd.read_excel('output_dataframed.xlsx')

# Check the loaded DataFrame
print(df.head())  # Print the first few rows
print(df.info())  # Print a summary of the DataFrame
print(df.describe())  # Print a statistical summary of the DataFrame

# Optionally, save a sample to a CSV file for visual inspection
df_sample = df.sample(10)  # Take a random sample of 10 rows
df_sample.to_csv('sample_output.csv', index=False)
