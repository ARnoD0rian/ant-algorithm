import tkinter as tk
from tkinter import ttk
import json
import sys
import os
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askstring
import networkx as nx
from algorithm.parallelModification import Algorithm

class GUI:
    def __init__(self, root: tk.Tk, title: str) -> None:
        
        #параметры
        self._vertex_num = 0
        self._edge_num = 0
        self._edge = list() # список ребер
        self._vertex = list() # список вершин
        self._algorithm = Algorithm() # класс алгоритма
        #интерфейс
        self.root = root
        self.root.title(title)
        self.root.geometry('1200x456')
        self.root['background'] = "#EDE7E6"
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.grid(row=0, column=0, rowspan=12, columnspan=10)
        #таблица
        self.tree = ttk.Treeview(self.root, columns=('From', 'To', 'Weight'), show='headings')
        self.tree.heading('From', text='From')
        self.tree.heading('To', text='To')
        self.tree.heading('Weight', text='Weight')
        self.tree.grid(column=10, row=0, columnspan=3, rowspan=3)
         #поля ввода данных для ребер графа
        self.from_label = ttk.Label(self.root, text="From:")
        self.from_label.grid(row=3, column=10)
        self.from_entry = ttk.Entry(self.root, justify='center')
        self.from_entry.grid(row=4, column=10)
        self.to_label = ttk.Label(self.root, text="To:")
        self.to_label.grid(row=5, column=10)
        self.to_entry = ttk.Entry(self.root, justify='center')
        self.to_entry.grid(row=6, column=10)
        
        self.weight_label = ttk.Label(self.root, text="Weight:")
        self.weight_label.grid(row=7, column=10)
        self.weight_entry = ttk.Entry(self.root, justify='center')
        self.weight_entry.grid(row=8, column=10)
        
        #поля ввода данных для температуры
        self.importance_pheromon_label = ttk.Label(self.root, text="importance pheromon")
        self.importance_pheromon_label.grid(row=3, column=11)
        self.importance_pheromon_entry = ttk.Entry(self.root, justify='center')
        self.importance_pheromon_entry.insert(0, "1")
        self.importance_pheromon_entry.grid(row=4, column=11)
        
        self.importance_long_label = ttk.Label(self.root, text="importance long")
        self.importance_long_label.grid(row=5, column=11)
        self.importance_long_entry = ttk.Entry(self.root, justify='center')
        self.importance_long_entry.insert(0, "3")
        self.importance_long_entry.grid(row=6, column=11)
        
        self.evaporation_rate_pheromon_label = ttk.Label(self.root, text="evaporation rate")
        self.evaporation_rate_pheromon_label.grid(row=7, column=11)
        self.evaporation_rate_pheromon_entry = ttk.Entry(self.root, justify='center')
        self.evaporation_rate_pheromon_entry.insert(0, "0.1")
        self.evaporation_rate_pheromon_entry.grid(row=8, column=11)
        
        self.iteration_label = ttk.Label(self.root, text="итерации")
        self.iteration_label.grid(row=3, column=12)
        self.iteration_entry = ttk.Entry(self.root, justify='center')
        self.iteration_entry.insert(0, "50")
        self.iteration_entry.grid(row=4, column=12)
        
        self.num_ant_label = ttk.Label(self.root, text="Количество муравьев")
        self.num_ant_label.grid(row=5, column=12)
        self.num_ant_entry = ttk.Entry(self.root, justify='center')
        self.num_ant_entry.insert(0, "50")
        self.num_ant_entry.grid(row=6, column=12)
        
        self.const_for_pheromon_label = ttk.Label(self.root, text="постоянная феромонов")
        self.const_for_pheromon_label.grid(row=7, column=12)
        self.const_for_pheromon_entry = ttk.Entry(self.root, justify='center')
        self.const_for_pheromon_entry.insert(0, "1")
        self.const_for_pheromon_entry.grid(row=8, column=12)
        
        
        
        #кнопка добавление ребра
        self.add_button = ttk.Button(self.root, text="Add Edge", command=self.add_edge)
        self.add_button.grid(row=9, column=10)
        #кнопка добавления данных для работы алгоритма
        self.add_button = ttk.Button(self.root, text="Add paremetres", command=self.add_paremetres)
        self.add_button.grid(row=9, column=11, columnspan=2)
        # canvas
        self.canvas.bind("<Button-1>", self.add_vertex)
        #меню
        self.main_menu = tk.Menu()
        self.main_menu.add_cascade(label="запустить", command=self.start_algorithm)
        self.main_menu.add_cascade(label="прочитать json", command=self.read_json)
        self.main_menu.add_cascade(label="выход", command=sys.exit)
        self.root.config(menu=self.main_menu)
        # запуск интерфейса
        self.root.mainloop()

    def add_vertex(self, event) -> None: #считывание нажатия и добавления в точку новой вершины
        x, y = event.x, event.y #получение координат
        self._vertex_num += 1
        self._vertex.append((x, y))
        self.draw_vertex((x, y))
        
        
    def draw_vertex(self, coordinate: tuple) -> None: # рисование вершины в canvas
        x, y = coordinate
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='green')
        self.canvas.create_text(x, y, text=str(self._vertex_num), fill='white') 
    
    def add_edge(self) -> None: #добавление ребра
        from_vertex = int(self.from_entry.get()) #считывание данных
        to_vertex = int(self.to_entry.get())
        weight = int(self.weight_entry.get())
        self._edge.append({"from": from_vertex, "to": to_vertex, "weight": weight}) #добавление ребра в список
        
        if from_vertex > 0 and from_vertex <= self._vertex_num and to_vertex > 0 and to_vertex <= self._vertex_num:
            self.draw_edge(from_vertex, to_vertex, weight) # проверка корректности введенных данных и отображение ребра
        else:
            return
        
    def draw_edge(self, from_vertex: int, to_vertex: int, weight: int) -> None: #отображение ребра
        self.tree.insert('', 'end', values=(from_vertex, to_vertex, weight)) # добавление ребра в таблицу
        
        from_x, from_y = self.get_vertex_coordinates(from_vertex) # получение координат исходящей вершины
        to_x, to_y = self.get_vertex_coordinates(to_vertex) # получение координат входящей вершины
        
        to_x, to_y = self.get_coordinate_edge(from_x, from_y, to_x, to_y) # корректировка координат для более красивой визуализации
        #отображение ребра в canvas
        line = self.canvas.create_line(from_x, from_y, to_x, to_y, width=2, fill= 'red' if from_vertex < to_vertex else 'blue', arrow='last', tag = 'line')
        self.canvas.create_text((to_x + from_x) / 2 + 5, (to_y + from_y) / 2 + 5, text=str(weight), fill='red' if from_vertex < to_vertex else 'blue')
        self.canvas.tag_lower(line) 
            
        
    
    def get_vertex_coordinates(self, vertex: int) -> tuple: #получение координат точки
                    return self._vertex[vertex - 1]
           
    def get_coordinate_edge(self, x_1, y_1, x_2, y_2, r = 10) -> tuple: #преобразование координат для пболее красивой визуализации
        #рассчет коэффициентов и получение новых координат, формулы для которых были получены аналитически
        k = (y_2-y_1) / (x_2 - x_1)
        d = (x_2 + k**2 * x_1 + k *(y_2 - y_1))**2 - (k** 2 + 1) * (x_2**2 + (k*x_1)**2 + 2*k*x_1*(y_2-y_1) + (y_2-y_1)**2 - r**2)
        
        x = (x_2 + k**2 * x_1 + k *(y_2 - y_1) - d**0.5) / (k**2 + 1)
        y = (x - x_1) * k + y_1
        o_1 = (x, y)
        
        x = (x_2 + k**2 * x_1 + k *(y_2 - y_1) + d**0.5) / (k**2 + 1)
        y = (x - x_1) * k + y_1
        o_2 = (x, y)
        
        return o_1 if (x_1 - o_1[0])**2 + (y_1 - o_1[1]) ** 2 < (x_1 - o_2[0])**2 + (y_1 - o_2[1]) ** 2 else o_2
    
    def add_paremetres(self) -> None:
        #считывание параметров
        importance_pheromon = float(self.importance_pheromon_entry.get())
        importance_long = float(self.importance_long_entry.get())
        evaporation_rate = float(self.evaporation_rate_pheromon_entry.get())
        iteration = float(self.iteration_entry.get())
        cont_for_pheromon = float(self.const_for_pheromon_entry.get())
        num_ant = float(self.num_ant_entry.get())
        # добавление начальных данных в алгоритм иммитации отжига
        self._algorithm.iteration = iteration
        self._algorithm.const_for_pheromon = cont_for_pheromon
        self._algorithm.num_ant = num_ant
        self._algorithm.importance_pheromon = importance_pheromon
        self._algorithm.importance_long = importance_long
        self._algorithm.evaporation_rate = evaporation_rate
        showinfo(title="успех", message="данные сохранены")
    
    def read_json(self) -> None: # чтение json файла и визуализация графа из него
        name = askstring("Файл", "Введите путь к файлу json") #получение директории от пользователя
        
        if not os.path.isfile(name):#проверка существования директории
            showerror(title="ошибка", message="файл не найден")
        
        #очистка предыдущих данных
        self.canvas.delete("all")
        self._edge.clear()
        self._vertex.clear()
        self._vertex_num = 0
        self._edge_num = 0
        self.tree.delete(*self.tree.get_children())
        
        # получение данных из файла
        with open(f"{name}", 'r') as file:
            data = json.load(file) 
            
            for i in range(len(data["vertexes"])):
                vertex = (data["vertexes"][i]["x"], data["vertexes"][i]["y"])
                self._vertex_num += 1
                self._vertex.append((vertex[0], vertex[1]))
                self.draw_vertex(vertex) #визуализация вершин
            
            for i in range(len(data["edges"])):
                edge = data["edges"][i]
                self._edge.append(edge)
                self.draw_edge(edge["from"], edge["to"], edge["weight"])#визуализация ребер
                
    
    def start_algorithm(self): #запуск алгоритма
        self._algorithm.init_graph(self._vertex_num, self._edge) #инициализация графа
        self._edge = self._algorithm.search_hamilton_cycle() # запуск алгоритма
        #очистка предыдущих данных
        self._edge_num = 0
        self._vertex_num = 0
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i in range(len(self._vertex)):
            self._vertex_num += 1
            self.draw_vertex(self._vertex[i])# визуализация вершин
            
        #визуализация пути
        for i in range(len(self._edge)):
            self.draw_edge(self._edge[i]["from"], self._edge[i]["to"], self._edge[i]["weight"])
            
        way = f"{self._edge[0]['from']}"
        sum = 0
        for edge in self._edge:
            sum += edge["weight"]
            way = way + f"-{edge['to']}"
            
        showinfo(title="результат", message=f"Сумма = {sum}, Путь: {way}")
        
    @property
    def edge(self): # получение ребер
        return self._edge
    
    @property
    def vartex(self): # получение вершин
        return self._vertex
    

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root, "алгоритм k ближайших соседей")
    
