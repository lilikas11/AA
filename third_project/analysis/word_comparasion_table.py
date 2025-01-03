import json
from pathlib import Path
import pandas as pd
import numpy as np
from tabulate import tabulate

class TopWordsAnalyzer:
    def __init__(self, results_dir="results"):
        self.results_dir = Path(results_dir)
        self.languages = ["English", "Esperanto", "Finnish", "French", "German", "Italian"]
        self.algorithms = {
            "exact_counter": "Exact",
            "lossy_count_stream": "Lossy",
            "decreasing_prob_counter": "Prob"
        }
        
    def load_results(self):
        """Load results for all algorithms."""
        self.results = {}
        for algo in self.algorithms.keys():
            file_path = self.results_dir / f"{algo}_results.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    self.results[algo] = json.load(f)
    
    def get_top_words(self, algorithm: str, language: str) -> list:
        """Extract top 10 words for a specific algorithm and language."""
        filename = f"processed_{language}.txt"
        
        if algorithm == "exact_counter":
            if filename in self.results[algorithm]:
                return [word for word, _ in self.results[algorithm][filename]["most_common"][:10]]
            
        elif algorithm == "lossy_count_stream":
            if filename in self.results[algorithm]:
                return [word for word, _ in self.results[algorithm][filename]["n_value_results"]["10"]["most_frequent_items"]]
            
        elif algorithm == "decreasing_prob_counter":
            if filename in self.results[algorithm]:
                # Get first trial results
                trial = self.results[algorithm][filename]["trial_results"][0]
                return [word for word, _ in trial["most_common"][:10]]
        
        return ["-"] * 10  # Return placeholder if data not found
    
    def create_latex_table(self):
        """Create a LaTeX table comparing top words across languages and algorithms."""
        # Create document header
        latex_doc = [
            "\\documentclass{article}",
            "\\usepackage[landscape]{geometry}",
            "\\usepackage{longtable}",
            "\\usepackage{booktabs}",
            "\\begin{document}",
            "\\begin{longtable}{lrrrrrrrrrrr}"
        ]
        
        for language in self.languages:
            # Add section title
            latex_doc.extend([
                "\\multicolumn{12}{l}{\\textbf{" + language + "}} \\\\",
                "\\toprule",
                "Algorithm & 1st & 2nd & 3rd & 4th & 5th & 6th & 7th & 8th & 9th & 10th \\\\"
                "\\midrule"
            ])
            
            # Add data for each algorithm
            for algo_key, algo_name in self.algorithms.items():
                words = self.get_top_words(algo_key, language)
                row = [algo_name] + words
                latex_doc.append(" & ".join(row) + " \\\\")
            
            latex_doc.append("\\bottomrule")
            latex_doc.append("\\addlinespace[1em]")
        
        # Close document
        latex_doc.extend([
            "\\end{longtable}",
            "\\end{document}"
        ])
        
        # Write to file
        with open("top_words_comparison.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(latex_doc))
    
    def create_markdown_table(self):
        """Create a markdown table comparing top words across languages and algorithms."""
        md_output = []
        
        for language in self.languages:
            # Add language header
            md_output.append(f"\n## {language}\n")
            
            # Create headers
            headers = ["Algorithm"] + [f"{i+1}st" for i in range(10)]
            
            # Get data for each algorithm
            rows = []
            for algo_key, algo_name in self.algorithms.items():
                words = self.get_top_words(algo_key, language)
                rows.append([algo_name] + words)
            
            # Create table
            table = tabulate(rows, headers=headers, tablefmt="pipe")
            md_output.append(table)
            md_output.append("\n")
        
        # Write to file
        with open("top_words_comparison.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_output))
    
    def create_html_table(self):
        """Create an HTML table comparing top words across languages and algorithms."""
        html_output = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<style>",
            "table { border-collapse: collapse; width: 100%; }",
            "th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }",
            "th { background-color: #f2f2f2; }",
            "h2 { color: #333; margin-top: 20px; }",
            ".language-section { margin-bottom: 30px; }",
            "</style>",
            "</head>",
            "<body>"
        ]
        
        for language in self.languages:
            html_output.extend([
                f'<div class="language-section">',
                f"<h2>{language}</h2>",
                "<table>",
                "<tr>",
                "<th>Algorithm</th>"
            ])
            
            # Add headers
            html_output.extend([f"<th>{i+1}st</th>" for i in range(10)])
            html_output.append("</tr>")
            
            # Add data for each algorithm
            for algo_key, algo_name in self.algorithms.items():
                words = self.get_top_words(algo_key, language)
                html_output.append("<tr>")
                html_output.append(f"<td>{algo_name}</td>")
                html_output.extend([f"<td>{word}</td>" for word in words])
                html_output.append("</tr>")
            
            html_output.append("</table>")
            html_output.append("</div>")
        
        html_output.extend([
            "</body>",
            "</html>"
        ])
        
        # Write to file
        with open("top_words_comparison.html", "w", encoding="utf-8") as f:
            f.write("\n".join(html_output))

def main():
    analyzer = TopWordsAnalyzer()
    analyzer.load_results()
    
    # Generate all formats
    print("Generating comparison tables...")
    analyzer.create_latex_table()
    analyzer.create_markdown_table()
    analyzer.create_html_table()
    
    print("\nFiles generated:")
    print("- top_words_comparison.tex (LaTeX format)")
    print("- top_words_comparison.md (Markdown format)")
    print("- top_words_comparison.html (HTML format)")

if __name__ == "__main__":
    main()