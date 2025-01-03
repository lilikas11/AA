import json
import sys
import time
from collections import Counter
import os


""" HELP FUNCTIONS """

def load_text_file(filename: str) -> str:
    """Load text content from a file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def save_results(results: dict, output_path: str):
    """Save results to a JSON file."""
    try:
        with open(output_path, 'r') as file:
            existing_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = {}

    existing_results.update(results)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(existing_results, file, indent=4)


""" ALGORITHM FUNCTIONS """

def exact_counter(text: str) -> Counter:
    """
    Count the exact frequency of each word in the text.
    Basic Operations Count:
    O(n) where n is the number of words in the text.
    """
    # Tokenize by splitting text into words
    words = text.split()

    # Count word frequencies
    return Counter(words)


""" ANALYSIS FUNCTIONS """

def analyze_text_file(file_path: str, output_path: str):
    # Load and preprocess the text
    text = load_text_file(file_path)

    # Measure time for exact counting
    start_time = time.time()
    word_counts = exact_counter(text)
    execution_time = time.time() - start_time

    # Save results
    results = {
        os.path.basename(file_path): {
            "total_words": len(word_counts),
            "most_common": word_counts.most_common(10),
            "less_common": word_counts.most_common()[:-11:-1],
            "execution_time": execution_time
        }
    }
    save_results(results, output_path)

    print(f"Results for {file_path} saved in {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exact_counter.py <text_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_dir = "results"
    output_path = os.path.join(output_dir, "exact_counter_results.json")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    analyze_text_file(file_path, output_path)
