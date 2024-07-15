from algorithm.abstract import Algorithm as AbcAlgorithm
from algorithm.Ant import Ant
import networkx as nx
import random
import multiprocessing as mp
import sys

N_POCESS = 4
N_DROB = 16
        

class Algorithm(AbcAlgorithm):
    def __init__(self) -> None:
        #начальные данные
        self._graph = nx.DiGraph()
        self._global_pheromon = nx.DiGraph()
        self._sum_local_pheromon = nx.DiGraph()
        
        self.iteration = 50
        self.const_for_pheromon = 1
        self.num_ant = N_POCESS*N_DROB
        
        self.importance_pheromon = 1
        self.importance_long = 3
        self.evaporation_rate = 0.1
        
    def init_graph(self, vertex_num: int, edges: list[dict])->None:
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        self._global_pheromon.add_nodes_from([(x+1) for x in range(vertex_num)])
        self._sum_local_pheromon.add_nodes_from([(x+1) for x in range(vertex_num)])
        
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight=edge["weight"])
            self._global_pheromon.add_edge(edge["from"], edge["to"], weight=1)
            self._sum_local_pheromon.add_edge(edge["from"], edge["to"], weight=0)
            
    def search_hamilton_cycle(self) -> list[dict]:
        input_process = mp.Queue()
        results = mp.Queue()
        updates = [
            mp.Queue()
            for _ in range(N_POCESS)
        ]

        processes = [
            mp.Process(target=self.process_search_way, args=(input_process, results, updates[i]))
            for i in range(N_POCESS)
            ]
        
        for process in processes:
            process.start()
        
        for _ in range(self.iteration):
            ants = [Ant(random.randint(1, len(self._graph.nodes)))
                    for _ in range(self.num_ant)
                    ]
            
            for i in range(N_DROB, self.num_ant + 1, N_DROB):
                input_process.put(ants[i-16:i])
            
            ants = []
            quality_results = 0
            while quality_results < 4:
                if not results.empty():
                    ants += results.get()
                    quality_results += 1
                    
            k = 0
            while k < len(ants):
                if ants[k].current_vertex == 0: ants.pop(k)
                else: k += 1
            self.update_sum_local_pheromon(ants)
            self.update_global_pheromon()

            for i in range(N_POCESS):
                updates[i].put(self._global_pheromon)
            
        min_way = min(ants, key=lambda x: self.way_long(x.way)).way
        
        min_way = [{"from": min_way[i],
                    "to": min_way[(i + 1) % len(min_way)],
                    "weight": self._graph[min_way[i]][min_way[(i + 1) % len(min_way)]]["weight"]}
                   for i in range(len(min_way))
                   ]
            
        for process in processes:
            process.terminate()

        if len(ants) > 0:  
            min_way = min(ants, key=lambda x: self.way_long(x.way)).way
        
            min_way = [{"from": min_way[i],
                        "to": min_way[(i + 1) % len(min_way)],
                        "weight": self._graph[min_way[i]][min_way[(i + 1) % len(min_way)]]["weight"]}
                       for i in range(len(min_way))
                       ]
            
            return min_way
        else:
            return []
    
    def process_search_way(self, input: mp.Queue, output: mp.Queue, update_global: mp.Queue) -> None:
        while True:
            if not input.empty():
                output.put([self.search_way_for_ant(ant) for ant in input.get()].copy())

            if not update_global.empty():
                self._global_pheromon = update_global.get()
    
    def update_global_pheromon(self) -> None:
        for edge in self._graph.edges:
            self._global_pheromon[edge[0]][edge[1]]["weight"] = (1 - self.evaporation_rate) * \
                self._global_pheromon[edge[0]][edge[1]]["weight"] + self._sum_local_pheromon[edge[0]][edge[1]]["weight"]
    
    def update_sum_local_pheromon(self, ants: list) -> None:
        for edge in self._graph.edges:
            self._sum_local_pheromon[edge[0]][edge[1]]["weight"] = 0
        
        for ant in ants:
            for i in range(1, len(ant.way) + 1):
                self._sum_local_pheromon
                self._sum_local_pheromon[ant.way[i-1]][ant.way[i % len(ant.way)]]["weight"] +=  \
                    self.const_for_pheromon / self._graph[ant.way[i-1]][ant.way[i % len(ant.way)]]["weight"]
        
                
    
    def new_vertex(self, current_vertex: int, may_vertexes: list) -> int:
        probalities_transition = []
        sum_wish = 0
        for may_new_vertex in may_vertexes:
            sum_wish += self._global_pheromon[current_vertex][may_new_vertex]["weight"] * \
                self.importance_pheromon + 1 / self._graph[current_vertex][may_new_vertex]["weight"] * \
                    self.importance_long
                    
        for may_new_vertex in may_vertexes:
            wish_transition = self._global_pheromon[current_vertex][may_new_vertex]["weight"] * \
                self.importance_pheromon + 1 / self._graph[current_vertex][may_new_vertex]["weight"] * \
                    self.importance_long
                    
            probalities_transition.append(wish_transition / sum_wish)
            
        return random.choices(may_vertexes, weights=probalities_transition, k=1)[0]
    
    def search_way_for_ant(self, ant: Ant) -> Ant:
        while len(ant.way) < len(self._graph.nodes):
            may_vertexes = list()
            for neibhor in self._graph.neighbors(ant.current_vertex):
                if not ant.is_visited(neibhor):
                    may_vertexes.append(neibhor)
            
            if len(may_vertexes) == 0:
                return Ant(0)
            else:
                ant.transition_new_vertex(self.new_vertex(ant.current_vertex, may_vertexes))
                
        if self._graph.has_edge(ant.way[-1], ant.way[0]):
            return ant
        else:
            return Ant(0)
    
    def way_long(self, way)->int:
        long = 0
        
        for i in range(1, len(way) + 1):
                
            long += self._graph[way[i - 1]][way[i % len(way)]]["weight"]
        
        return long
    
    