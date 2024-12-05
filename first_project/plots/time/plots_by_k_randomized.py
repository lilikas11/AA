import matplotlib.pyplot as plt
import json
import re

def extract_vertices_number(filename):
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def extract_graph_size(filename):
    match = re.search(r'_(\d+)\.json$', filename)
    return match.group(1)

def create_plots(data):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    k_values = [0.125, 0.25, 0.5, 0.75]
    axes = dict(zip(k_values, [ax1, ax2, ax3, ax4]))
    
    colors = {
        '12': 'blue',
        '25': 'green',
        '50': 'red',
        '75': 'purple'
    }
    
    graph_data = {}
    for filename, measurements in data.items():
        size = extract_graph_size(filename)
        vertices = extract_vertices_number(filename)
        
        if size not in graph_data:
            graph_data[size] = {'vertices': [], 'times': {k: [] for k in k_values}}
        
        graph_data[size]['vertices'].append(vertices)
        for measurement in measurements:
            graph_data[size]['times'][measurement['k']].append(measurement['execution_time'])
    
    for k in k_values:
        ax = axes[k]
        
        for size in colors.keys():
            if size in graph_data:
                vertices = sorted(graph_data[size]['vertices'])
                times = [y for _, y in sorted(zip(graph_data[size]['vertices'], 
                                                graph_data[size]['times'][k]))]
                ax.plot(vertices, times, 'o-', 
                       label=f'Density {size}', 
                       color=colors[size])
        
        ax.set_title(f'k={k}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Execution time (s)')
        ax.grid(True)
        ax.legend()
    
    plt.suptitle('Tempo de Execução por Número de Vértices para Diferentes Valores de k', y=1.02)
    plt.tight_layout()
    plt.show()

# with open('results/greedy_search_results.json', 'r') as f:
#     data = json.load(f)

with open('results/randomized_search_results.json', 'r') as f:
    data = json.load(f)

# Criar os gráficos
create_plots(data)