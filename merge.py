import os
import re
import pandas as pd

# Step 1: Parse the INDEX_general_PL_data.2018 file to get binding affinities and PDB IDs
binding_affinity_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\index\INDEX_refined_data.2018"
binding_affinity_data = []

with open(binding_affinity_file_path, 'r') as file:
    for line in file:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = re.split(r'\s+', line.strip())
        pdb_id = parts[0]
        binding_affinity = parts[3]
        binding_affinity_data.append({"PDB_ID": pdb_id, "Binding_Affinity": binding_affinity})

binding_affinity_df = pd.DataFrame(binding_affinity_data)
print("Binding Affinity DataFrame:")
print(binding_affinity_df.head())

# Step 2: Parse the output.txt file
output_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\output.txt"
ligand_data = {}

with open(output_file_path, 'r') as file:
    current_pdb_id = None
    for line in file:
        line = line.strip()
        if line.startswith("PDB ID:"):
            current_pdb_id = line.split(":")[1].strip()
            if current_pdb_id not in ligand_data:
                ligand_data[current_pdb_id] = {"pocket_coordinates": [], "ligand_coordinates": []}
        elif "Pocket:" in line and current_pdb_id:
            ligand_data[current_pdb_id]["pocket_coordinates"].append(line.split("Pocket:")[1].strip())
        elif "Ligand:" in line and current_pdb_id:
            ligand_data[current_pdb_id]["ligand_coordinates"].append(line.split("Ligand:")[1].strip())

# Filter the ligand_data to include only those PDB IDs present in binding_affinity_df
ligand_data_filtered = {k: v for k, v in ligand_data.items() if k in binding_affinity_df["PDB_ID"].values}

# Convert lists of coordinates to a single string for each PDB ID
for pdb_id in ligand_data_filtered:
    ligand_data_filtered[pdb_id]["pocket_coordinates"] = " | ".join(ligand_data_filtered[pdb_id]["pocket_coordinates"])
    ligand_data_filtered[pdb_id]["ligand_coordinates"] = " | ".join(ligand_data_filtered[pdb_id]["ligand_coordinates"])

print("Filtered Ligand Data parsed from output.txt:")
print(ligand_data_filtered)

ligand_data_df = pd.DataFrame.from_dict(ligand_data_filtered, orient='index').reset_index().rename(columns={"index": "PDB_ID"})
print("Ligand Data DataFrame:")
print(ligand_data_df.head())

# Step 3: Merge the data
merged_df = pd.merge(ligand_data_df, binding_affinity_df, on="PDB_ID", how="inner")
print("Merged DataFrame:")
print(merged_df.head())

# Check for potential issues in the merge
if merged_df.empty:
    print("The merged DataFrame is empty. Possible reasons could be:")
    print("- Mismatch in PDB IDs between the files.")
    print("- Incorrect parsing of either the ligand or binding affinity data.")
else:
    # Step 4: Save the merged data to a CSV file
    merged_output_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\merged_data.csv"
    try:
        merged_df.to_csv(merged_output_file_path, index=False)
        print(f"Merged data has been saved to {merged_output_file_path}")
    except PermissionError:
        print(f"Permission denied: Unable to save file to {merged_output_file_path}. Please check the file permissions.")
