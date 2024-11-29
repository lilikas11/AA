import random
import networkx as nx
import json
import os
import sys
import matplotlib.pyplot as plt


seed = 108713
random.seed(seed)

def generate_vertex(existing_vertices):
    while True:
        x, y = random.randint(1, 1000), random.randint(1, 1000)
        if not is_too_close((x, y), existing_vertices):
            return (x, y)
        
def is_too_close(vertex, existing_vertices):
    for ex in existing_vertices:
        if (vertex[0] - ex[0])**2 + (vertex[1] - ex[1])**2 < 4:
            return True
    return False

def generate_edges(num_vertices, edge_percent, vertices):
    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = int(max_edges * edge_percent)
    all_possible_edges = [(vertices[i], vertices[j]) for i in range(num_vertices) for j in range(i+1, num_vertices)]
    edges = random.sample(all_possible_edges, num_edges)
    
    return edges

def generate_graph(num_vertices, edge_percent):
    G = nx.Graph()
    vertices = []
    for _ in range(num_vertices):
        new_vertex = generate_vertex(vertices)
        vertices.append(new_vertex)
        G.add_node(new_vertex)

    edges = generate_edges(num_vertices, edge_percent, vertices)
    G.add_edges_from(edges)

    return G


def save_graph(G, adjacency_list, size, edge_percent, folder, generate_image):
    filename = os.path.join(folder, f'graph_{str(size).zfill(3)}_{int(edge_percent*100)}.json')
    # json with adjacency list
    with open(filename, 'w') as file:
        json.dump(adjacency_list, file, indent=4)

    if generate_image:
        # image with graph
        plt.figure(figsize=(10, 10))
        pos = {node: node for node in G.nodes()}
        nx.draw(G, pos, with_labels=True, node_size=500, font_size=10)
        plt.title(f"Graph with {size} vertices and {int(edge_percent*100)}% edges")
        plt.savefig(os.path.join(folder, f"graph_{str(size).zfill(3)}_{int(edge_percent*100)}.png"))
        plt.close()


def generate_and_save_graphs(size, edge_percents, folder, generate_image):
    if not os.path.exists(folder):
        os.makedirs(folder)
    

    for edge_percent in edge_percents:
        G = generate_graph(size, edge_percent)
        # {node: [neighbor1, neighbor2, ...]}
        adjacency_list = {str(node): [str(neighbor) for neighbor in G.neighbors(node)] for node in G.nodes()}
        save_graph(G, adjacency_list, size, edge_percent, folder, generate_image)


if __name__ == '__main__' :
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 graph_generator.py <vertices> [image]")
        sys.exit(1)

    size = int(sys.argv[1])
    generate_image = len(sys.argv) == 3 and sys.argv[2] == "image"

    edge_percents = [0.125, 0.25, 0.5, 0.75]
    folder = 'graphs'

    generate_and_save_graphs(size, edge_percents, folder, generate_image)