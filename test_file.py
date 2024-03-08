from algorithm.karcas import Algorithm
from algorithm.classic import Algorithm as Clas
from algorithm.parallelModification import Algorithm as Parallel
import json
import os
import copy
import time


N = 100

def test_on_result(algorithm: Algorithm, filename: str):
    with open(f"results/result/{filename}.txt", "w") as file:
        for i in range(4, N + 1):
            name = f"tests/result/test_{i}.json"
            print(f"test {i}, result")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm
                algo.init_graph(data["num_vertex"], data["edges"])
                way_long = 0
                for edge in algo.search_hamilton_cycle():
                    way_long += edge["weight"]
                file.write(f"{way_long}\n")
                # print(f"test,{i}, {filename}, {sum_1}")

def test_on_search(algorithm: Algorithm, filename: str):
    with open(f"results/search/{filename}.txt", "w") as file:
        k = 0
        for i in range(4, N + 1):
            name = f"tests/search/test_{i}.json"
            print(f"test {i}, search")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm
                algo.init_graph(data["num_vertex"], data["edges"])
                way = algo.search_hamilton_cycle()
                if len(way) != 0: k += 1 
                
        file.write(f"{k/(N - 3)}\n")
        
def test_on_time(algorithm: Algorithm, filename: str):
    with open(f"results/time/{filename}.txt", "w") as file:
        for i in range(4, N + 1):
            name = f"tests/time/test_{i}.json"
            print(f"test {i}, time")
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm
                time_start = time.time()
                algo.init_graph(data["num_vertex"], data["edges"])
                way = algo.search_hamilton_cycle()
                time_end = time.time()
                if len(way) != 0: file.write(f"{time_end - time_start}\n")

def test_all(algorithm: Algorithm, filename: str):
    result_file = open(f"results/result/{filename}.txt", "w")
    time_file = open(f"results/time/{filename}.txt", "w")
    search_file = open(f"results/search/{filename}.txt", "w")
    k = 0
    for i in range(4, N + 1):
        name = f"tests/search/test_{i}.json"
        with open(name, "r") as json_file:
            data = json.load(json_file)
            algo = algorithm
            time_start = time.time()
            algo.init_graph(data["num_vertex"], data["edges"])
            way = algo.search_hamilton_cycle()
            time_end = time.time()
        
        print(f"test {i}, all. {filename}: {time_end - time_start}")
        if len(way) != 0: 
            k += 1
            time_file.write(f"{time_end - time_start}\n")

            way_long = 0
            for edge in way:
                way_long += edge["weight"]
            result_file.write(f"{way_long}\n")

    search_file.write(f"{k/(N - 3)}\n")
    result_file.close()
    time_file.close()
    search_file.close()

def start_test(algorithm: Algorithm, filename: str, test):
    test(algorithm, filename)
    print(f"{filename} has completed successfully, {test.__name__}")
    
tests = {"result": test_on_result, "search": test_on_search, "time": test_on_time, "all": test_all}

if __name__ == "__main__":
    start_test(Parallel(), "parallel", tests["all"])
    start_test(Clas(), "classic", tests["all"])