import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load your dataset
df = pd.read_excel(r'C:\Users\91985\drug-discovery-analysis\src\features_debug.xlsx')

# Extract features (excluding 'pdb_id')
features = df.drop(columns=['pdb_id'])

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform PCA again to get the loadings
n_components = 14
pca = PCA(n_components=n_components)
pca.fit(scaled_features)

# Get the loadings
loadings = pca.components_

# Create a DataFrame for loadings
loadings_df = pd.DataFrame(loadings.T, columns=[f'PC{i+1}' for i in range(n_components)], index=features.columns)

# Save the full loadings to an Excel file
full_loadings_path = r'C:\Users\91985\drug-discovery-analysis\src\full_loadings.xlsx'
loadings_df.to_excel(full_loadings_path, sheet_name='Full_Loadings')

# To focus on the first 7 components, subset the DataFrame
loadings_first_7 = loadings_df.iloc[:, :7]

# Save the first 7 loadings to a separate Excel file
first_7_loadings_path = r'C:\Users\91985\drug-discovery-analysis\src\first_7_loadings.xlsx'
loadings_first_7.to_excel(first_7_loadings_path, sheet_name='First_7_Loadings')

print(f"Full loadings saved to {full_loadings_path}")
print(f"First 7 components' loadings saved to {first_7_loadings_path}")
