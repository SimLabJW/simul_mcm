import tkinter as tk

class NodeGraph:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_list = []
        
        self.node_radius = 20
        self.node_distance = 80
        
        self.start_x, self.start_y = 50, 50
        self.count_x, self.count_y = 0, 0
        self.flag_reverse = False
        
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

    def add_node(self, node):
        node_info = {}
        node_detail = self.node_coordinate()
        node_info[node] = node_detail
        self.node_list.append(node_info)
        self.draw_graph(node_info)
        
        
    def node_coordinate(self) -> dict :
        node_coord = {}
        node_coord["x"] = self.start_x + (self.count_x * self.node_distance)
        node_coord["y"] = self.start_y + (self.count_y * self.node_distance)
      
        self.check_canvas()        
        
        return node_coord
            
    def draw_graph(self, node_info):
        node_name = list(node_info.keys())[0]
        node_x = node_info[node_name]["x"]
        node_y = node_info[node_name]["y"]
        
        self.canvas.create_oval(node_x - self.node_radius, node_y - self.node_radius,\
            node_x + self.node_radius, node_y + self.node_radius, fill="lightblue")
        self.canvas.create_text(node_x, node_y, text=node_name)   
        
        self.add_edge()
        
    def add_edge(self):
        # 간선 그리기
        
        if len(self.node_list) > 1:
            start_node_info = self.node_list[len(self.node_list) - 2]
            end_node_info = self.node_list[len(self.node_list) - 1]
            
            start_node_name = list(start_node_info.keys())[0]
            end_node_name = list(end_node_info.keys())[0]
            
            start_node_x = start_node_info[start_node_name]["x"]
            start_node_y = start_node_info[start_node_name]["y"]
            
            end_node_x = end_node_info[end_node_name]["x"]
            end_node_y = end_node_info[end_node_name]["y"]
            
            
            self.canvas.create_line(start_node_x, start_node_y, end_node_x, end_node_y, arrow=tk.LAST, fill="black")    
            
    
    def set_next_node(self):
        if self.flag_reverse:
            self.count_y -= 1
        
        else:
            self.count_y += 1
            
        
    def check_canvas(self):
        if self.count_y == 2 and not self.flag_reverse:
            self.flag_reverse = True
            self.count_x += 1
            
        elif self.count_y == 0 and self.node_list and self.flag_reverse:
            self.flag_reverse = False
            self.count_x += 1
            
        else:
            self.set_next_node()
        
    # def add_graph(self, start_node, end_node = None):
    #     self.calculate_node_coordinate(start_node, end_node)
    #     # self.node[key] = label    
    #     # 노드 그리기
    #     # node = self.root.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
    #     self.canvas.create_oval(x - self.node_radius, y - self.node_radius,\
    #         x + self.node_radius, y + self.node_radius, fill="lightblue")
    #     self.canvas.create_text(x, y, text=node_name)    

    # def add_node(self, node_name):
    #     self.calculate_node_coordinate(node_name)
    #     # self.node[key] = label    
    #     # 노드 그리기
    #     # node = self.root.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
    #     self.canvas.create_oval(x - self.node_radius, y - self.node_radius,\
    #         x + self.node_radius, y + self.node_radius, fill="lightblue")
    #     self.canvas.create_text(x, y, text=node_name)
        
    # def del_node(self, x, y, key, label):
    #     del self.node[key]
        
    # def calculate_node_coordinate(self, start_node, end_node = None):    
    #     start_node_feature = start_node.split('_')[0]
    #     end_node_feature = end_node.split('_')[0]
    #     temp_dict = {}
        
    #     # 첫 시작일경우
    #     if len(self.feature_count) == 0 and end_node == None:            
    #         temp_dict[start_node.split('_')[0]] = 1
    #         self.feature_count.append(temp_dict)
    #     else:
    #     # 이미 존재하는 노드일경우
    #         # 시작 노드와 끝 노드의 feature가 같을 경우 : 상하 연결
    #         if start_node_feature == end_node_feature:
                
    #             # 새로운 feature일 경우
    #             if end_node_feature not in self.feature_count:
                                    
    #                 temp_dict[end_node_feature] = 0
                
                
    #         # 시작 노드와 끝 노드의 feature가 다른 경우 : 좌우 연결
            # else:
                # 노드 리스트에 노드가 있는 경우
                # 없는 경우
            
            
    # def set_node_coordinate(self, feature):
    #     for index, dict in enumerate(self.feature_count):
    #         if feature in dict:
    #             self.node[feature]["x"] = self.start_x + (index * self.node_distance)
    #             self.node[feature]["y"] = self.start_y + (dict[feature] * self.node_distance)
                
    #             self.feature_count[index][feature] += 1
            
