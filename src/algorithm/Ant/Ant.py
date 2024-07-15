class Ant:
    def __init__(self, start_vertex: int) -> None:
        self._current_vertex = start_vertex
        self._way = list()
        self._visited = set()
        self._way.append(start_vertex)
        self._visited.add(start_vertex)
        
    @property
    def current_vertex(self):
        return self._current_vertex
    
    @property
    def way(self):
        return self._way
    
    def is_visited(self, vertex):
        return vertex in self._visited
    
    def transition_new_vertex(self, vertex):
        self._way.append(vertex)
        self._visited.add(vertex)
        self._current_vertex = vertex