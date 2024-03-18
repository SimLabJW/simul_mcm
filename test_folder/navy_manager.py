from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from navy_area import Area_Model
from navy_uuv import UUV_Model
from navy_dive import DIVE_Model
from navy_node_manager import NODE_Model
# from navy_graph import GUI_Model
import tkinter as tk
from node_graph import NodeGraph


sim_flag = False

class Navy_manager():
    def __init__(self) -> None:
        self.ss = SystemSimulator()

        self.ss.register_engine("OBSERVER", "VIRTUAL_TIME", 0.1)
        self.navy_simulation_model = self.ss.get_engine("OBSERVER")


        self.navy_simulation_model.insert_input_port("start")
        self.navy_simulation_model.insert_input_port("next")
        self.navy_simulation_model.insert_input_port("stop")

        Area_m = Area_Model(0, Infinite, "Area_m", "OBSERVER")
        UUV_m = UUV_Model(0, Infinite, "UUV_m", "OBSERVER")
        Dive_m = DIVE_Model(0, Infinite, "Dive_m", "OBSERVER")
        Node_m = NODE_Model(0, Infinite, "Node_m", "OBSERVER")
        # GUI_m = GUI_Model(0, Infinite, "GUI_m", "OBSERVER")

        self.navy_simulation_model.register_entity(Area_m)
        self.navy_simulation_model.register_entity(UUV_m)
        self.navy_simulation_model.register_entity(Dive_m)
        self.navy_simulation_model.register_entity(Node_m)
        # self.navy_simulation_model.register_entity(GUI_m)
  
        # simulation 진행 커리큘럼
        self.navy_simulation_model.coupling_relation(None, "start", Area_m, "start")
        self.navy_simulation_model.coupling_relation(Area_m, "area_state", Node_m, "start")
        self.navy_simulation_model.coupling_relation(Node_m, "next_a", Area_m, "next")

        self.navy_simulation_model.coupling_relation(Node_m, "Done_a", UUV_m, "start")
        self.navy_simulation_model.coupling_relation(UUV_m, "uuv_state", Node_m, "start")
        self.navy_simulation_model.coupling_relation(Node_m, "next_u", UUV_m, "next")

        self.navy_simulation_model.coupling_relation(Node_m, "Done_u", Dive_m, "start")
        self.navy_simulation_model.coupling_relation(Dive_m, "dive_state", Node_m, "start")
        self.navy_simulation_model.coupling_relation(Node_m, "next_d", Dive_m, "next")

        # self.navy_simulation_model.coupling_relation(Node_m, "Done_d", Dive_m, "stop")
        self.navy_simulation_model.coupling_relation(Node_m, "Done_d", None, "stop")



    def start(self) -> None:
        # pass
        self.navy_simulation_model.insert_external_event("start","start")
        self.navy_simulation_model.simulate()
        