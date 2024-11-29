import json
import math

with open('results/greedy_search_results.json', 'r') as f:
    data = json.load(f)

total_operations = 0
total_execution_time = 0

# Iterar sobre cada grafo e acumular operações e tempo
for graph, results in data.items():
    for entry in results:
        total_operations += entry["basic_operations_count"]
        total_execution_time += entry["execution_time"]

# Calcular operações por segundo
if total_execution_time > 0:
    operations_per_second = total_operations / total_execution_time
    # Calcular a ordem de grandeza como 10^n
    order_of_magnitude = math.floor(math.log10(operations_per_second))
    print(f"The order of magnitude of operations per second is: 10^{order_of_magnitude}")
else:
    print("Execution time is zero, cannot calculate operations per second.")
