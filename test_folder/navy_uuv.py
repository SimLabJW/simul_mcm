from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np 
import time

class UUV_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_state("first_state",1)
        self.insert_state("second_state",1)
        self.insert_state("third_state",1)
    
        self.insert_input_port("start")
        self.insert_input_port("next")
        self.insert_input_port("stop")

        self.insert_output_port("uuv_state")
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            self._cur_state = "first_state"
            
        if port == "next":
            self.label = msg.retrieve()[0][0]
            print(f"self.label {self.label}")
            if self.label:
                if self.label == "1":
                    self._cur_state = "second_state"
                else:
                    self._cur_state = "third_state"
        
        if port == "stop":
            self._cur_state = "Wait"

    def output(self): 

        if self._cur_state == "first_state":
            print("aaaaaaaaaaaa")
            self.first_c()
            msg = SysMessage(self.get_name(), "uuv_state")
            msg.insert(["uuv","1"])
            return msg
        
        if self._cur_state == "second_state":
            self.second_c()
            msg = SysMessage(self.get_name(), "uuv_state")
            msg.insert(["uuv","2"])
            return msg
        
        if self._cur_state == "third_state":
            self.third_c()
            msg = SysMessage(self.get_name(), "uuv_state")
            msg.insert(["uuv","3"])
            return msg
            
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "first_state":
            self._cur_state = "Wait"
        elif self._cur_state == "second_state":
            self._cur_state = "Wait"
        elif self._cur_state == "third_state":
            self._cur_state = "Wait"

    def first_c(self):
        time.sleep(2)
        print(f"uuv model c 1")
        time.sleep(2)

    def second_c(self):
        time.sleep(2)
        print(f"uuv model c 2")
        time.sleep(2)


    def third_c(self):
        time.sleep(2)
        print(f"uuv model c 3")
        time.sleep(2)
   