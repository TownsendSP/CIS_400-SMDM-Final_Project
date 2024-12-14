import re

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        content = infile.read()
        processed_content = re.sub(r'(?<!")\n', ' ', content)
        outfile.write(processed_content)

input_file = 'combined.csv'
output_file = 'combined_fixed.csv'
process_csv(input_file, output_file)
