import json
import os

def load_json_file(file_path):
    try:
        print(f"Attempting to load file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Successfully loaded data from {file_path}")
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {file_path}")
        return None

# Get the absolute path to the medier directory
medier_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Medier directory: {medier_dir}")

# Load the JSON files
victoria_data = load_json_file(os.path.join(medier_dir, 'victoria', 'victoria.json'))
victoria_used_data = load_json_file(os.path.join(medier_dir, 'victoria', 'victoria_used.json'))

# Export the data
__all__ = ['victoria_data', 'victoria_used_data']
