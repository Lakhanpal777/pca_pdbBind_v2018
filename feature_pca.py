import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the data from an Excel file
df = pd.read_excel(r'C:\Users\91985\drug-discovery-analysis\src\output_dataframed.xlsx')

# Function to safely parse JSON strings
def safe_json_loads(s):
    try:
        # Fix invalid JSON format
        s = s.replace("[[", "[{\"type\":\"point\",\"coords\":[").replace("]]", "]}]").replace("], [", "]}, {\"type\":\"point\",\"coords\":[")
        parsed_json = json.loads(s)
        return [item['coords'] for item in parsed_json] if isinstance(parsed_json, list) else []
    except json.JSONDecodeError:
        print(f"Invalid JSON: {s}")
        return []

# Function to extract basic statistics from coordinates
def extract_features(coord_list):
    if len(coord_list) == 0:
        return [0, 0, 0, 0, 0, 0, 0]  # Return zeros if the list is empty
    coords = np.array(coord_list)
    return [
        len(coords),  # Number of coordinates
        np.mean(coords[:, 0]),  # Mean X
        np.mean(coords[:, 1]),  # Mean Y
        np.mean(coords[:, 2]),  # Mean Z
        np.std(coords[:, 0]),  # Std X
        np.std(coords[:, 1]),  # Std Y
        np.std(coords[:, 2])   # Std Z
    ]

# Apply the safe JSON parsing to the ligand and pocket coordinates
df['Ligand_Coordinates'] = df['Ligand_Coordinates'].apply(safe_json_loads)
df['Pocket_Coordinates'] = df['Pocket_Coordinates'].apply(safe_json_loads)

# Apply the feature extraction to the ligand and pocket coordinates
df['Ligand_Features'] = df['Ligand_Coordinates'].apply(extract_features)
df['Pocket_Features'] = df['Pocket_Coordinates'].apply(extract_features)

# Convert lists of features into DataFrames
ligand_features = pd.DataFrame(df['Ligand_Features'].tolist(), columns=['Num_Ligand_Coords', 'Ligand_Mean_X', 'Ligand_Mean_Y', 'Ligand_Mean_Z', 'Ligand_Std_X', 'Ligand_Std_Y', 'Ligand_Std_Z'])
pocket_features = pd.DataFrame(df['Pocket_Features'].tolist(), columns=['Num_Pocket_Coords', 'Pocket_Mean_X', 'Pocket_Mean_Y', 'Pocket_Mean_Z', 'Pocket_Std_X', 'Pocket_Std_Y', 'Pocket_Std_Z'])

# Combine features into a single DataFrame
features = pd.concat([ligand_features, pocket_features], axis=1)

# Check for rows with NaN or infinite values and remove them
features.replace([np.inf, -np.inf], np.nan, inplace=True)
features.dropna(inplace=True)

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_features)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Plot the PCA result
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Ligand and Pocket Features')
plt.show()

# Scree plot to show the explained variance
explained_variance = pca.explained_variance_ratio_

plt.figure(figsize=(8, 6))
plt.bar(range(1, len(explained_variance) + 1), explained_variance, alpha=0.7)
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.title('Scree Plot')
plt.show()
