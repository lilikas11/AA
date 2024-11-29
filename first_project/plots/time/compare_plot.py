import matplotlib.pyplot as plt
import json
import re
from collections import defaultdict

def extract_vertices_number(filename):
    match = re.search(r'graph_(\d+)', filename)
    return int(match.group(1))

def create_comparison_plots(greedy_data, exhaustive_data):
    # Configurar subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
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
        times_greedy = []
        vertices_exhaustive = []
        times_exhaustive = []
        
        # Coletar dados do greedy
        for filename, measurements in greedy_data.items():
            if '_75.' in filename:  # Apenas grafos de tamanho 75
                vertices = extract_vertices_number(filename)
                for measurement in measurements:
                    if measurement['k'] == k:
                        vertices_greedy.append(vertices)
                        times_greedy.append(measurement['execution_time'])
        
        # Coletar dados do exhaustive
        for filename, measurements in exhaustive_data.items():
            if '_75.' in filename:  # Apenas grafos de tamanho 75
                vertices = extract_vertices_number(filename)
                for measurement in measurements:
                    if measurement['k'] == k:
                        vertices_exhaustive.append(vertices)
                        times_exhaustive.append(measurement['execution_time'])
        
        ax = axes[k]
        
        # Ordenar os pontos pelo número de vértices
        if vertices_greedy:
            points_greedy = sorted(zip(vertices_greedy, times_greedy))
            vertices_greedy, times_greedy = zip(*points_greedy)
            ax.plot(vertices_greedy, times_greedy, 'o-', 
                   label='Greedy', color=colors['greedy'])
        
        if vertices_exhaustive:
            points_exhaustive = sorted(zip(vertices_exhaustive, times_exhaustive))
            vertices_exhaustive, times_exhaustive = zip(*points_exhaustive)
            ax.plot(vertices_exhaustive, times_exhaustive, 'o-', 
                   label='Exhaustive', color=colors['exhaustive'])
        
        ax.set_title(f'k={k}')
        ax.set_xlabel('Vertices number')
        ax.set_ylabel('Execution time (s)')
        ax.grid(True)
        ax.legend()
        
        # Se houver grande diferença na escala, usar escala logarítmica
        if vertices_exhaustive and vertices_greedy:
            max_time = max(max(times_exhaustive), max(times_greedy))
            min_time = min(min(times_exhaustive), min(times_greedy))
            if max_time / min_time > 100:  # Se a diferença for maior que 2 ordens de magnitude
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