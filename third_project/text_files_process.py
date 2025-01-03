import os
import re
import nltk
from nltk.corpus import stopwords
import string
import sys

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    start_pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"
    end_pattern = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"
    start_match = re.search(start_pattern, text)
    end_match = re.search(end_pattern, text)

    if start_match and end_match:
        text = text[start_match.end():end_match.start()]
    elif start_match:
        text = text[start_match.end():]
    elif end_match:
        text = text[:end_match.start()]

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)
    return cleaned_text

def main():
    if len(sys.argv) < 2:
        print("Usage: python text_files_process.py <path_to_text_file>")
        return

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    processed_text = clean_text(file_path)
    output_dir = "processed_files"
    os.makedirs(output_dir, exist_ok=True)
    input_filename = os.path.basename(file_path)
    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(processed_text)

    print(f"Processed text saved in: {output_path}")

if __name__ == "__main__":
    main()
