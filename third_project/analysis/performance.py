import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns

class PerformanceAnalyzer:
    def __init__(self, results_dir="results"):
        self.results_dir = Path(results_dir)
        self.languages = ["English", "Esperanto", "Finnish", "French", "German", "Italian"]
        self.algorithms = ["exact_counter", "lossy_count_stream", "decreasing_prob_counter"]
        
    def load_results(self):
        """Load results for all algorithms and languages."""
        self.results = {}
        
        for algo in self.algorithms:
            file_path = self.results_dir / f"{algo}_results.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    self.results[algo] = json.load(f)
                    
    def plot_execution_times(self):
        """Compare execution times across algorithms and languages."""
        times = {lang: [0, 0, 0] for lang in self.languages}  # Initialize with zeros
        
        for lang in self.languages:
            filename = f"processed_{lang}.txt"
            
            # Exact counter
            if 'exact_counter' in self.results:
                if filename in self.results['exact_counter']:
                    times[lang][0] = self.results['exact_counter'][filename]['execution_time']
                    
            # Lossy count
            if 'lossy_count_stream' in self.results:
                if filename in self.results['lossy_count_stream']:
                    times[lang][1] = self.results['lossy_count_stream'][filename]['execution_time']
                    
            # Decreasing probability
            if 'decreasing_prob_counter' in self.results:
                if filename in self.results['decreasing_prob_counter']:
                    times[lang][2] = self.results['decreasing_prob_counter'][filename]['average_execution_time']
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        x = np.arange(len(self.languages))
        width = 0.25
        
        plt.bar(x - width, [times[lang][0] for lang in self.languages], width, label='Exact Counter')
        plt.bar(x, [times[lang][1] for lang in self.languages], width, label='Lossy Count')
        plt.bar(x + width, [times[lang][2] for lang in self.languages], width, label='Decreasing Probability')
        
        plt.xlabel('Languages')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Execution Time Comparison Across Algorithms and Languages')
        plt.xticks(x, self.languages)
        plt.legend()
        plt.tight_layout()
        plt.savefig('execution_times.png')
        plt.close()
        
    def plot_accuracy_comparison(self):
        """Compare accuracy of approximate methods against exact counts."""
        for lang in self.languages:
            filename = f"processed_{lang}.txt"
            
            # Get exact counts
            exact_counts = dict(self.results['exact_counter'][filename]['most_common'])
            
            # Get lossy counts
            lossy_counts = {}
            if filename in self.results['lossy_count_stream']:
                lossy_results = self.results['lossy_count_stream'][filename]['n_value_results']['10']['most_frequent_items']
                lossy_counts = dict(lossy_results)
            
            # Get probability counts (average across trials)
            prob_counts = {}
            if filename in self.results['decreasing_prob_counter']:
                trials = self.results['decreasing_prob_counter'][filename]['trial_results']
                for word, _ in exact_counts.items():
                    counts = []
                    for trial in trials:
                        trial_counts = dict(trial['most_common'])
                        if word in trial_counts:
                            counts.append(trial_counts[word])
                    if counts:
                        prob_counts[word] = np.mean(counts)
            
            # Create relative error plot for lossy count
            plt.figure(figsize=(10, 6))
            words = list(exact_counts.keys())
            
            lossy_errors = []
            
            for word in words:
                exact = exact_counts[word]
                lossy_error = abs(lossy_counts.get(word, 0) - exact) / exact * 100 if word in lossy_counts else 100
                lossy_errors.append(lossy_error)
            
            x = np.arange(len(words))
            width = 0.35
            
            plt.bar(x, lossy_errors, width, label='Lossy Count Error')
            
            plt.xlabel('Words')
            plt.ylabel('Relative Error (%)')
            plt.title(f'Relative Error Comparison - Lossy Count - {lang}')
            plt.xticks(x, words, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'accuracy_comparison_lossy_{lang}.png')
            plt.close()
            
            # Create relative error plot for decreasing probability
            plt.figure(figsize=(10, 6))
            
            prob_errors = []
            
            for word in words:
                exact = exact_counts[word]
                prob_error = abs(prob_counts.get(word, 0) - exact) / exact * 100 if word in prob_counts else 100
                prob_errors.append(prob_error)
            
            plt.bar(x, prob_errors, width, label='Decreasing Probability Error')
            
            plt.xlabel('Words')
            plt.ylabel('Relative Error (%)')
            plt.title(f'Relative Error Comparison - Decreasing Probability - {lang}')
            plt.xticks(x, words, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'accuracy_comparison_prob_{lang}.png')
            plt.close()
            
    def plot_memory_usage(self):
        """Compare memory usage (distinct items tracked) across algorithms."""
        distinct_items = {lang: [] for lang in self.languages}
        
        for lang in self.languages:
            filename = f"processed_{lang}.txt"
            
            # Exact counter (total unique words)
            if filename in self.results['exact_counter']:
                distinct_items[lang].append(self.results['exact_counter'][filename]['total_words'])
                
            # Lossy count
            if filename in self.results['lossy_count_stream']:
                distinct_items[lang].append(self.results['lossy_count_stream'][filename]['final_distinct_items'])
                
            # Decreasing probability (average across trials)
            if filename in self.results['decreasing_prob_counter']:
                trials = self.results['decreasing_prob_counter'][filename]['trial_results']
                avg_items = np.mean([len(trial['most_common']) for trial in trials])
                distinct_items[lang].append(avg_items)
        
        plt.figure(figsize=(12, 6))
        x = np.arange(len(self.languages))
        width = 0.25
        
        plt.bar(x - width, [distinct_items[lang][0] for lang in self.languages], width, label='Exact Counter')
        plt.bar(x, [distinct_items[lang][1] for lang in self.languages], width, label='Lossy Count')
        plt.bar(x + width, [distinct_items[lang][2] for lang in self.languages], width, label='Decreasing Probability')
        
        plt.xlabel('Languages')
        plt.ylabel('Number of Distinct Items Tracked')
        plt.title('Memory Usage Comparison (Distinct Items)')
        plt.xticks(x, self.languages)
        plt.legend()
        plt.tight_layout()
        plt.savefig('memory_usage.png')
        plt.close()

def main():
    analyzer = PerformanceAnalyzer()
    analyzer.load_results()
    analyzer.plot_execution_times()
    analyzer.plot_accuracy_comparison()
    analyzer.plot_memory_usage()

if __name__ == "__main__":
    main()