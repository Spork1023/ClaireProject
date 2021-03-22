import socket
import sys
class Server:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("", 25273))
    s.listen()
    conn, addr = s.accept()

    print('Connected by', addr)

    conn.send(bytes([len(sys.argv[-1])]))
    conn.send(sys.argv[-1].encode())
    conn.close()