import json
import sys
import time
from collections import defaultdict
import random
import os
import math


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

class DecreasingProbCounter:
    """
    Implements the Decreasing Probability Counter (1/2^k) algorithm.
    For each word, maintains a counter that is incremented with probability 1/2^k,
    where k is the current value of the counter.
    """
    
    def __init__(self):
        self.counters = defaultdict(int)
    
    def increment(self, word: str):
        """
        Increment counter for a word with probability 1/2^k.
        """
        k = self.counters[word]
        if random.random() < 1 / (2 ** k):
            self.counters[word] += 1
    
    def get_count(self, word: str) -> int:
        """
        Get the estimated count for a word.
        The actual estimate is (2^k - 1), where k is the counter value.
        """
        k = self.counters[word]
        return (2 ** k) - 1 if k > 0 else 0
    
    def process_text(self, text: str):
        """
        Process all words in the text.
        """
        words = text.split()
        for word in words:
            self.increment(word)
    
    def most_common(self, n: int = None):
        """
        Return the n most common words and their estimated counts.
        """
        # Calculate estimated counts for all words
        estimates = {word: self.get_count(word) for word in self.counters}
        # Sort by estimated count
        sorted_words = sorted(estimates.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:n] if n is not None else sorted_words


""" ANALYSIS FUNCTIONS """

def analyze_text_file(file_path: str, output_path: str, num_trials: int = 5):
    """
    Analyze a text file using the Decreasing Probability Counter algorithm.
    Performs multiple trials to account for the randomness in the algorithm.
    """
    # Load and preprocess the text
    text = load_text_file(file_path)
    
    trial_results = []
    total_execution_time = 0
    
    for trial in range(num_trials):
        # Create new counter instance and measure execution time
        counter = DecreasingProbCounter()
        
        start_time = time.time()
        counter.process_text(text)
        execution_time = time.time() - start_time
        total_execution_time += execution_time
        
        # Get results for this trial
        most_common = counter.most_common(10)
        less_common = counter.most_common()[-10:]
        
        trial_results.append({
            "most_common": most_common,
            "less_common": less_common,
            "execution_time": execution_time
        })
    
    # Calculate average results across all trials
    avg_execution_time = total_execution_time / num_trials
    
    # Save results
    results = {
        os.path.basename(file_path): {
            "algorithm": "decreasing_probability_counter",
            "num_trials": num_trials,
            "trial_results": trial_results,
            "average_execution_time": avg_execution_time
        }
    }
    save_results(results, output_path)
    
    print(f"Results for {file_path} saved in {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decreasing_prob_counter.py <text_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_dir = "results"
    output_path = os.path.join(output_dir, "decreasing_prob_counter_results.json")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    analyze_text_file(file_path, output_path)