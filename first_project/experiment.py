import sys
import os
import time
import subprocess

def generate_graph(vertices):
    vertices = 4
    while vertices <= 100:
        os.system(f"python3 graph_generator.py {vertices}")
        vertices += 1

def run_exhaustive_search():
    edge_probability = [12, 25, 50, 75]

    for probability in edge_probability:
        vertices = 4
        while vertices <= 100:
            try:
                subprocess.run(
                    f"python3 exhaustive_search.py graphs/graph_{str(vertices).zfill(3)}_{probability}.json",
                    shell=True,
                    timeout=60
                )
            except subprocess.TimeoutExpired:
                print(f"Graph with {vertices} vertices and {probability}% edges took more than 1 minute to run")
                break
            
            vertices += 1

def run_greedy_search():
    edge_probability = [12, 25, 50, 75]

    for probability in edge_probability:
        vertices = 4
        while vertices <= 100:
            try:
                subprocess.run(
                    f"python3 greedy_search.py graphs/graph_{str(vertices).zfill(3)}_{probability}.json",
                    shell=True,
                    timeout=60
                )
            except subprocess.TimeoutExpired:
                print(f"Graph with {vertices} vertices and {probability}% edges took more than 1 minute to run")
                break
            
            vertices += 1

if __name__ == "__main__":
    run_greedy_search()
