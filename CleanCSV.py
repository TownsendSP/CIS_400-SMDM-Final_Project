import csv

with open('5M_English_bluesky.csv', 'r', newline='') as infile, open('5m_english_bluesky_cleaned.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    for row in reader:
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        cleaned_row = [field.replace('\n', ' ').replace('\r', '') for field in row]
        writer.writerow(cleaned_row)
