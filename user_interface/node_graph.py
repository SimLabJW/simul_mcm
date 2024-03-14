import tkinter as tk

class NodeGraph:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node = {}
        
        self.node_radius = 20
        self.node_distace = 150
        
        self.start_x, self.start_y = 50, 50
        self.feature_count = {}
        
        
        # self.feature_list = ["area", "uun", "dive"]
        
        # self.root.title("노드 그래프 예제")

        # Canvas 생성
        # self.canvas = tk.Canvas(self.master, width=400, height=300, bg="white")
        # self.canvas.pack()

        # 노드와 간선 추가
        # self.add_node(50, 50, "노드 1")
        # self.add_node(200, 50, "노드 2")
        # self.add_node(125, 150, "노드 3")

        # self.add_edge(50, 50, 200, 50)
        # self.add_edge(50, 50, 125, 150)
        # self.add_edge(200, 50, 125, 150)

    def add_graph(self, start_node, end_node):
        self.calculate_node_coordinate(start_node, end_node)
        # self.node[key] = label    
        # 노드 그리기
        # node = self.root.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,\
            x + self.node_radius, y + self.node_radius, fill="lightblue")
        self.canvas.create_text(x, y, text=node_name)    

    def add_node(self, node_name):
        self.calculate_node_coordinate(node_name)
        # self.node[key] = label    
        # 노드 그리기
        # node = self.root.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,\
            x + self.node_radius, y + self.node_radius, fill="lightblue")
        self.canvas.create_text(x, y, text=node_name)

    def add_edge(self, x1, y1, x2, y2):
        # 간선 그리기
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black")
        
    def del_node(self, x, y, key, label):
        del self.node[key]
        
    def calculate_node_coordinate(self, start_node, end_node):    
        start_node_feature = start_node.split('_')[0]
        end_node_feature = end_node.split('_')[0]
        
        if start_node_feature == end_node_feature:
            
            if self.feature_count[start_node_feature] == None:
                self.feature_count[start_node_feature]["x"] = len(self.feature_count)
                self.feature_count[start_node_feature]["y"] = 0
                
            self.node[start_node]["x"] = self.start_x + (self.feature_count[start_node_feature]["x"] * self.node_distace)
            self.node[start_node]["y"] = self.start_y + (self.feature_count[start_node_feature]["y"] * self.node_distace)
            
            self.feature_count[start_node_feature]["y"] += 1
                
        else:
            # 노드 리스트에 노드가 있는 경우
            # 없는 경우
            
            
    
            
