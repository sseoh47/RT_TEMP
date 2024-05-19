from queue import Queue
from controller.path_find_logic import PathFindLogic
from controller.beacon_logic import BeaconLogic
from threading import Thread

class Logic:
    def __init__(self) -> None:
        self.__send_queue=Queue()
        self.__recv_queue=Queue()
        thread=Thread(target= self.__controller_interface_thread,
                    args=None)
        thread.start()
        thread.join()
       
    def recv_enque(self, dict_data:dict):
        self.__recv_queue.put(dict_data)

    def send_deque(self) -> dict:
        dict_data = self.__send_queue.get()    
        return dict_data
    
    def isEmptySendQueue(self) -> bool:
        result=self.__send_queue.empty()
        return result
    
    def __isEmptyRecvQueue(self) -> bool:
        result = self.__recv_queue.empty()
        return result

    def __recv_deque(self) -> dict:
        dict_data = self.__recv_queue.get()
        return dict_data
    
    def __send_enque(self, dict_data:dict):
        self.__send_queue.put(dict_data)
        return
    
    def __controller_interface_thread(self):
        result = self.__isEmptyRecvQueue()
        if not result:
            dict_data = self.__recv_deque()
            if dict_data['root'] == 'PATH':
                pathFindLogic = PathFindLogic()
                result = pathFindLogic.get_shortest_path(dict_data['bname'], dict_data['body'])
                self.__send_enque(dict_data=result)
            elif dict_data['root'] == 'BUS':
                beaconLogic = BeaconLogic()
                result = beaconLogic.find_beacon_info(dict_data['bname'])
                self.__send_enque(dict_data=result)

