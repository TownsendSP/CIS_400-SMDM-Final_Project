import json
import csv
import os
import sys
import time
from typing import List, Dict
from tqdm import tqdm

def process_jsonl_folder(input_folder: str, output_file: str) -> Dict[str, float]:
    """
    Recursively process all JSONL files in a folder, appending to a single CSV file.
    Supports partial write on keyboard interrupt.
    """
    jsonl_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.jsonl'):
                jsonl_files.append(os.path.join(root, file))

    # Performance tracking
    start_time = time.time()
    processed_lines = 0
    skipped_lines = 0

    # Collect data in memory
    csv_data = []

    try:
        # Process files with progress bar
        for file in tqdm(jsonl_files, total=len(jsonl_files), desc="Processing files"):
            try:
                with open(file, 'r', encoding='utf-8') as jsonl_file:
                    for line in jsonl_file:
                        try:
                            # Parse the JSON data
                            tweet_data = json.loads(line)

                            # Extract top-level tweet data
                            data = tweet_data.get('data', {})
                            text = data.get('text', 'N/A').replace('\n', ' ').replace('\r', '')

                            # Extract public metrics
                            public_metrics = data.get('public_metrics', {})
                            likes = public_metrics.get('like_count', 0)
                            retweets = public_metrics.get('retweet_count', 0)
                            replies = public_metrics.get('reply_count', 0)

                            # Extract creation time and reply settings
                            created_at = data.get('created_at', 'N/A')
                            reply_settings = data.get('reply_settings', 'N/A')

                            # Collect row
                            csv_data.append([
                                likes,
                                retweets,
                                text,
                                replies,
                                created_at,
                                reply_settings
                            ])

                            processed_lines += 1

                        except json.JSONDecodeError:
                            skipped_lines += 1
                        except Exception:
                            skipped_lines += 1

            except Exception:
                print(f"Error processing file {file}")

    except KeyboardInterrupt:
        # Partial write on interrupt
        partial_output = output_file
        print(f"\nKeyboard interrupt. Writing partial results to {partial_output}")

        with open(partial_output, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Likes', 'Retweets', 'text', 'Replies', 'Created At', 'Reply Settings'])
            csv_writer.writerows(csv_data)

        print(f"Processed {processed_lines} lines before interrupt")
        sys.exit(1)

    # Write collected data to single CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Likes', 'Retweets', 'text', 'Replies', 'Created At', 'Reply Settings'])
        csv_writer.writerows(csv_data)

    end_time = time.time()

    return {
        'total_time': end_time - start_time,
        'processed_lines': processed_lines,
        'skipped_lines': skipped_lines
    }

def main():
    input_folder = '/mnt/ssd2/SMDM_Project_Data/archiveteam-twitter-stream-2023-01/2023/1'
    output_file = '/mnt/ssd2/SMDM_Project_Data/archiveteam-twitter-stream-2023-01/2023/2_combined.csv'

    metrics = process_jsonl_folder(input_folder, output_file)

    print(f"\nTotal Processing Time: {metrics['total_time']:.2f} seconds")
    print(f"Processed Lines: {metrics['processed_lines']}")
    print(f"Skipped Lines: {metrics['skipped_lines']}")

if __name__ == '__main__':
    main()
