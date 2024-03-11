import tkinter as tk

class NodeGraph:
    def __init__(self, root):
        self.root = root
        # self.root.title("노드 그래프 예제")

        # Canvas 생성
        # self.canvas = tk.Canvas(self.master, width=400, height=300, bg="white")
        # self.canvas.pack()

        # 노드와 간선 추가
        self.add_node(50, 50, "노드 1")
        self.add_node(200, 50, "노드 2")
        self.add_node(125, 150, "노드 3")

        self.add_edge(50, 50, 200, 50)
        self.add_edge(50, 50, 125, 150)
        self.add_edge(200, 50, 125, 150)

    def add_node(self, x, y, label):
        # 노드 그리기
        node = self.root.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.root.create_text(x, y, text=label)

    def add_edge(self, x1, y1, x2, y2):
        # 간선 그리기
        self.root.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black")