import json

# Load the JSON data from the file
with open('output.json', 'r') as file:
    data = json.load(file)

# Inspect the data structure
print("Data type:", type(data))
if isinstance(data, list):
    print("Number of entries:", len(data))
    print("First entry:", data[0])  # Display the first entry if data is a list
elif isinstance(data, dict):
    print("Keys:", list(data.keys()))  # Display the keys if data is a dictionary
    first_key = list(data.keys())[0]
    print("First entry:", data[first_key])  # Display the first entry if data is a dictionary

# Check a sample of the data
if isinstance(data, list):
    # Data is a list of dictionaries
    sample_entry = data[0]
    print("Sample entry:", sample_entry)
elif isinstance(data, dict):
    # Data is a dictionary of dictionaries
    sample_entry = data[list(data.keys())[0]]
    print("Sample entry:", sample_entry)
