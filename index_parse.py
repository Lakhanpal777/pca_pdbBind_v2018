import os
import re
import pandas as pd

def parse_binding_affinity(binding_affinity_str):
    """
    Parse the binding affinity value from the given string.
    Handles formats like Ki=400mM, IC50=355mM, etc.
    """
    match = re.search(r'([-+]?\d*\.\d+|\d+)\s*(mM|uM|nM|pM)?', binding_affinity_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        
        if unit == 'uM':
            value /= 1000  # Convert from microMolar to milliMolar
        elif unit == 'nM':
            value /= 1e6  # Convert from nanoMolar to milliMolar
        elif unit == 'pM':
            value /= 1e9  # Convert from picoMolar to milliMolar
        
        return value
    return None

def load_binding_affinity(index_file_path):
    affinity_data = []
    with open(index_file_path, 'r') as file:
        for line in file:
            if not line.startswith("#"):  # Skip comment lines
                parts = re.split(r'\s+', line.strip())
                pdb_id = parts[0]
                binding_affinity_str = parts[4]
                binding_affinity = parse_binding_affinity(binding_affinity_str)
                if binding_affinity is not None:
                    affinity_data.append({'pdb_id': pdb_id, 'binding_affinity': binding_affinity})
    return pd.DataFrame(affinity_data)

def load_coordinates(file_path):
    ligand_data = []
    with open(file_path, 'r') as file:
        current_pdb_id = None
        for line in file:
            line = line.strip()
            if line.startswith("PDB ID:"):
                current_pdb_id = line.split(":")[1].strip()
                print(f"Parsing PDB ID: {current_pdb_id}")  # Debug print
            elif "Pocket Coordinates:" in line and current_pdb_id:
                pocket_coords = line.split("Pocket Coordinates:")[1].strip()
                print(f"Pocket coordinates for {current_pdb_id}: {pocket_coords[:100]}...")  # Debug print
                ligand_data.append({"pdb_id": current_pdb_id, "type": "Pocket", "coordinates": pocket_coords})
            elif "Ligand Coordinates:" in line and current_pdb_id:
                ligand_coords = line.split("Ligand Coordinates:")[1].strip()
                print(f"Ligand coordinates for {current_pdb_id}: {ligand_coords[:100]}...")  # Debug print
                ligand_data.append({"pdb_id": current_pdb_id, "type": "Ligand", "coordinates": ligand_coords})
    return pd.DataFrame(ligand_data)

if __name__ == '__main__':
    # Load binding affinity data
    index_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\INDEX_general_PL_data.2018"
    binding_affinity_data = load_binding_affinity(index_file_path)
    print("Binding Affinity DataFrame:")
    print(binding_affinity_data.head())

    # Load coordinates data
    coordinates_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\output.txt"
    coordinates_df = load_coordinates(coordinates_file_path)
    print("Coordinates DataFrame:")
    print(coordinates_df.head())

    # Check for PDB IDs in coordinates file that are not in binding affinity data
    if not coordinates_df.empty:
        missing_binding_affinity_ids = set(coordinates_df['pdb_id']) - set(binding_affinity_data['pdb_id'])
        if missing_binding_affinity_ids:
            print("PDB IDs missing in binding affinity data:")
            print(missing_binding_affinity_ids)

        # Check for PDB IDs in binding affinity data that are not in coordinates file
        missing_coordinates_ids = set(binding_affinity_data['pdb_id']) - set(coordinates_df['pdb_id'])
        if missing_coordinates_ids:
            print("PDB IDs missing in coordinates data:")
            print(missing_coordinates_ids)

        # Merge data
        merged_df = pd.merge(coordinates_df, binding_affinity_data, on="pdb_id", how="inner")
        print("Merged DataFrame:")
        print(merged_df.head())

        # Save merged data
        merged_output_file_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\merged_data.csv"
        merged_df.to_csv(merged_output_file_path, index=False)
        print(f"Merged data has been saved to {merged_output_file_path}")
    else:
        print("Coordinates DataFrame is empty. Please check the format and content of output.txt.")
