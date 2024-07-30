import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

# Load the DataFrame from the Excel file
df = pd.read_excel('output_dataframed.xlsx')

# Define a function to safely parse JSON strings
def parse_json_safe(json_str):
    try:
        return json.loads(json_str.replace("'", '"'))
    except json.JSONDecodeError:
        return []

# Calculate the number of coordinates for ligands and pockets using json.loads
df['Num_Ligand_Coords'] = df['Ligand_Coordinates'].apply(lambda x: len(parse_json_safe(x)))
df['Num_Pocket_Coords'] = df['Pocket_Coordinates'].apply(lambda x: len(parse_json_safe(x)))

# Plot the distribution of ligand coordinates
plt.figure(figsize=(10, 5))
sns.histplot(df['Num_Ligand_Coords'], bins=30, kde=True)
plt.title('Distribution of Number of Ligand Coordinates')
plt.xlabel('Number of Ligand Coordinates')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of pocket coordinates
plt.figure(figsize=(10, 5))
sns.histplot(df['Num_Pocket_Coords'], bins=30, kde=True)
plt.title('Distribution of Number of Pocket Coordinates')
plt.xlabel('Number of Pocket Coordinates')
plt.ylabel('Frequency')
plt.show()

# Plot the scatter plot of ligand vs pocket coordinates
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Num_Ligand_Coords', y='Num_Pocket_Coords', data=df)
plt.title('Scatter Plot of Number of Ligand vs Pocket Coordinates')
plt.xlabel('Number of Ligand Coordinates')
plt.ylabel('Number of Pocket Coordinates')
plt.show()

# Plot the box plot for ligand coordinates
plt.figure(figsize=(10, 5))
sns.boxplot(x=df['Num_Ligand_Coords'])
plt.title('Box Plot of Number of Ligand Coordinates')
plt.xlabel('Number of Ligand Coordinates')
plt.show()

# Plot the box plot for pocket coordinates
plt.figure(figsize=(10, 5))
sns.boxplot(x=df['Num_Pocket_Coords'])
plt.title('Box Plot of Number of Pocket Coordinates')
plt.xlabel('Number of Pocket Coordinates')
plt.show()

# Create a pair plot for the dataset
sns.pairplot(df[['Num_Ligand_Coords', 'Num_Pocket_Coords']])
plt.suptitle('Pair Plot of Ligand and Pocket Coordinates', y=1.02)
plt.show()
