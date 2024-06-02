from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue
import time
from src.network_provider import NetworkProvider

if __name__=="__main__":
    netWorkProvider=NetworkProvider()
    netWorkProvider.start()