import json

# Carregar os dados dos arquivos JSON
with open('/home/lilikas11/Curso/AA/first_project/results/exhaustive_search_results.json', 'r') as f:
    exhaustive_data = json.load(f)

with open('/home/lilikas11/Curso/AA/first_project/results/randomized_search_results.json', 'r') as f:
    greedy_data = json.load(f)

# Função para comparar os resultados dos algoritmos
def compare_algorithms(exhaustive, greedy):
    comparison_results = {}
    
    # Iterar sobre cada gráfico nos resultados exaustivos
    for graph, exhaustive_results in exhaustive.items():
        greedy_results = greedy.get(graph, [])

        # Verificar se o gráfico está nos dois algoritmos
        if not greedy_results:
            print(f"Graph {graph} not found in greedy results.")
            continue

        # Comparar resultados para cada valor de k
        comparison_results[graph] = []
        for ex_result, gr_result in zip(exhaustive_results, greedy_results):
            result = {
                "k": ex_result["k"],
                "exhaustive_success": ex_result["success"],
                "greedy_success": gr_result["success"],
                "false_positive": False,
                "false_negative": False
            }

            # Determinar falso positivo ou falso negativo
            if ex_result["success"] != gr_result["success"]:
                if gr_result["success"] and not ex_result["success"]:
                    result["false_positive"] = True
                elif not gr_result["success"] and ex_result["success"]:
                    result["false_negative"] = True

            comparison_results[graph].append(result)

    return comparison_results

# Comparar e exibir resultados
comparison = compare_algorithms(exhaustive_data, greedy_data)

# Exibir apenas resultados com falsos positivos ou falsos negativos
for graph, results in comparison.items():
    false_results = [result for result in results if result["false_positive"] or result["false_negative"]]
    if false_results:
        print(f"Results for {graph}:")
        for result in false_results:
            print(f"  k = {result['k']}")
            print(f"    Exhaustive Success: {result['exhaustive_success']}")
            print(f"    Greedy Success: {result['greedy_success']}")
            if result["false_positive"]:
                print("    False Positive detected!")
            if result["false_negative"]:
                print("    False Negative detected!")
            print("\n")
