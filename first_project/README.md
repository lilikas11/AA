# First Project

This repository contains the code for the first project in the AA course.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/lilikas/AA/first_project.git
    ```
2. Navigate to the project directory:
    ```sh
    cd first_project
    ```
3. (Optional) Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Python Files

To generate graphs, run:
```sh
python3 graph_generator.py <vertices> [image]
```

- `vertices` is the number of vertices you want to generate the graph with (required).
- `image` is an optional parameter that specifies whether you want to generate a file for the graph.

### Running Exhaustive Search

To run the exhaustive search algorithm, use the following command:
```sh
python3 exhaustive_search.py <filename> [solution]
```

- `<input_file>` is the path to tge graph file.
- `solution` is an optional parameter that specifies whether you want to see the solution on the generated file.



### Running Greedy Search

To run the greedy search algorithm, use the following command:
```sh
python3 greedy_search.py <filename> [solution]
```

- `<filename>` is the path to tge graph file.
- `solution` is an optional parameter that specifies whether you want to see the solution on the generated file.



### Running results for 100 graphs

To run the experiment, use the following command:
```sh
python3 experiment.py 
```

Change the algorithm you want to run on the file

