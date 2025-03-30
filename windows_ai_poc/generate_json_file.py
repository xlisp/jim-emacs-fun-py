import json
from typing import Dict, Any

def generate_json_file(model_name: str, header: Dict[str, Any], filename: str = "output.json") -> None:
    """
    Generate a JSON file based on model_name and header.
    
    Args:
        model_name: The name of the model
        header: A dictionary containing header information
        filename: Name of the output JSON file (default: "output.json")
    """
    # Create the base JSON structure
    data = {
        "model": model_name,
        "headers": header,
        "metadata": {
            "generated_at": "2025-03-30",
            "version": "1.0"
        }
    }
    
    # Write the dictionary to a JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"JSON file '{filename}' has been created successfully.")

# Example usage
if __name__ == "__main__":
    # Example inputs
    model = "gpt-4"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY",
        "User-Agent": "Python/3.9"
    }
    
    # Generate the JSON file
    generate_json_file(model, headers, "config.json")

