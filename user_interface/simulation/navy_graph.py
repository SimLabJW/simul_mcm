# from user_interface.node_graph import NodeGraph
from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import tkinter as tk


sim_flag = False

class GUI_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
    

        self.insert_input_port("start")
        self.insert_output_port("st_b")
        

        """
        nodes = {
            "노드 이름" : {x : 100, y : 140}
        }
        links = [["노드 이름", "노드 이름"], ["노드 이름", "노드 이름"]]
        """

        # 기본 창 생성
        self.root = tk.Tk()
        self.root.title("진우의 신나는 시뮬레이터 GUI")

        # 드롭다운 메뉴의 옵션들
        self.algorithm_options = ["알고리즘 1", "알고리즘 2", "알고리즘 3", "알고리즘 4"]
        self.military_doctrine_options = ["전투교리 1", "전투교리 2", "전투교리 3", "전투교리 4"]
        self.weapon_system_options = ["무기체계1", "무기체계2", "무기체계3", "무기체계4"]

        self.root_label = tk.Label(self.root, text="시뮬레이션 상태: 정지")
        self.root_label.pack(pady=10)

        # 선택된 값 표시를 위한 라벨 - 알고리즘
        self.algorithm_label = tk.Label(self.root, text="선택된 값: ")
        self.algorithm_label.pack(pady=10)

        # 드롭다운 메뉴 생성 - 알고리즘
        self.algorithm_selected_option = tk.StringVar(self.root)
        self.algorithm_selected_option.set(self.algorithm_options[0])  # 기본값 설정
        self.algorithm_dropdown_menu = tk.OptionMenu(self.root, self.algorithm_selected_option, *self.algorithm_options, command=self.algorithm_on_select)
        self.algorithm_dropdown_menu.pack(pady=10)

        # 선택된 값 표시를 위한 라벨 - 전투교리
        self.military_doctrine_label = tk.Label(self.root, text="선택된 값: ")
        self.military_doctrine_label.pack(pady=10)

        # 드롭다운 메뉴 생성 - 전투교리
        self.military_doctrine_selected_option = tk.StringVar(self.root)
        self.military_doctrine_selected_option.set(self.military_doctrine_options[0])  # 기본값 설정
        self.military_doctrine_dropdown_menu = tk.OptionMenu(self.root, self.military_doctrine_selected_option, *self.military_doctrine_options, command=self.military_doctrine_on_select)
        self.military_doctrine_dropdown_menu.pack(pady=10)

        # 선택된 값 표시를 위한 라벨 - 무기체계
        self.weapon_system_label = tk.Label(self.root, text="선택된 값: ")
        self.weapon_system_label.pack(pady=10)

        # 드롭다운 메뉴 생성 - 무기체계
        self.weapon_system_selected_option = tk.StringVar(self.root)
        self.weapon_system_selected_option.set(self.weapon_system_options[0])  # 기본값 설정
        self.weapon_system_dropdown_menu = tk.OptionMenu(self.root, self.weapon_system_selected_option, *self.weapon_system_options, command=self.weapon_system_on_select)
        self.weapon_system_dropdown_menu.pack(pady=10)

        # Start 버튼
        self.start_button = tk.Button(self.root, text='Start', command=self.sim_start_event)
        self.start_button.pack(pady=10)

        # Canvas 추가
        self.canvas = tk.Canvas(self.root, width=500, height=300, bg="white")
        self.canvas.pack(pady=10)

        node_graph = NodeGraph(self.canvas)
        # # Draw Graph 버튼
        # draw_graph_button = tk.Button(root, text='Draw Graph', command=draw_graph)
        # draw_graph_button.pack(pady=10)

        self.root.mainloop()

    def ext_trans(self, port, msg):
        global sim_flag
        if port == "start":
            # 창 실행
            # self.root.mainloop()
            self._cur_state = "Generate"
            print("in navy_graph")

        
            # if sim_flag == False:
            #     msg = SysMessage(self.get_name(), "st_b")
            #     return msg

      
    def output(self): 
       if self._cur_state == "Generate":
           if sim_flag == False:
                msg = SysMessage(self.get_name(), "st_b")
                return msg
            
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Generate":
            self._cur_state = "Generate"

    def sim_start_event(self):
        global sim_flag
        if sim_flag == False:
            self.root_label.config(text="시뮬레이션 상태: 동작 중")
            self.start_button.config(text="Running...")
            # 노드 그래프 그림
            self.draw_graph()
            sim_flag = True
            self.output()
        else:
            self.root_label.config(text="시뮬레이션 상태: 정지")
            self.start_button.config(text="Start")
            # 노드 그래프 삭제
            # canvas.delete("all")
            sim_flag = False

    def algorithm_on_select(self,value):
        self.algorithm_label.config(text="선택된 값: " + value)

    def military_doctrine_on_select(self,value):
        self.military_doctrine_label.config(text="선택된 값: " + value)

    def weapon_system_on_select(self,value):
        self.weapon_system_label.config(text="선택된 값: " + value)

    def draw_graph(self):
        
        global node_graph
        self.canvas.delete("all")
        
        # node_graph.add_node("dive_1")