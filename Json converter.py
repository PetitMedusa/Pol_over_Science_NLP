import json
import re

def convert_json_quotes(text):
    # Track state to avoid replacing quotes in the middle of strings
    result = ""
    in_string = False
    quote_type = None
    escape_next = False
    
    for i, char in enumerate(text):
        # Handle escape sequences
        if escape_next:
            result += char
            escape_next = False
            continue
            
        if char == '\\':
            result += char
            escape_next = True
            continue
            
        # Track string state
        if char in ['"', "'"]:
            # Start of a string or end of a string
            if not in_string:
                # Starting a new string - convert single quote to double
                in_string = True
                quote_type = char
                result += '"'  # Always use double quotes for JSON
            elif char == quote_type:
                # Ending current string - convert single quote to double
                in_string = False
                result += '"'  # Always use double quotes for JSON
            else:
                # This is a different quote inside a string - keep as is
                result += char
        else:
            # Regular character, add as is
            result += char
            
    return result

def convert_to_json(input_file, output_file):
    """
    Convert a file with Python dict objects containing datetime.datetime objects
    into a proper JSON file with ISO formatted date strings.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.readlines()
    
    json_objects = []
    
    for line in content:
        if not line.strip():
            continue
            
        # Extract datetime values from datetime.datetime() function calls
        # This regex captures the year, month, day, hour, minute, second values
        def replace_datetime(match):
            parts = match.group(1).split(', ')
            
            # Extract components
            year = parts[0]
            month = parts[1].zfill(2)  # Zero-pad to ensure 2 digits
            day = parts[2].zfill(2)
            
            # Handle time components if they exist
            time_part = "00:00:00"
            if len(parts) > 3:
                hour = parts[3].zfill(2)
                minute = "00"
                second = "00"
                
                if len(parts) > 4:
                    minute = parts[4].zfill(2)
                
                if len(parts) > 5:
                    second = parts[5].zfill(2)
                
                time_part = f"{hour}:{minute}:{second}"
            
            # Create ISO format date string
            return f'"{year}-{month}-{day}T{time_part}Z"'
        
        # Replace datetime objects with ISO format strings
        modified_line = re.sub(r"datetime\.datetime\(([\d, ]+)\)", replace_datetime, line)
        
        # Replace Python syntax with JSON syntax
        modified_line = convert_json_quotes(modified_line)
        modified_line = modified_line.replace("True", "true")
        modified_line = modified_line.replace("False", "false")
        modified_line = modified_line.replace("None", "null")
        
        try:
            # Parse as JSON to validate and then add to our list
            obj = json.loads(modified_line)
            json_objects.append(obj)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")
            print(f"Problematic line: {modified_line[:100]}...")
    
    # Write all objects to JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(json_objects, outfile, indent=2)
    
    return len(json_objects)

# Usage example
if __name__ == "__main__":
    input_file = "keyword_filter_output/USA_March_June2020.txt"  # Change to your input file
    output_file = "keyword_filter_output/USA-03-06-2020.json"  # Change to your desired output file
    
    count = convert_to_json(input_file, output_file)
    print(f"Successfully converted {count} objects to JSON in {output_file}")