# CIS_400-SMDM-Final_Project
Final Project - Comparitive Sentiment Analysis of Bluesky and Twitter

A Python-based project for processing, cleaning, analyzing, and visualizing social media data. This project provides tools for working with JSONL and CSV files, sentiment analysis, and graph visualization for platforms like X (Twitter) and Bluesky.

File Overview

Main Scripts

- BlueskyGraph.py
  - Generates graphs and visualizations for Bluesky data.

- CleanCSV.py
  - Cleans and preprocesses CSV files to remove inconsistencies and prepare data for analysis.

- FixCSV.py
  - Fixes structural issues in CSV files to ensure proper formatting.

- SentimentAnalyzer.py
  - Analyzes sentiment in text data, providing insights into positive, negative, or neutral sentiments.

- TwitterXCombineJSONLFolder.py
  - Combines multiple JSONL files from a folder into a single, consolidated CSV for further processing.

- TwitterXGraph.py
  - Creates graphs and visualizations based on X (Twitter) data.

- TwitterXJSONLtoCSV.py
  - Converts JSONL files containing X (Twitter) data into CSV format for easier analysis.

Support Files

- LICENSE
  - Contains the licensing information for the project.

- README.md
  - Provides an overview of the project, including file descriptions and usage instructions.

- requirements.txt
  - Lists the Python dependencies required to run the scripts in this project.

Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-folder>
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Usage

Each script in this project is standalone. Use the following commands to run them:

- BlueskyGraph.py
  ```bash
  python BlueskyGraph.py
  ```

- CleanCSV.py
  ```bash
  python CleanCSV.py --input <input_file.csv> --output <output_file.csv>
  ```

- FixCSV.py
  ```bash
  python FixCSV.py --input <input_file.csv> --output <output_file.csv>
  ```

- SentimentAnalyzer.py
  ```bash
  python SentimentAnalyzer.py --input <input_file.csv> --output <output_file.csv>
  ```

- TwitterXCombineJSONLFolder.py
  ```bash
  python TwitterXCombineJSONLFolder.py --folder <folder_path> --output <output_file.jsonl>
  ```

- TwitterXGraph.py
  ```bash
  python TwitterXGraph.py --input <input_file.csv>
  ```

- TwitterXJSONLtoCSV.py
  ```bash
  python TwitterXJSONLtoCSV.py --input <input_file.jsonl> --output <output_file.csv>
  ```

License

This project is licensed under the terms of the license provided in the **LICENSE** file.

Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

Contact

For questions or suggestions, please contact Townsend Southard Pantano at tgsoutha@syr.edu or Aaron Moradi at ammoradi@syr.edu.
