import matplotlib.pyplot as plt
import json
import re

def extract_vertices_number(filename):
    # Extrai o número de vértices do nome do arquivo (número após "graph_")
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def create_plots(data):
    # Criar 4 subplots (um para cada k)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    axes = {
        '12': ax1,
        '25': ax2,
        '50': ax3,
        '75': ax4
    }
    
    # Cores para cada valor de k
    colors = {
        0.125: 'blue',
        0.25: 'green',
        0.5: 'red',
        0.75: 'purple'
    }
    
    # Para cada subplot (12, 25, 50, 75)
    for graph_size in axes.keys():
        ax = axes[graph_size]
        
        # Preparar dados para este tamanho de grafo
        vertices = []
        times = {k: [] for k in colors.keys()}
        
        # Filtrar e organizar dados
        for filename, measurements in data.items():
            if f'_{graph_size}.' in filename:  # Verificar se é do tamanho correto
                vertex_count = extract_vertices_number(filename)
                vertices.append(vertex_count)
                
                # Organizar tempos de execução por k
                for measurement in measurements:
                    times[measurement['k']].append(measurement['basic_operations_count'])
        
        # Plotar uma linha para cada k
        for k, execution_times in times.items():
            ax.plot(vertices, execution_times, 'o-', label=f'k={k}', color=colors[k])
        
        ax.set_title(f'Grafo tamanho {graph_size}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Basic Operations')
        ax.grid(True)
        ax.legend()
    
    plt.tight_layout()
    plt.show()

# Seus dados
with open('results/greedy_search_results.json', 'r') as f:
    data = json.load(f)

# Criar os gráficos
create_plots(data)