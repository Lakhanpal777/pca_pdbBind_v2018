import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the data from the Excel file
df = pd.read_excel('features_debug.xlsx')

# Extract the features from the DataFrame
features = df[['Num_Ligand_Coords', 'Ligand_Mean_X', 'Ligand_Mean_Y', 'Ligand_Mean_Z',
               'Ligand_Std_X', 'Ligand_Std_Y', 'Ligand_Std_Z',
               'Num_Pocket_Coords', 'Pocket_Mean_X', 'Pocket_Mean_Y',
               'Pocket_Mean_Z', 'Pocket_Std_X', 'Pocket_Std_Y', 'Pocket_Std_Z']]

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
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--')
plt.ylabel('Explained Variance Ratio')
plt.xlabel('Principal Components')
plt.title('Scree Plot')
plt.xticks(range(1, len(explained_variance) + 1))
plt.show()
