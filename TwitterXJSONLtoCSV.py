import json
import csv
import os
import time
from typing import List, Dict

def process_twitter_jsonl(input_file: str, output_file: str) -> Dict[str, float]:
    """
    Convert a JSONL file of Twitter data to a CSV file, including performance metrics.
    
    Parameters:
    - input_file (str): Path to the input JSONL file
    - output_file (str): Path to the output CSV file
    
    Returns:
    - Dictionary with processing performance metrics
    """
    start_time = time.time()
    processed_lines = 0
    skipped_lines = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as jsonl_file, \
             open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Likes', 'Retweets', 'Replies', 'Created At', 'text', 'Reply Settings'])
            
            # Process each line in the JSONL file
            for line in jsonl_file:
                try:
                    tweet_data = json.loads(line)

                    # Extract top-level tweet data
                    data = tweet_data.get('data', {})
                    text = data.get('text', 'N/A')
                    
                    # Extract public metrics
                    public_metrics = data.get('public_metrics', {})
                    likes = public_metrics.get('like_count', 0)
                    retweets = public_metrics.get('retweet_count', 0)
                    replies = public_metrics.get('reply_count', 0)
                    
                    # Extract creation time and reply settings
                    created_at = data.get('created_at', 'N/A')
                    reply_settings = data.get('reply_settings', 'N/A')
                    
                    csv_writer.writerow([
                        text, 
                        likes, 
                        retweets, 
                        replies, 
                        created_at, 
                        reply_settings
                    ])
                    
                    processed_lines += 1
                    
                except json.JSONDecodeError:
                    skipped_lines += 1
                except Exception as e:
                    skipped_lines += 1
        
        end_time = time.time()
        
        return {
            'total_time': end_time - start_time,
            'processed_lines': processed_lines,
            'skipped_lines': skipped_lines
        }
    
    except Exception as e:
        print(f"Error processing file {input_file}: {e}")
        return {
            'total_time': 0,
            'processed_lines': 0,
            'skipped_lines': 0
        }

def process_jsonl_folder(input_folder: str, output_folder: str) -> List[Dict[str, float]]:
    os.makedirs(output_folder, exist_ok=True)
    
    file_performance_metrics = []
    total_start_time = time.time()
    
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.jsonl'):
                input_path = os.path.join(root, file)
                
                relative_path = os.path.relpath(input_path, input_folder)
                output_filename = os.path.splitext(relative_path)[0] + '.csv'
                output_path = os.path.join(output_folder, output_filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                print(f"Processing {input_path}...")
                
                # Process the file
                metrics = process_twitter_jsonl(input_path, output_path)
                metrics['input_file'] = input_path
                file_performance_metrics.append(metrics)
    
    total_end_time = time.time()
    
    # Print summary
    print("\n--- Processing Summary ---")
    for metrics in file_performance_metrics:
        print(f"File: {metrics['input_file']}")
        print(f"  Processing Time: {metrics['total_time']:.2f} seconds")
        print(f"  Processed Lines: {metrics['processed_lines']}")
        print(f"  Skipped Lines: {metrics['skipped_lines']}")
    
    # Calculate and print overall statistics
    avg_processing_time = sum(m['total_time'] for m in file_performance_metrics) / len(file_performance_metrics)
    print(f"\nAverage File Processing Time: {avg_processing_time:.2f} seconds")
    print(f"Total Processing Time: {total_end_time - total_start_time:.2f} seconds")
    
    return file_performance_metrics

def main():
    # Example usage
    input_folder = '/mnt/ssd2/SMDM_Project_Data/archiveteam-twitter-stream-2023-01/2023/1'
    output_folder = '/mnt/ssd2/SMDM_Project_Data/archiveteam-twitter-stream-2023-01/2023/1_csv'
    
    process_jsonl_folder(input_folder, output_folder)

if __name__ == '__main__':
    main()
