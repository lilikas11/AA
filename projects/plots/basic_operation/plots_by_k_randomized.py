import matplotlib.pyplot as plt
import json
import re

def extract_vertices_number(filename):
    # Extrai o número de vértices do nome do arquivo (número após "graph_")
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def extract_graph_size(filename):
    # Extrai o número após o último underscore e antes do .json
    match = re.search(r'_(\d+)\.json$', filename)
    return match.group(1)

def create_plots(data):
    # Criar 4 subplots (um para cada k)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    k_values = [0.125, 0.25, 0.5, 0.75]
    axes = dict(zip(k_values, [ax1, ax2, ax3, ax4]))
    
    # Cores para cada tamanho de grafo
    colors = {
        '12': 'blue',
        '25': 'green',
        '50': 'red',
        '75': 'purple'
    }
    
    # Organizar dados por tamanho de grafo
    graph_data = {}
    for filename, measurements in data.items():
        size = extract_graph_size(filename)
        vertices = extract_vertices_number(filename)
        
        if size not in graph_data:
            graph_data[size] = {'vertices': [], 'operations': {k: [] for k in k_values}}
        
        graph_data[size]['vertices'].append(vertices)
        for measurement in measurements:
            graph_data[size]['operations'][measurement['k']].append(measurement['basic_operations_count'])
    
    # Para cada valor de k (cada subplot)
    for k in k_values:
        ax = axes[k]
        
        # Plotar uma linha para cada tamanho de grafo
        for size in colors.keys():
            if size in graph_data:
                vertices = sorted(graph_data[size]['vertices'])
                # Ordenar os tempos de acordo com os vértices
                operations = [y for _, y in sorted(zip(graph_data[size]['vertices'], 
                                                graph_data[size]['operations'][k]))]
                ax.plot(vertices, operations, 'o-', 
label=f'Density {size}',                        color=colors[size])
        
        ax.set_title(f'k={k}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Basic Operations')
        ax.grid(True)
        ax.legend()
    
    plt.suptitle('Tempo de Execução por Número de Vértices para Diferentes Valores de k', y=1.02)
    plt.tight_layout()
    plt.show()


with open('results/randomized_search_results.json', 'r') as f:
    data = json.load(f)

# Criar os gráficos
create_plots(data)