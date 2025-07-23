import json
import sys
import re
import csv
import ast


def extract_text_from_jsonl(input_file, output_file, max_lines=500):
    """
    Reads a text file where each line is a JSON object, extracts the 'text' attribute from each,
    and saves the extracted text to an output file. Stops after processing max_lines.
    
    Args:
        input_file (str): Path to the input file with JSON objects on each line
        output_file (str): Path to the output text file
        max_lines (int): Maximum number of lines to process
    """
    try:
        extracted_texts = []
        processed_lines = 0
        id_pattern = re.compile(r"'_id':\s*'([^']*)', '") #"', '" at the end to limit matches to the end of the field data
        text_pattern = re.compile(r"\s'text':\s*['\"](.*?)['\"], '")
        # Process the file line by line
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                id_match = id_pattern.search(line)
                text_match = text_pattern.search(line)
                if id_match and text_match:
                    tweet_id = id_match.group(1)
                    tweet_text = text_match.group(1)
                    if tweet_text.startswith("RT"):
                        continue
                    extracted_texts.append((tweet_id, tweet_text))
                
                    processed_lines += 1
                    if processed_lines >= max_lines:
                        print(f"Reached limit of {max_lines} lines. Stopping.")
                        break
        
        # Write all extracted texts to the output file
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['tweet_id', 'tweet_text'])  # header
            writer.writerows(extracted_texts)  # data rows
                
        print(f"Successfully extracted {len(extracted_texts)} text entries to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        # If third argument is provided, use it as max_lines
        max_lines = 500  # Default
        if len(sys.argv) >= 4:
            try:
                max_lines = int(sys.argv[3])
            except ValueError:
                print(f"Invalid max lines value: {sys.argv[3]}. Using default: 500")
        
        extract_text_from_jsonl(sys.argv[1], sys.argv[2], max_lines)
    else:
        # If arguments aren't provided, prompt the user
        input_file = "EVS_Tweets_USA.txt"
        output_file = "Tw_2_rate.csv"
        max_lines = 500
        
extract_text_from_jsonl(input_file, output_file, max_lines=500)