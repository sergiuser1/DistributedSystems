import socket
import json
import threading


RECEIVE_BYTES = 4096 # Chunk size constant

# credit to
# https://eli.thegreenplace.net/2011/05/18/code-sample-socket-client-thread-in-python/
class Gate(threading.Thread):
    """ Each gate is a thread bound to a socket, that accepts connections and
        handles them.
    """
    def __init__(self, space, host, port=31415):
        super().__init__()
        self.alive = threading.Event()
        self.alive.set()
        self.daemon = True # make it a daemon so it closes when the program exists

        self.space = space
        self.source = host, port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket
        s.bind((host, port))
        s.listen(1) # since one socket is used per request, we have a CONN type connection.
        self.socket = s



    def run(self):
        while True:
            print("Waiting for connection")
            clientsocket, addr = self.socket.accept()
            print("Got a connection from {}".format(addr))
            with clientsocket: # making sure to close the socket once it's done
                request = receiveJson(clientsocket)
                action = request['action']
                source = request['source']
                host = source[0]
                port = source[1]
                if action == 'PUT_REQUEST':
                    response = self._handle_PUT(request)

                elif action == 'GET_RESPONSE':
                    response = self._handle_GET(request)

                elif action == 'GETP_REQUEST':
                    response = self._handle_GETP(request)

                elif action =='QUERY_REQUEST':
                    response = self._handle_QUERY(request)

                elif action == 'QUERYP_REQUEST':
                    response = self._handle_QUERYP(request)

                else:
                    response = self._message(request)
                    code = -1  # unknown request
                    message = 'unknown request'
                    response['code'] = code
                    response['message'] = message

                #sendJson(host, port, response)

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)


    def _handle_PUT(self, request):

        self.space.spaces[request['target']]['space'].put(tuple(request['tuple']))
        code = 0
        message = 'OK'
        response = self._message(request)
        response['code'] = code
        response['message'] = message
        response['action'] = request['action']

        return response

    def _handle_GET(self, request):
        if self.writers_q.qsize() > 0:
            code = 100  # writers queue is full
            message = 'writers queue is full'
            response = self._message(request)
            response['code'] = code
            response['message'] = message
            response['action'] = 'PUT_RESPONSE'

        else:
            self.space.spaces[request['target']].get(request['tuple'])
            code = 0
            message = 'OK'
            response = self._message(request)
            response['code'] = code
            response['message'] = message
            response['action'] = request['action']

    def _handle_GETP(self, request):
        self.space.spaces[request['target']]['space'].getp(tuple(request['tuple']))
        code = 0
        message = 'OK'
        response = self._message(request)
        response['code'] = code
        response['message'] = message
        response['action'] = request['action']

    def _handle_QUERY(self, request):
        pass # TODO

    def _handle_QUERYP(self, request):
        pass # TODO

    def _message(self, request):
            host, port = self.source
            return {
                'target': request['target'],
                'source': (host, port)
                }





def receiveJson(connection):
    """"
    This function gets a connection as an input and receives a dictionary formatted as JSON
    through that connection, then returns the data formatted as a dictionary.
    """
    data = []
    while True:
        chunk = connection.recv(RECEIVE_BYTES)
        if chunk == b'':
            break
        data.append(chunk)

    data = b"".join(data)
    decoded = json.loads(data.decode("utf-8"))
    return decoded


def sendJson(host, port, data):
    """
    This function sends a dictionary encoded as JSON to the target (host,port).
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = bytes(json.dumps(data).encode("utf-8")) # encoding the data so it cant be sent through a socket
        s.sendall(data)

