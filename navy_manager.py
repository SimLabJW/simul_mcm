from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
# from navy_area import Area_Model
# from navy_uuv import UUV_Model
# from navy_dive import DIVE_Model
from navy_node_manager import NODE_Model

class Navy_manager():
    def __init__(self) -> None:
        self.ss = SystemSimulator()

        self.ss.register_engine("OBSERVER", "VIRTUAL_TIME", 0.1)
        self.navy_simulation_model = self.ss.get_engine("OBSERVER")


        self.navy_simulation_model.insert_input_port("start")

        # Area_m = Area_Model(0, Infinite, "Area_m", "OBSERVER")
        # UUV_m = UUV_Model(0, Infinite, "UUV_m", "OBSERVER")
        # Dive_m = DIVE_Model(0, Infinite, "Dive_m", "OBSERVER")
        Node_m = NODE_Model(0, Infinite, "Node_m", "OBSERVER")

        # self.navy_simulation_model.register_entity(Area_m)
        # self.navy_simulation_model.register_entity(UUV_m)
        # self.navy_simulation_model.register_entity(Dive_m)
        self.navy_simulation_model.register_entity(Node_m)
  
        # simulation 진행 커리큘럼
        # self.navy_simulation_model.coupling_relation(None, "start", Area_m, "start")
        # self.navy_simulation_model.coupling_relation(Area_m, "start", UUV_m, "start")
        # self.navy_simulation_model.coupling_relation(UUV_m, "start", Dive_m, "start")

        # # node 진행 사항 입력 확인 
        # self.navy_simulation_model.coupling_relation(Area_m, "start", Node_m, "start")
        # self.navy_simulation_model.coupling_relation(UUV_m, "start", Node_m, "start")
        # self.navy_simulation_model.coupling_relation(Dive_m, "start", Node_m, "start")
        # 진행 종료
        # self.navy_simulation_model.coupling_relation(Dive_m, "start", Node_m, "start")
        self.navy_simulation_model.coupling_relation(None, "start", Node_m, "start")


        self.start()


    def start(self) -> None:
        # pass
        self.navy_simulation_model.insert_external_event("start","start")
        self.navy_simulation_model.simulate()
        