import os
import json
import csv
from datetime import datetime

def save_to_txt(data, filename=None):
    """Save encryption/decryption results to a text file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mini_aes_output_{timestamp}.txt"
    
    # Make sure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("=== Mini-AES Encryption/Decryption Results ===\n")
        file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write input data
        file.write(f"Mode: {data.get('mode', 'Unknown')}\n")
        if data.get('block_mode'):
            file.write(f"Block Mode: {data['block_mode']}\n")
        file.write(f"Input: {data.get('input', '')}\n")
        file.write(f"Key: {data.get('key', '')}\n")
        if data.get('block_mode') == 'CBC' and data.get('iv'):
            file.write(f"IV: {data['iv']}\n")
        
        # Write output data
        file.write(f"\nOutput: {data.get('output', '')}\n")
        
        # Write additional data
        file.write("\n=== Additional Data ===\n")
        for key, value in data.items():
            if key not in ['mode', 'input', 'key', 'output', 'iv', 'logs', 'block_mode']:
                file.write(f"{key}: {value}\n")
        
        # Write logs
        if 'logs' in data:
            file.write("\n=== Detailed Process Logs ===\n")
            for log in data['logs']:
                file.write(f"{log}\n")
    
    return os.path.abspath(filename)

def save_to_csv(data, filename=None):
    """Save encryption/decryption results to a CSV file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mini_aes_output_{timestamp}.csv"
    
    # Make sure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Prepare data for CSV
    csv_data = []
    
    # Add metadata
    csv_data.append(["Mini-AES Encryption/Decryption Results", ""])
    csv_data.append(["Time", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    csv_data.append(["", ""])  # Empty row for spacing
    
    # Add input data
    csv_data.append(["Mode", data.get('mode', 'Unknown')])
    if data.get('block_mode'):
        csv_data.append(["Block Mode", data['block_mode']])
    csv_data.append(["Input", data.get('input', '')])
    csv_data.append(["Key", data.get('key', '')])
    if data.get('block_mode') == 'CBC' and data.get('iv'):
        csv_data.append(["IV", data['iv']])
    
    # Add output data
    csv_data.append(["Output", data.get('output', '')])
    
    # Add additional data
    csv_data.append(["", ""])  # Empty row for spacing
    csv_data.append(["Additional Data", ""])
    for key, value in data.items():
        if key not in ['mode', 'input', 'key', 'output', 'iv', 'logs', 'block_mode']:
            csv_data.append([key, value])
    
    # Write logs (save limited number to avoid making CSV too large)
    if 'logs' in data:
        csv_data.append(["", ""])  # Empty row for spacing
        csv_data.append(["Process Logs", ""])
        for log in data['logs'][:100]:  # Limit to 100 log entries
            csv_data.append(["Log", log])
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    
    return os.path.abspath(filename)

def load_from_file(filename):
    """Load plaintext or key from a text file."""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    return content

def parse_input_file(filename):
    """Parse a structured input file with plaintext and key."""
    result = {}
    try:
        # Try to parse as JSON first
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass  # Not a JSON file, try other formats
        
        # Try to parse as simple text format (key=value)
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip().lower()] = value.strip()
            
            return result if result else {'input': load_from_file(filename)}
    
    except Exception as e:
        # If all parsing fails, just return the raw content as input
        return {'input': load_from_file(filename), 'error': str(e)}