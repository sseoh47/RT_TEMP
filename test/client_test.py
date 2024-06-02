from socket import socket, AF_INET, SOCK_STREAM

def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))

    raw_data = "PATH STATION 경산시장"
    # raw_data = "BUS 840 dumy"

    client.send(raw_data.encode())

    recv_data = client.recv(1024).decode('utf-8')

    print(recv_data)


    
if __name__ == "__main__":
    main()