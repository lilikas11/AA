import json
import sys
import time
import random
from typing import Dict, List, Set, Tuple

def load_graph(filename: str) -> Dict[str, List[str]]:
    """Load graph from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def get_all_edges(graph: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    """Get all edges from the graph."""
    edges = set()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([vertex, neighbor]))
            edges.add(edge)
    return list(edges)

""" ALGORITHM FUNCTIONS """

def find_edge_cover_randomized(graph: Dict[str, List[str]], edges: List[Tuple[str, str]], 
                                nr_edge_cover: int, max_iterations: int = 1000) -> Tuple[bool, Set[Tuple[str, str]], int]:
    """
    Find an edge cover using a randomized heuristic.
    
    Returns:
        - bool: Whether a solution was found
        - Set[Tuple[str, str]]: The edge cover if found, empty set otherwise
        - int: Number of decisions made
    """
    decisions_made = 0
    
    for _ in range(max_iterations):
        # reset for each iteration
        edge_cover = set()
        uncovered_vertices = set(graph.keys())
        available_edges = edges.copy()
        
        while uncovered_vertices and available_edges:
            decisions_made += 1
            
            # randomly select an edge with bias covering more uncovered vertices
            weighted_edges = [
                (edge, sum(1 for v in edge if v in uncovered_vertices)) 
                for edge in available_edges
            ]
            
            # Probabilistic edge selection with weight
            total_weight = sum(weight for _, weight in weighted_edges)
            if total_weight == 0:
                break
            
            probabilities = [weight / total_weight for _, weight in weighted_edges]
            selected_edge = random.choices([edge for edge, _ in weighted_edges], 
                                           weights=probabilities)[0]
            
            edge_cover.add(selected_edge)
            available_edges.remove(selected_edge)
            
            # Update uncovered vertices
            uncovered_vertices.discard(selected_edge[0])
            uncovered_vertices.discard(selected_edge[1])
        
        # Check if found a valid cover
        if len(uncovered_vertices) == 0 and len(edge_cover) <= nr_edge_cover:
            return True, edge_cover, decisions_made
    
    return False, set(), decisions_made

""" ANALYSIS FUNCTIONS """

def set_variables_and_analyze_performance(filename: str, k: float, edge_cover_save_solution: bool):
    # Load the graph
    graph = load_graph(filename)
    edges = get_all_edges(graph)
    nr_edge_cover = int(len(edges) * k)

    start_time = time.time()
    success, edge_cover, decisions_made = find_edge_cover_randomized(graph, edges, nr_edge_cover)
    execution_time = time.time() - start_time

    basic_operations_count = decisions_made * 10

    write_results_to_file(filename, k, success, edge_cover, decisions_made, 
                           execution_time, basic_operations_count, edge_cover_save_solution)

def write_results_to_file(graph_filename: str, k: float, success: bool, 
                           edge_cover: Set[Tuple[str, str]], decisions_made: int, 
                           execution_time: float, basic_operations_count: int, 
                           edge_cover_save_solution: bool):
    results_filename = 'results/randomized_search_results.json'
    
    try:
        with open(results_filename, 'r') as f:
            results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        results = {}

    if graph_filename not in results:
        results[graph_filename] = []

    result_entry = {
        'k': k,
        'success': success,
        'decisions_made': decisions_made,
        'execution_time': execution_time,
        'basic_operations_count': basic_operations_count
    }

    if edge_cover_save_solution:
        result_entry['edge_cover'] = list(edge_cover)

    results[graph_filename].append(result_entry)

    with open(results_filename, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python randomized_search.py <graph_file> [solution]")
        sys.exit(1)

    graph_filename = sys.argv[1]
    edge_cover_save_solution = len(sys.argv) == 3 and sys.argv[2] == "solution"

    kvalues = [0.125, 0.25, 0.5, 0.75]

    for k in kvalues:
        set_variables_and_analyze_performance(graph_filename, k, edge_cover_save_solution)