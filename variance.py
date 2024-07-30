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
pca = PCA()
pca.fit(scaled_features)

# Explained variance ratio
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Plot explained variance ratio
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--', color='b')
plt.ylabel('Explained Variance Ratio')
plt.xlabel('Principal Components')
plt.title('Explained Variance Ratio by Principal Component')
plt.xticks(range(1, len(explained_variance) + 1))
plt.grid(True)
plt.show()

# Plot cumulative explained variance
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--', color='g')
plt.ylabel('Cumulative Explained Variance')
plt.xlabel('Principal Components')
plt.title('Cumulative Explained Variance Plot')
plt.xticks(range(1, len(cumulative_variance) + 1))
plt.grid(True)
plt.show()
