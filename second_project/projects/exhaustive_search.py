import itertools
import json
import sys
import time
from typing import Dict, List, Set, Tuple
import math


""" HELP FUNCTIONS """

def load_graph(filename: str) -> Dict[str, List[str]]:
    """Load graph from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def get_all_edges(graph: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    """Get all edges from the graph."""
    edges = set()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            # Ensure consistent ordering of vertices in edge
            edge = tuple(sorted([vertex, neighbor]))
            edges.add(edge)
    return list(edges)


""" ALGORITHM FUNCTIONS """

def is_valid_edge_cover(graph: Dict[str, List[str]], edge_set: Set[Tuple[str, str]]) -> bool:
    """
    Check if the given  set is a valid edge cover.
    An edge cover must incluedgede at least one edge incident to each vertex.

    Basic Operations Count:
    1 + 3*len(edge_set) + 2*len(graph)
    """

    covered_vertices = set()
    
    # Add all vertices that are incident to edges in the edge set
    for edge in edge_set: 
        covered_vertices.add(edge[0])
        covered_vertices.add(edge[1])
    
    # Check if all vertices in the graph are covered
    for vertex in graph.keys():
        if vertex not in covered_vertices:
            return False
            
    return True

def find_edge_cover_exhaustive(graph: Dict[str, List[str]] , edges: List[Tuple[str, str]], nr_edge_cover: int) -> Tuple[bool, Set[Tuple[str, str]], int]:
    """
    Find an edge cover of size k using exhaustive search.
    Returns:
        - bool: Whether a solution was found
        - Set[Tuple[str, str]]: The edge cover if found, empty set otherwise
        - int: Number of configurations tested


    Basic Operations Count (dentro do for):
    3 + is_valid_edge_cover ==
    3 + 1 + 3*len(edge_set) + 2*len(graph) ==
    4 + 3*len(nr_edge_cover) + 2*len(graph)
    """
    configs_tested = 0
    
    # Try all possible combinations of k edges
    for edge_combination in itertools.combinations(edges, nr_edge_cover):
        configs_tested += 1
        edge_set = set(edge_combination)
        
        if is_valid_edge_cover(graph, edge_set):
            return True, edge_set, configs_tested
    
    return False, set(), configs_tested

""" ANALYSIS FUNCTIONS """

def set_variables_and_analyze_performance(filename: str, k: float, edge_cover_save_solution: bool):
    # Load the graph
    graph = load_graph(filename)

    edges = get_all_edges(graph)

    nr_edge_cover = int(len(edges) * k)

    start_time = time.time()
    # Run the algorithm
    success, edge_cover, configs_tested = find_edge_cover_exhaustive(graph, edges, nr_edge_cover)

    execution_time = time.time() - start_time

    # Basic Operations Count:
    # ( This number is counted in the alforithm functions, if you change the algorithm you must change this number )
    basic_operations_count = configs_tested * 4 + 3*nr_edge_cover + 2*len(graph)

    write_results_to_file(filename, k, success, edge_cover, configs_tested, execution_time, basic_operations_count, edge_cover_save_solution)



def write_results_to_file(graph_filename: str, k: int, success: bool, edge_cover: Set[Tuple[str, str]], configs_tested: int, execution_time: float, basic_operations_count: int, edge_cover_save_solution: bool):
    
    results_filename = 'results/exhaustive_search_results.json'
    
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
        'configs_tested': configs_tested,
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
        print("Usage: python greedy_search.py <graph_file> [solution]")
        sys.exit(1)

    graph_filename = sys.argv[1]
    
    edge_cover_save_solution = len(sys.argv) == 3 and sys.argv[2] == "solution"


    kvalues = [0.125, 0.25, 0.5, 0.75]

    for k in kvalues:
        set_variables_and_analyze_performance(graph_filename, k, edge_cover_save_solution)
