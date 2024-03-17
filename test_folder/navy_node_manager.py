from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np

import socket
import json
from node_graph import *

class NODE_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_input_port("start")

        self.insert_output_port("next")
        self.insert_output_port("Done")
        self.client_socket = self.connect_to_server()

    def ext_trans(self, port, msg):
        
        if port == "start":
            self.insert_data = msg.retrieve()
            self._cur_state = "Generate"
      
    def output(self): 
        if self._cur_state == "Generate":
            print(f"self.insert data {[self.insert_data[0]]}")
            self.send_data([self.insert_data[0][0],self.insert_data[0][1]])
            if self.insert_data[0][0] == "area":
                if self.insert_data[0][1] == "3":
                    msg = SysMessage(self.get_name(), "Done_a")
                    return msg
                
                else:
                    msg = SysMessage(self.get_name(), "next_a")
                    msg.insert([self.insert_data[0][1]])
                    return msg
                
            if self.insert_data[0][0] == "uuv":
                if self.insert_data[0][1] == "3":
                    msg = SysMessage(self.get_name(), "Done_u")
                    return msg
                
                else:
                    msg = SysMessage(self.get_name(), "next_u")
                    msg.insert([self.insert_data[0][1]])
                    return msg
                
            if self.insert_data[0][0] == "dive":
                if self.insert_data[0][1] == "3":
                    msg = SysMessage(self.get_name(), "Done_d")
                    return msg
                
                else:
                    msg = SysMessage(self.get_name(), "next_d")
                    msg.insert([self.insert_data[0][1]])
                    return msg
            # self._cur_state = "Wait"
                
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Generate":
            self._cur_state = "Wait"

    


    def connect_to_server(self):
        # 서버 주소와 포트
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 12345

        # 소켓 생성
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # 서버에 연결
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("서버에 연결되었습니다.")
            return self.client_socket

        except Exception as e:
            print("서버 연결 중 오류 발생:", e)
            return None
        

    def send_data(self,data):
    
        if self.client_socket:
            try:
                # 리스트를 JSON 형식의 문자열로 변환
                json_data = json.dumps(data)
                # 첫 번째 데이터 전송
                self.client_socket.send(json_data.encode())
                print("첫 번째 데이터 전송 완료")


            except Exception as e:
                print("데이터 전송 중 오류 발생:", e)