import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple
from scipy.stats import kendalltau

class WordOrderAnalyzer:
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

    def get_word_rankings(self, language: str) -> Dict[str, List[Tuple[str, int]]]:
        """Get top and bottom word rankings for each algorithm for a specific language."""
        filename = f"processed_{language}.txt"
        rankings = {}
        
        # Exact Counter
        if filename in self.results['exact_counter']:
            rankings['exact'] = {
                'top': self.results['exact_counter'][filename]['most_common'],
                'bottom': self.results['exact_counter'][filename]['less_common']
            }
        
        # Lossy Count
        if filename in self.results['lossy_count_stream']:
            rankings['lossy'] = {
                'top': self.results['lossy_count_stream'][filename]['n_value_results']['10']['most_frequent_items'],
                'bottom': self.results['lossy_count_stream'][filename]['least_frequent_items']
            }
        
        # Decreasing Probability (average across trials)
        if filename in self.results['decreasing_prob_counter']:
            trials = self.results['decreasing_prob_counter'][filename]['trial_results']
            # Get most common words from first trial (could average across trials if needed)
            rankings['prob'] = {
                'top': trials[0]['most_common'],
                'bottom': trials[0]['less_common']
            }
            
        return rankings

    def plot_rank_correlation_matrix(self, language: str):
        """Plot correlation matrix of word rankings between algorithms."""
        rankings = self.get_word_rankings(language)
        
        # Create lists of words and their ranks for each algorithm
        word_ranks = {}
        all_words = set()
        
        for algo, data in rankings.items():
            word_ranks[algo] = {}
            # Add top words
            for rank, (word, _) in enumerate(data['top']):
                word_ranks[algo][word] = rank
                all_words.add(word)
            # Add bottom words
            for rank, (word, _) in enumerate(data['bottom']):
                word_ranks[algo][word] = len(data['top']) + rank
                all_words.add(word)
        
        # Calculate correlation matrix
        algos = list(rankings.keys())
        corr_matrix = np.zeros((len(algos), len(algos)))
        
        for i, algo1 in enumerate(algos):
            for j, algo2 in enumerate(algos):
                # Get common words
                common_words = set(word_ranks[algo1].keys()) & set(word_ranks[algo2].keys())
                if common_words:
                    # Extract rankings for common words
                    ranks1 = [word_ranks[algo1][word] for word in common_words]
                    ranks2 = [word_ranks[algo2][word] for word in common_words]
                    # Calculate Kendall's tau correlation
                    tau, _ = kendalltau(ranks1, ranks2)
                    corr_matrix[i, j] = tau
        
        # Plot correlation matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, 
                   annot=True, 
                   cmap='RdYlBu', 
                   xticklabels=algos, 
                   yticklabels=algos,
                   vmin=-1, 
                   vmax=1)
        plt.title(f'Rank Correlation Matrix - {language}')
        plt.tight_layout()
        plt.savefig(f'rank_correlation_{language}.png')
        plt.close()

    def plot_top_words_comparison(self, language: str):
        """Plot comparison of top words identified by each algorithm."""
        rankings = self.get_word_rankings(language)
        
        # Prepare data for plotting
        all_words = set()
        word_freqs = {}
        
        for algo, data in rankings.items():
            word_freqs[algo] = dict(data['top'])
            all_words.update(word_freqs[algo].keys())
        
        # Create DataFrame for plotting
        df_data = []
        for word in all_words:
            for algo in rankings.keys():
                df_data.append({
                    'Algorithm': algo,
                    'Word': word,
                    'Frequency': word_freqs[algo].get(word, 0)
                })
        
        df = pd.DataFrame(df_data)
        
        # Plot
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='Word', y='Frequency', hue='Algorithm')
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Top Words Comparison - {language}')
        plt.legend(title='Algorithm')
        plt.tight_layout()
        plt.savefig(f'top_words_comparison_{language}.png')
        plt.close()

    def analyze_word_overlap(self):
        """Analyze overlap of identified words between algorithms and languages."""
        results = {lang: {} for lang in self.languages}
        
        for lang in self.languages:
            rankings = self.get_word_rankings(lang)
            
            # Calculate overlap between algorithms
            for algo1 in rankings:
                for algo2 in rankings:
                    if algo1 < algo2:
                        set1_top = set(word for word, _ in rankings[algo1]['top'])
                        set2_top = set(word for word, _ in rankings[algo2]['top'])
                        overlap_top = len(set1_top & set2_top)
                        
                        set1_bottom = set(word for word, _ in rankings[algo1]['bottom'])
                        set2_bottom = set(word for word, _ in rankings[algo2]['bottom'])
                        overlap_bottom = len(set1_bottom & set2_bottom)
                        
                        results[lang][f"{algo1}_vs_{algo2}"] = {
                            "top_overlap": overlap_top,
                            "top_overlap_percentage": (overlap_top / len(set1_top)) * 100,
                            "bottom_overlap": overlap_bottom,
                            "bottom_overlap_percentage": (overlap_bottom / len(set1_bottom)) * 100
                        }
        
        return results

def main():
    analyzer = WordOrderAnalyzer()
    analyzer.load_results()
    
    # Generate visualizations for each language
    for lang in analyzer.languages:
        print(f"Analyzing {lang}...")
        analyzer.plot_rank_correlation_matrix(lang)
        analyzer.plot_top_words_comparison(lang)
    
    # Analyze word overlap
    overlap_results = analyzer.analyze_word_overlap()
    
    # Save overlap results
    with open('word_overlap_analysis.json', 'w') as f:
        json.dump(overlap_results, f, indent=4)
    
    print("\nAnalysis complete. Generated files:")
    print("- Rank correlation matrices (PNG files)")
    print("- Top words comparisons (PNG files)")
    print("- Word overlap analysis (JSON file)")

if __name__ == "__main__":
    main()