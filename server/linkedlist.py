class Node:
    def __init__(self, client_socket, addr, next_node=None):
        self.client_socket = client_socket
        self.addr = addr
        self.next = next_node

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, client_socket, addr):
        if not self.head:
            self.head = Node(client_socket, addr)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(client_socket, addr)

    def remove(self, client_socket):
        current = self.head
        prev = None
        while current:
            if current.client_socket == client_socket:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def get_all_sockets(self):
        current = self.head
        sockets = []
        while current:
            sockets.append(current.client_socket)
            current = current.next
        return sockets
