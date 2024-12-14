import pandas as pd
import torch
import warnings
import argparse
import os
import multiprocessing
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from datasets import Dataset

def sentiment_worker(batch):
    """
    Standalone function for sentiment analysis to work with multiprocessing

    Args:
        batch (dict): Batch of examples from the dataset

    Returns:
        dict: Batch with added sentiment information
    """

    model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        device_map='cuda' if device.type == 'cuda' else 'cpu',
        torch_dtype=torch.float16 if device.type == 'cuda' else torch.float32
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Create sentiment pipeline
    sentiment_pipeline = pipeline(
        'sentiment-analysis',
        model=model,
        tokenizer=tokenizer,
    )

    # Prepare texts, handling potential missing values
    texts = [str(text) if text and not pd.isna(text) else '' for text in batch['text']]

    # Perform sentiment analysis on non-empty texts
    non_empty_texts = [t for t in texts if t]

    # Perform sentiment analysis
    try:
        if non_empty_texts:
            results = sentiment_pipeline(non_empty_texts)
        else:
            results = []
    except Exception as e:
        print(f"Error in batch processing: {e}")
        results = [{'label': 'NEUTRAL', 'score': 0.5}] * len(non_empty_texts)

    # Reconstruct full results with placeholders for empty texts
    full_results = []
    result_idx = 0
    for text in texts:
        if text and not pd.isna(text):
            full_results.append(results[result_idx])
            result_idx += 1
        else:
            full_results.append({'label': 'NEUTRAL', 'score': 0.5})

    return {
        'sentiment_label': [result['label'] for result in full_results],
        'sentiment_score': [result['score'] for result in full_results]
    }

class DatasetSentimentAnalyzer:
    def __init__(self, output_path='./sentiment_analyzed.csv', batch_size=1024):
        multiprocessing.set_start_method('spawn', force=True)

        self.output_path = output_path
        self.batch_size = batch_size
        self.num_workers = max(1, multiprocessing.cpu_count() - 2)

    def analyze_csv(self, input_path):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Read entire CSV into DataFrame
        df = pd.read_csv(input_path)

        # Convert to Hugging Face Dataset
        dataset = Dataset.from_pandas(df)

        # Apply sentiment analysis with multiprocessing
        dataset = dataset.map(
            sentiment_worker,
            batched=True,
            batch_size=self.batch_size,
            num_proc=self.num_workers,
            remove_columns=[]
        )

        analyzed_df = dataset.to_pandas()
        analyzed_df.to_csv(self.output_path, index=False)

        print(f"Sentiment analysis complete. Results saved to {self.output_path}")

        return {
            'output_file': self.output_path,
            'total_processed': len(analyzed_df),
            'workers_used': self.num_workers
        }

def main():
    parser = argparse.ArgumentParser(description="Analyze sentiment in a CSV file.")
    parser.add_argument('--input', '-i', required=True, help="Path to the input CSV file")
    parser.add_argument('--output', '-o', required=True, help="Path to save the analyzed CSV file")
    args = parser.parse_args()

    analyzer = DatasetSentimentAnalyzer(output_path=args.output)

    try:
        results = analyzer.analyze_csv(args.input)
        print("Analysis Results:")
        print(results)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
