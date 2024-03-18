import tkinter as tk
from node_graph import NodeGraph
import socket
import threading
import json
import os

sim_flag = False
server_socket = None
"""
nodes = {
    "노드 이름" : {x : 100, y : 140}
}
links = [["노드 이름", "노드 이름"], ["노드 이름", "노드 이름"]]
"""


def start_server():
    global server_socket
    # 서버 주소와 포트
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 주소와 포트에 바인드
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # 클라이언트의 연결을 기다림
    server_socket.listen(1)
    print(f"[*] 서버가 {SERVER_HOST}:{SERVER_PORT} 에서 클라이언트를 기다리고 있습니다.")

    # 클라이언트 연결 받기
    client_socket, client_address = server_socket.accept()
    print(f"[*] {client_address} 로부터 연결이 수락되었습니다.")

    # 클라이언트로부터 메시지 수신 및 출력
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(f"[받은 메시지] {message}")

        # JSON 형식의 데이터를 파이썬 리스트로 변환
        data_list = json.loads(message)
        node_graph.add_node(data_list[0] + data_list[1])


    # 연결 종료
    client_socket.close()


def sim_start_event():
    global sim_flag
    if sim_flag == False:
        root_label.config(text="시뮬레이션 상태: 동작 중")
        start_button.config(text="Running...")
        # 노드 그래프 그림
        draw_graph()
        # start_simulator.start()
        sim_flag = True

        # 통신을 시작하는 쓰레드 시작
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        # 통신을 시작하는 쓰레드 시작
        simulator_thread = threading.Thread(target=start_simulator)
        simulator_thread.start()

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
    
def on_closing():
    # 창이 닫힐 때 서버 소켓 닫기
    if server_socket:
        server_socket.close()
    root.destroy()
    
def start_simulator():
    os.system("python navy_simulator.py")
# 기본 창 생성
root = tk.Tk()
root.title("진우의 신나는 시뮬레이터 GUI")

# 종료 이벤트 핸들러 등록
root.protocol("WM_DELETE_WINDOW", on_closing)

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


