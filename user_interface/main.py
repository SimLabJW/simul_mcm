import tkinter as tk
from node_graph import NodeGraph

sim_flag = False

"""
nodes = {
    "노드 이름" : {x : 100, y : 140}
}
links = [["노드 이름", "노드 이름"], ["노드 이름", "노드 이름"]]
"""


def sim_start_event():
    global sim_flag
    if sim_flag == False:
        root_label.config(text="시뮬레이션 상태: 동작 중")
        start_button.config(text="Running...")
        # 노드 그래프 그림
        draw_graph()
        sim_flag = True
    else:
        root_label.config(text="시뮬레이션 상태: 정지")
        start_button.config(text="Start")
        # 노드 그래프 삭제
        # canvas.delete("all")
        sim_flag = False

def algorithm_on_select(value):
    algorithm_label.config(text="선택된 값: " + value)

def military_doctrine_on_select(value):
    military_doctrine_label.config(text="선택된 값: " + value)

def weapon_system_on_select(value):
    weapon_system_label.config(text="선택된 값: " + value)

def draw_graph():
    
    global node_graph
    canvas.delete("all")
    
    node_graph.add_node("dive_1")
    node_graph.add_node("dive_2")
    node_graph.add_node("dive_3")
    node_graph.add_node("dive_4")
    node_graph.add_node("dive_5")
    node_graph.add_node("dive_111")
    node_graph.add_node("dive_123")
    node_graph.add_node("dive_14")
    node_graph.add_node("dive_11")
    
    
    
    

# 기본 창 생성
root = tk.Tk()
root.title("진우의 신나는 시뮬레이터 GUI")

# 드롭다운 메뉴의 옵션들
algorithm_options = ["알고리즘 1", "알고리즘 2", "알고리즘 3", "알고리즘 4"]
military_doctrine_options = ["전투교리 1", "전투교리 2", "전투교리 3", "전투교리 4"]
weapon_system_options = ["무기체계1", "무기체계2", "무기체계3", "무기체계4"]

root_label = tk.Label(root, text="시뮬레이션 상태: 정지")
root_label.pack(pady=10)

# 선택된 값 표시를 위한 라벨 - 알고리즘
algorithm_label = tk.Label(root, text="선택된 값: ")
algorithm_label.pack(pady=10)

# 드롭다운 메뉴 생성 - 알고리즘
algorithm_selected_option = tk.StringVar(root)
algorithm_selected_option.set(algorithm_options[0])  # 기본값 설정
algorithm_dropdown_menu = tk.OptionMenu(root, algorithm_selected_option, *algorithm_options, command=algorithm_on_select)
algorithm_dropdown_menu.pack(pady=10)

# 선택된 값 표시를 위한 라벨 - 전투교리
military_doctrine_label = tk.Label(root, text="선택된 값: ")
military_doctrine_label.pack(pady=10)

# 드롭다운 메뉴 생성 - 전투교리
military_doctrine_selected_option = tk.StringVar(root)
military_doctrine_selected_option.set(military_doctrine_options[0])  # 기본값 설정
military_doctrine_dropdown_menu = tk.OptionMenu(root, military_doctrine_selected_option, *military_doctrine_options, command=military_doctrine_on_select)
military_doctrine_dropdown_menu.pack(pady=10)

# 선택된 값 표시를 위한 라벨 - 무기체계
weapon_system_label = tk.Label(root, text="선택된 값: ")
weapon_system_label.pack(pady=10)

# 드롭다운 메뉴 생성 - 무기체계
weapon_system_selected_option = tk.StringVar(root)
weapon_system_selected_option.set(weapon_system_options[0])  # 기본값 설정
weapon_system_dropdown_menu = tk.OptionMenu(root, weapon_system_selected_option, *weapon_system_options, command=weapon_system_on_select)
weapon_system_dropdown_menu.pack(pady=10)

# Start 버튼
start_button = tk.Button(root, text='Start', command=sim_start_event)
start_button.pack(pady=10)

# Canvas 추가
canvas = tk.Canvas(root, width=500, height=300, bg="white")
canvas.pack(pady=10)

node_graph = NodeGraph(canvas)
# # Draw Graph 버튼
# draw_graph_button = tk.Button(root, text='Draw Graph', command=draw_graph)
# draw_graph_button.pack(pady=10)

# 창 실행
root.mainloop()
