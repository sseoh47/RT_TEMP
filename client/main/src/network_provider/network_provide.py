from network_provider.custom_protocol import CustomProtocol
from network_provider.stream_socket import StreamTCPSocket
from controller import EmbeddedLogic
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time


class NetworkProvider:
    def start(self):
        embedded_logic = EmbeddedLogic()
        
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 5000))

        streamTCPSocket = StreamTCPSocket(client_socket)
        protocol = CustomProtocol()
        
        # send, recv thread start
        send_thread=Thread(target=self.send_thread, args=(streamTCPSocket, embedded_logic, protocol))
        send_thread.start()
        recv_thread = Thread(target=self.recv_thread, args=(streamTCPSocket, embedded_logic, protocol))
        recv_thread.start()
        

    def recv_thread(self, streamTCPSocket:StreamTCPSocket, embedded_logic:EmbeddedLogic,custom_protocol:CustomProtocol):
        while True:
            time.sleep(0.5)
            data = streamTCPSocket.recv()  # input data
            dict_data=custom_protocol.string_to_dict(data.decode())
            embedded_logic.recv_enque(dict_data)

    def send_thread(self, streamTCPSocket:StreamTCPSocket, embedded_logic:EmbeddedLogic, custom_protocol:CustomProtocol):
        while True:
            time.sleep(0.5)
            result=embedded_logic.is_send_queue_empty()  #  YES(1) / NO(0)
            if not result:  # 비어있다면
                dict_data=embedded_logic.send_deque()  # 데이터 추출
                string_data:str=custom_protocol.dict_to_string(dict_data)
                streamTCPSocket.send(string_data)  # 변환한 string data를 server로 전송
