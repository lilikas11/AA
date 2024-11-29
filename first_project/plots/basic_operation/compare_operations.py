import matplotlib.pyplot as plt
import json
import re


def extract_vertices_number(filename):
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def create_comparison_plots(greedy_data, exhaustive_data):
    # Configurar subplots
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    k_values = [0.125, 0.25, 0.5, 0.75]
    axes = dict(zip(k_values, [ax1, ax2, ax3, ax4]))
    
    # Cores para cada algoritmo
    colors = {
        'greedy': 'blue',
        'exhaustive': 'red'
    }
    
    # Para cada valor de k
    for k in k_values:
        vertices_greedy = []
        operations_greedy = []
        vertices_exhaustive = []
        operations_exhaustive = []
        
        # Coletar dados do greedy
        for filename, measurements in greedy_data.items():
            if '_25.' in filename:  # Apenas grafos de tamanho 75
                vertices = extract_vertices_number(filename)
                for measurement in measurements:
                    if measurement['k'] == k:
                        vertices_greedy.append(vertices)
                        operations_greedy.append(measurement['basic_operations_count'])
        
        # Coletar dados do exhaustive
        for filename, measurements in exhaustive_data.items():
            if '_25.' in filename:  # Apenas grafos de tamanho 75
                vertices = extract_vertices_number(filename)
                for measurement in measurements:
                    if measurement['k'] == k:
                        vertices_exhaustive.append(vertices)
                        operations_exhaustive.append(measurement['basic_operations_count'])
        
        ax = axes[k]
        
        # Ordenar os pontos pelo número de vértices
        if vertices_greedy:
            points_greedy = sorted(zip(vertices_greedy, operations_greedy))
            vertices_greedy, operations_greedy = zip(*points_greedy)
            ax.plot(vertices_greedy, operations_greedy, 'o-', 
                   label='Greedy', color=colors['greedy'])
        
        if vertices_exhaustive:
            points_exhaustive = sorted(zip(vertices_exhaustive, operations_exhaustive))
            vertices_exhaustive, operations_exhaustive = zip(*points_exhaustive)
            ax.plot(vertices_exhaustive, operations_exhaustive, 'o-', 
                   label='Exhaustive', color=colors['exhaustive'])
        
        ax.set_title(f'k={k}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Basic Operations')
        ax.grid(True)
        ax.legend()
        
        # Se houver grande diferença na escala, usar escala logarítmica
        if vertices_exhaustive and vertices_greedy:
            max_operation = max(max(operations_exhaustive), max(operations_greedy))
            min_operation = min(min(operations_exhaustive), min(operations_greedy))
            if min_operation > 0 and max_operation / min_operation > 100:  # Se a diferença for maior que 2 ordens de magnitude
                ax.set_yscale('log')
    
    plt.suptitle('Comparação Greedy vs Exhaustive (Grafo tamanho 75)')
    plt.tight_layout()
    plt.show()


# Exemplo de como usar:
# Seus dados do algoritmo 
with open('results/greedy_search_results.json', 'r') as f:
    greedy_data = json.load(f)

with open('results/exhaustive_search_results.json', 'r') as f:
    exhaustive_data = json.load(f)

# Criar os gráficos
create_comparison_plots(greedy_data, exhaustive_data)