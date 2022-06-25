import threading, socket, pickle
from user import User
IP = socket.gethostname() # change
PORT = 7777 # change
class Server(object):
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP,PORT))
        self.server.listen()

        self.accounts = {'FLR':'123'}
        self.clients = {}
    
    def parse(self, data: dict, socket: socket.socket) -> None:
        print(data)
        if (action := data.get("action")):
            if action == "send":
                data = {"action": "message", "data": data.get("data"), "username": self.clients[socket].user()}
                print(data)
                return self.broadcast(pickle.dumps(data), socket)

    
    def connect(self, address: tuple, socket: socket.socket) -> None:
        data: dict = pickle.loads(socket.recv(512))
        assert isinstance(data, dict), socket.send(b"Error while processing your request")
        if data.get("action") == "login":
            if self.login(data.get("username"), data.get("password")):
                self.clients.setdefault(socket, User(data.get("username"), address))
                socket.send(b"Succes")
                return self.listen(socket)
            else:
                socket.send(b"Bad username / password")
                return self.connect(address, socket)
        if data.get("action") == "register":
            self.register(data.get("username"), data.get("password"),socket)
            socket.send(b"Succes")
            return self.connect(address, socket)
            

    def disconnect(self, socket: socket.socket) -> None:
        del self.clients[socket]; return socket.close()
    
    def register(self, username: str, password: str, socket: socket.socket) -> None:
        if self.accounts.get(username): return socket.send(b"Acest cont exista deja")

        self.accounts.setdefault(username, password)
        return print(self.accounts)

    def broadcast(self, data: bytes, fwsocket: socket.socket) -> None:
        for socket in self.clients.copy().keys():
            self.send(data, socket)

    def login(self, username: str, password: str) -> bool:
        return True if self.accounts.get(username) == password else False
    
    def users(self) -> bytes:
        return pickle.dumps([user.user() for user in self.clients.copy().values()])

    def send(self, data: bytes, socket: socket.socket) -> None:
        print("Sending to", self.clients[socket].user(), pickle.loads(data))
        return socket.send(data)

    def listen(self, socket: socket.socket) -> None:
        while True:
            try:
                data = socket.recv(2048)
                if not data: raise
                self.parse(pickle.loads(data), socket)
            except Exception as error:
                print(error)
                return self.disconnect(socket)

    def main(self) -> None:
        while True:
            client, address = self.server.accept()
            threading.Thread(target = self.connect, args = (address, client)).start()

Server().main()