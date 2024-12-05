import matplotlib.pyplot as plt
import json
import re
import numpy as np

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
    
    # Cores para cada tamanho de grafo e status de sucesso
    colors = {
        '12': {'success': 'green', 'failure': 'red'},
    }
    
    # Organizar dados por tamanho de grafo
    graph_data = {}
    for filename, measurements in data.items():
        size = extract_graph_size(filename)
        vertices = extract_vertices_number(filename)
        
        if size not in graph_data:
            graph_data[size] = {
                'vertices': set(), 
                'operations': {k: {'success': {}, 'failure': {}} for k in k_values}
            }
        
        graph_data[size]['vertices'].add(vertices)
        
        for measurement in measurements:
            k = measurement['k']
            success = measurement['success']
            status = 'success' if success else 'failure'
            
            if vertices not in graph_data[size]['operations'][k][status]:
                graph_data[size]['operations'][k][status][vertices] = []
            
            graph_data[size]['operations'][k][status][vertices].append(measurement['basic_operations_count'])
    
    # Para cada valor de k (cada subplot)
    for k in k_values:
        ax = axes[k]
        
        # Plotar uma linha para cada tamanho de grafo, separando sucesso e falha
        for size in colors.keys():
            if size in graph_data:
                # Calcular valores médios para cada número de vértices
                vertices = sorted(graph_data[size]['vertices'])
                
                # Sucesso
                success_operations = []
                for v in vertices:
                    if v in graph_data[size]['operations'][k]['success']:
                        success_mean = np.mean(graph_data[size]['operations'][k]['success'][v])
                        success_operations.append(success_mean)
                    else:
                        success_operations.append(np.nan)
                
                # Plotar apenas se houver dados de sucesso
                if any(not np.isnan(x) for x in success_operations):
                    ax.plot(vertices, success_operations, 'o-', 
                            label=f'Density {size} (Success)', 
                            color=colors[size]['success'], 
                            linestyle='-')
                
                # Falha
                failure_operations = []
                for v in vertices:
                    if v in graph_data[size]['operations'][k]['failure']:
                        failure_mean = np.mean(graph_data[size]['operations'][k]['failure'][v])
                        failure_operations.append(failure_mean)
                    else:
                        failure_operations.append(np.nan)
                
                # Plotar apenas se houver dados de falha
                if any(not np.isnan(x) for x in failure_operations):
                    ax.plot(vertices, failure_operations, 'o-', 
                            label=f'Density {size} (Failure)', 
                            color=colors[size]['failure'], 
                            linestyle='--')
        
        ax.set_title(f'k={k}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Basic Operations')
        ax.grid(True)
        ax.legend()
    
    plt.suptitle('Tempo de Execução por Número de Vértices para Diferentes Valores de k\n(Sucesso vs Falha)', y=1.02)
    plt.tight_layout()
    plt.show()


with open('results/randomized_search_results.json', 'r') as f:
    data = json.load(f)

# Criar os gráficos
create_plots(data)