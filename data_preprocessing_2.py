import os
import glob
from Bio.PDB import PDBParser
from rdkit import Chem
import numpy as np

# Define the path to your PDB bind dataset
pdb_bind_path = r"C:\Users\91985\drug-discovery-analysis\data\refined-set"
output_file = r"C:\Users\91985\drug-discovery-analysis\data\refined-set\output.txt"

# Create PDB parser
parser = PDBParser(QUIET=True)

def read_ligand_coordinates(ligand_file):
    coordinates = []
    try:
        if ligand_file.endswith('.mol2'):
            mol = Chem.MolFromMol2File(ligand_file)
        elif ligand_file.endswith('.sdf'):
            suppl = Chem.SDMolSupplier(ligand_file)
            mol = next(suppl)
        else:
            raise ValueError("Unsupported ligand file format")

        if mol is None:
            raise ValueError("Failed to read ligand file")

        conf = mol.GetConformer()
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            coordinates.append((atom.GetSymbol(), np.array([pos.x, pos.y, pos.z], dtype=np.float32)))
    except Exception as e:
        raise ValueError(f"Error reading ligand file: {ligand_file}, {e}")
    return coordinates

def read_protein_coordinates(pocket_file):
    coordinates = []
    try:
        structure = parser.get_structure('protein', pocket_file)
        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        coordinates.append((atom.get_name(), atom.get_vector().get_array()))
    except Exception as e:
        raise ValueError(f"Error reading pocket file: {pocket_file}, {e}")
    return coordinates

# Open the output file for writing
with open(output_file, 'w') as f_out:
    for pdb_id_folder in glob.glob(os.path.join(pdb_bind_path, '*')):
        pdb_id = os.path.basename(pdb_id_folder)
        
        # Print the directory being processed
        print(f"Processing directory: {pdb_id_folder}")
        
        # Search for ligand files matching the patterns *_ligand.mol2 and *_ligand.sdf
        ligand_files = glob.glob(os.path.join(pdb_id_folder, '*_ligand.mol2')) + glob.glob(os.path.join(pdb_id_folder, '*_ligand.sdf'))
        print(f"Ligand files found: {ligand_files}")
        
        if not ligand_files:
            print(f"Ligand file not found for PDB ID: {pdb_id}")
            f_out.write(f"Ligand file not found for PDB ID: {pdb_id}\n")
            continue
        
        # Use the first matching ligand file (assuming there is only one per folder)
        ligand_file = ligand_files[0]
        pocket_file = os.path.join(pdb_id_folder, f'{pdb_id}_pocket.pdb')
        
        print(f"Processing PDB ID: {pdb_id}")
        f_out.write(f"Processing PDB ID: {pdb_id}\n")
        
        # Read ligand coordinates
        try:
            ligand_coords = read_ligand_coordinates(ligand_file)
            f_out.write(f"PDB ID: {pdb_id} Ligand Coordinates: {ligand_coords}\n")
        except ValueError as e:
            print(f"Error: {e}")
            f_out.write(f"Error: {e}\n")
            continue
        
        # Read protein pocket coordinates
        try:
            pocket_coords = read_protein_coordinates(pocket_file)
            f_out.write(f"PDB ID: {pdb_id} Pocket Coordinates: {pocket_coords}\n")
        except ValueError as e:
            print(f"Error: {e}")
            f_out.write(f"Error: {e}\n")
            continue

print("Data preprocessing completed.")
