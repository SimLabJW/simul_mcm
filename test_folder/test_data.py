import socket

def connect_to_server():
    # 서버 주소와 포트
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 서버에 연결
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("서버에 연결되었습니다.")
        return client_socket

    except Exception as e:
        print("서버 연결 중 오류 발생:", e)
        return None

def send_data_twice(data):
    
    if client_socket:
        try:
            # 첫 번째 데이터 전송
            client_socket.send(data.encode())
            print("첫 번째 데이터 전송 완료")


        except Exception as e:
            print("데이터 전송 중 오류 발생:", e)

        # finally:
        #     # 소켓 닫기
        #     client_socket.close()

client_socket = connect_to_server()
# 데이터 전송 테스트
for i in range(5):
    send_data_twice("테스트 데이터")
