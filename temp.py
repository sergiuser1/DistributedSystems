from gate import receiveJson, sendJson
import socket
import threading
import time

dict = {'name':"Jack",
        'age':21,
        'ee':(1,23,4, "ey")
}

def trySend(host, port, dict):
    time.sleep(1)

    sendJson(host, port, dict)
host = socket.gethostname()
port = 995
threading.Thread(target=trySend, args=(host, port, dict)).start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket
s.bind((host, port))
s.listen(1)
connection, address = s.accept()

data = receiveJson(connection)

print(data['ee'])




# 100 = writers queue is full
# 0 = ok

