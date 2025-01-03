import json
import sys
import time
from collections import defaultdict
import os
from typing import List, Tuple, Dict


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

class LossyCounter:
    """
    Implements the Lossy Counting algorithm for finding frequent items in a data stream.
    Uses a support threshold (s) and error parameter (ε) to maintain frequency counts
    within guaranteed error bounds while using bounded memory.
    """
    
    def __init__(self, error: float):
        """
        Initialize the Lossy Counter.
        
        Args:
            error (float): Error parameter ε (epsilon), between 0 and 1.
                         Smaller values provide better accuracy but use more memory.
        """
        if not 0 < error < 1:
            raise ValueError("Error parameter must be between 0 and 1")
            
        self.error = error
        self.width = int(1 / error)  # Width of each bucket
        self.current_bucket = 1  # Current bucket number (bcurrent)
        self.total_items = 0  # Total number of items seen
        # Dictionary to store items: (frequency, delta)
        self.counts: Dict[str, Tuple[int, int]] = defaultdict(lambda: (0, 0))
    
    def process_item(self, item: str):
        """Process a single item from the stream."""
        self.total_items += 1
        
        # If item exists, increment its frequency
        if item in self.counts:
            freq, delta = self.counts[item]
            self.counts[item] = (freq + 1, delta)
        else:
            # Add new item with current bucket - 1 as delta
            self.counts[item] = (1, self.current_bucket - 1)
        
        # If we've seen width items, perform cleanup
        if self.total_items % self.width == 0:
            self._cleanup()
            self.current_bucket += 1
    
    def _cleanup(self):
        """Remove items whose frequency + delta ≤ current bucket number."""
        to_remove = []
        for item, (freq, delta) in self.counts.items():
            if freq + delta <= self.current_bucket:
                to_remove.append(item)
        
        for item in to_remove:
            del self.counts[item]
    
    def process_text(self, text: str):
        """Process all words in the text as a stream."""
        words = text.split()
        for word in words:
            self.process_item(word)
    
    def get_frequent_items(self, n: int = None) -> List[Tuple[str, int]]:
        """
        Get the n most frequent items.
        
        Args:
            n (int): Number of most frequent items to return. If None, returns all items.
        
        Returns:
            List of (item, estimated_frequency) tuples.
        """
        sorted_items = sorted(
            [(item, freq) for item, (freq, _) in self.counts.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_items[:n] if n is not None else sorted_items


""" ANALYSIS FUNCTIONS """

def analyze_text_file(file_path: str, output_path: str, error: float = 0.001, n_values: List[int] = None):
    """
    Analyze a text file using the Lossy Counting algorithm.
    
    Args:
        file_path: Path to the input text file
        output_path: Path to save the results
        error: Error parameter epsilon (default: 0.001)
        n_values: List of n values to test for most frequent items
    """
    if n_values is None:
        n_values = [5, 10, 15, 20]  # As specified in the project requirements
    
    # Load and preprocess the text
    text = load_text_file(file_path)
    
    # Create counter and measure execution time
    start_time = time.time()
    counter = LossyCounter(error)
    counter.process_text(text)
    execution_time = time.time() - start_time
    
    # Get results for different n values
    n_value_results = {}
    for n in n_values:
        frequent_items = counter.get_frequent_items(n)
        n_value_results[str(n)] = {
            "most_frequent_items": frequent_items,
            "number_of_items": len(frequent_items)
        }
    
    # Get all items for overall statistics
    all_counts = counter.get_frequent_items()
    
    # Save results
    results = {
        os.path.basename(file_path): {
            "algorithm": "lossy_count_stream",
            "parameters": {
                "error": error,
                "n_values_tested": n_values
            },
            "n_value_results": n_value_results,
            "total_items_processed": counter.total_items,
            "final_distinct_items": len(counter.counts),
            "least_frequent_items": all_counts[-10:],  # 10 least frequent items
            "execution_time": execution_time
        }
    }
    save_results(results, output_path)
    
    print(f"Results for {file_path} saved in {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lossy_count_stream.py <text_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_dir = "results"
    output_path = os.path.join(output_dir, "lossy_count_stream_results.json")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    analyze_text_file(file_path, output_path)