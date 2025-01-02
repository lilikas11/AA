import matplotlib.pyplot as plt
import json
import re

def extract_vertices_number(filename):
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def create_plots(data):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    axes = {
        '12': ax1,
        '25': ax2,
        '50': ax3,
        '75': ax4
    }
    
    colors = {
        0.125: 'blue',
        0.25: 'green',
        0.5: 'red',
        0.75: 'purple'
    }
    
    for graph_size in axes.keys():
        ax = axes[graph_size]
        
        vertices = []
        times = {k: [] for k in colors.keys()}
        
        for filename, measurements in data.items():
            if f'_{graph_size}.' in filename:
                vertex_count = extract_vertices_number(filename)
                vertices.append(vertex_count)
                
                for measurement in measurements:
                    times[measurement['k']].append((vertex_count, measurement['basic_operations_count']))
        
        for k, execution_times in times.items():
            execution_times.sort()  # Ordenar por número de vértices
            vertices_sorted, operations_sorted = zip(*execution_times)
            ax.plot(vertices_sorted, operations_sorted, 'o-', label=f'k={k}', color=colors[k])
            
        ax.set_title(f'Grafo tamanho {graph_size}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Basic Operations')
        ax.grid(True)
        ax.legend()
    
    plt.tight_layout()
    plt.show()

with open('results/randomized_search_results.json', 'r') as f:
    data = json.load(f)

create_plots(data)
