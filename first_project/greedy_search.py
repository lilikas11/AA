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
            # consistent
            edge = tuple(sorted([vertex, neighbor]))
            edges.add(edge)
    return list(edges)


""" ALGORITHM FUNCTIONS """

def calculate_edge_score(edge: Tuple[str, str], uncovered_vertices: Set[str]) -> int:
    """
    Calculate how many uncovered vertices an edge would cover.

    Basic Operations Count:
    2 + 2 = 4
    """
    score = 0
    if edge[0] in uncovered_vertices:
        score += 1
    if edge[1] in uncovered_vertices:
        score += 1
    return score

def find_edge_cover_greedy(graph: Dict[str, List[str]], edges: List[Tuple[str, str]], nr_edge_cover: int) -> Tuple[bool, Set[Tuple[str, str]], int]:
    """
    Find an edge cover using a greedy heuristic.
    The heuristic selects edges that cover the most uncovered vertices at each step.
    
    Returns:
        - bool: Whether a solution was found
        - Set[Tuple[str, str]]: The edge cover if found, empty set otherwise
        - int: Number of decisions made (edges considered)

    Basic Operations Count (dentro do while):
    decisions_made * 10 
    """

    decisions_made = 0
    uncovered_vertices = set(graph.keys())
    edge_cover = set()
    available_edges = edges.copy()
    
    while len(edge_cover) < nr_edge_cover and uncovered_vertices and available_edges:
        # edges that cover most uncovered vertices
        best_edge = None
        best_score = -1
        
        for edge in available_edges:
            decisions_made += 1
            score = calculate_edge_score(edge, uncovered_vertices)
            if score > best_score:
                best_score = score
                best_edge = edge
        
        if best_edge is None or best_score == 0:
            break
            
        # best edge
        edge_cover.add(best_edge)
        available_edges.remove(best_edge)
        
        # update uncovered vertices
        uncovered_vertices.discard(best_edge[0])
        uncovered_vertices.discard(best_edge[1])
    
    # Check if found a valid cover
    success = len(uncovered_vertices) == 0 and len(edge_cover) <= nr_edge_cover
    return success, edge_cover, decisions_made


""" ANALYSIS FUNCTIONS """

def set_variables_and_analyze_performance(filename: str, k: float, edge_cover_save_solution: bool):
    # Load the graph
    graph = load_graph(filename)

    edges = get_all_edges(graph)

    nr_edge_cover = int(len(edges) * k)

    start_time = time.time()

    success, edge_cover, decisions_made = find_edge_cover_greedy(graph, edges, nr_edge_cover)

    execution_time = time.time() - start_time

    # Basic Operations Count:
    # (10 operações por decisão tomada,  if you change the algorithm you must change this number )
    basic_operations_count = decisions_made * 10

    write_results_to_file(filename, k, success, edge_cover, decisions_made, execution_time, basic_operations_count, edge_cover_save_solution)


def write_results_to_file(graph_filename: str, k: int, success: bool, edge_cover: Set[Tuple[str, str]], decisions_made: int, execution_time: float, basic_operations_count: int, edge_cover_save_solution: bool):
    
    results_filename = 'results/greedy_search_results.json'
    
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
        print("Usage: python greedy_search.py <graph_file> [solution]")
        sys.exit(1)

    graph_filename = sys.argv[1]
    
    edge_cover_save_solution = len(sys.argv) == 3 and sys.argv[2] == "solution"

    kvalues = [0.125, 0.25, 0.5, 0.75]

    for k in kvalues:
        set_variables_and_analyze_performance(graph_filename, k, edge_cover_save_solution)