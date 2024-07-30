import pandas as pd
import json

# Load JSON data
with open('output.json', 'r') as file:
    data = json.load(file)

# Initialize lists to store data
pdb_ids = []
ligand_coords = []
pocket_coords = []

# Extract data from JSON
for pdb_id, values in data.items():
    pdb_ids.append(pdb_id)
    ligand_coords.append(values['ligand_coordinates'])
    pocket_coords.append(values['pocket_coordinates'])

# Create DataFrame
df = pd.DataFrame({
    'PDB_ID': pdb_ids,
    'Ligand_Coordinates': ligand_coords,
    'Pocket_Coordinates': pocket_coords
})

# Check for duplicate or null entries
if df['PDB_ID'].duplicated().any():
    print("Warning: There are duplicate PDB IDs in the dataset.")
else:
    print("No duplicate PDB IDs found.")

# Ensure there are no missing values
if df.isnull().values.any():
    print("Warning: There are missing values in the dataset.")
else:
    print("No missing values found.")

# Inspect the DataFrame
print(df.head())
print(df.info())

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

# Verify the number of rows written to each file
csv_df = pd.read_csv('output.csv')
excel_df = pd.read_excel('output.xlsx')

print(f"Number of rows in CSV file: {len(csv_df)}")
print(f"Number of rows in Excel file: {len(excel_df)}")
print(f"Expected number of complexes: {len(df)}")

# Debug: Save JSON data directly to CSV to check for hidden issues
with open('direct_output.csv', 'w') as file:
    for pdb_id, values in data.items():
        ligand_coordinates = values['ligand_coordinates']
        pocket_coordinates = values['pocket_coordinates']
        file.write(f"{pdb_id},{ligand_coordinates},{pocket_coordinates}\n")

# Verify the number of rows written to the direct CSV file
direct_csv_df = pd.read_csv('direct_output.csv', header=None)

print(f"Number of rows in direct CSV file: {len(direct_csv_df)}")
print(f"Expected number of complexes: {len(data)}")
