import random
import json

def gamilton_generation_result(number: int)->None:
    for i in range(number - 3):
        N = i + 4
        data = {"num_vertex": N, "vertexes": [], "edges": []}
        coordinate_x = set()
        coordinate_y = set()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    data["edges"].append({"from": i, "to": j, "weight": random.randint(1, 100)})
        k = 0
        while k < N:
            coor = (random.randint(1, 600), random.randint(1, 400))
            if coor[0] in coordinate_x: continue
            if coor[1] in coordinate_y: continue
            coordinate_x.add(coor[0])
            coordinate_y.add(coor[1])
            data["vertexes"].append({"x": coor[0], "y": coor[1]})
            k += 1


        with open(f"tests/result/test_{N}.json", "w") as file:
            json.dump(data, file)
        
def gamilton_generation_search(number: int):
    for i in range(number - 3):
        N = i + 4
        data = {"num_vertex": N, "vertexes": [], "edges": []}
        coordinate_x = set()
        coordinate_y = set()
        vertexes = [x + 1 for x in range(N)]
        for i in range(1, N):
            data["edges"].append({"from": i, "to": i + 1, "weight": random.randint(1, 100)})
        
        data["edges"].append({"from": N, "to": 1, "weight": random.randint(1, 100)})    
        
            
        k = 0
        while k < N:
            coor = (random.randint(1, 600), random.randint(1, 400))
            if coor[0] in coordinate_x: continue
            if coor[1] in coordinate_y: continue
            coordinate_x.add(coor[0])
            coordinate_y.add(coor[1])
            data["vertexes"].append({"x": coor[0], "y": coor[1]})
            k += 1

        k = 0
        added_edges = set()
        end = random.randint(0, N * (N - 1) - N)
        
        while k < end:
            edge = (random.randint(1, N), random.randint(1, N))
            if not edge in added_edges and edge[0] != edge[1]:
                added_edges.add(edge)
                k += 1
                data["edges"].append({"from": edge[0], "to": edge[1], "weight": random.randint(1, 100)})  

        with open(f"tests/search/test_{N}.json", "w") as file:
            json.dump(data, file)
            
def gamilton_generation_time(number: int):
    for i in range(number - 3):
        N = i + 4
        data = {"num_vertex": N, "vertexes": [], "edges": []}
        coordinate_x = set()
        coordinate_y = set()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    data["edges"].append({"from": i, "to": j, "weight": random.randint(1, 100)})
        k = 0
        while k < N:
            coor = (random.randint(1, 600), random.randint(1, 400))
            if coor[0] in coordinate_x: continue
            if coor[1] in coordinate_y: continue
            coordinate_x.add(coor[0])
            coordinate_y.add(coor[1])
            data["vertexes"].append({"x": coor[0], "y": coor[1]})
            k += 1


        with open(f"tests/time/test_{N}.json", "w") as file:
            json.dump(data, file)
        

def all_tests(number: int):
    gamilton_generation_result(number)
    gamilton_generation_search(number)
    gamilton_generation_time(number)

def main():
    type_tests = input()
    n = int(input())
    type_generation = {"result": gamilton_generation_result,
                 "search": gamilton_generation_search, 
                 "time": gamilton_generation_time,
                 "all": all_tests
                 }
    type_generation[type_tests](n)

if __name__ == "__main__":
    main()
