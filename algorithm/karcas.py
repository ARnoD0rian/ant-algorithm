from abc import ABC, abstractmethod

class Algorithm(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def init_graph(self, vertex_num: int, edges: list[dict])->None:
        pass
    @abstractmethod
    def search_hamilton_cycle(self)->list[dict]:
        pass