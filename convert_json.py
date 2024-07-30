import re
import json

def parse_output_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    pdb_data = {}
    current_pdb_id = None
    ligand_coordinates = []
    pocket_coordinates = []
    
    for line in lines:
        pdb_id_match = re.match(r'Processing PDB ID: (\w+)', line)
        if pdb_id_match:
            if current_pdb_id:
                pdb_data[current_pdb_id] = {
                    "ligand_coordinates": ligand_coordinates,
                    "pocket_coordinates": pocket_coordinates
                }
            current_pdb_id = pdb_id_match.group(1)
            ligand_coordinates = []
            pocket_coordinates = []
        elif "Ligand Coordinates" in line:
            coordinates = re.findall(r"\('(\w+)', array\(\[([0-9.,\s-]+)\]", line)
            for atom, values in coordinates:
                values = [float(x) for x in values.split(',')]
                ligand_coordinates.append((atom, values))
        elif "Pocket Coordinates" in line:
            coordinates = re.findall(r"\('(\w+)', array\(\[([0-9.,\s-]+)\]", line)
            for atom, values in coordinates:
                values = [float(x) for x in values.split(',')]
                pocket_coordinates.append((atom, values))
    
    if current_pdb_id:
        pdb_data[current_pdb_id] = {
            "ligand_coordinates": ligand_coordinates,
            "pocket_coordinates": pocket_coordinates
        }

    return pdb_data

def save_as_json(data, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Specify the file paths
input_file_path = 'output.txt'
output_file_path = 'output.json'

# Parse the output.txt file
parsed_data = parse_output_txt(input_file_path)

# Save the parsed data as a JSON file
save_as_json(parsed_data, output_file_path)

print(f"Data successfully parsed and saved to {output_file_path}")
