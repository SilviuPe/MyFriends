import socket, pickle

IP = socket.gethostname() # change
PORT = 7777  # change

class Client(object):
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((IP,PORT))
    

        self.message, self.username = None, None

    def recv(self) -> None:
        data = self.server.recv(4096)
        try:
            return self.parse(pickle.loads(data))
        except:
            pass


    def parse(self, data: dict) -> None:
        if (action := data.get("action")):
            print(data)
            if action == "update":
                clients = pickle.loads(data.get("active-users"))
                #update la lista cu useri conectati

            elif action == "message":
                self.message, self.username = data.get("data"), data.get("username")
                return "message_done"

    def send(self, data: str) -> None:
        data = {"action": "send", "data": data}
        return self.server.send(pickle.dumps(data))

    def login(self, username: str, password: str) -> bool:

        self.server.send(pickle.dumps({"action": "login",
                                       "username": username,
                                       "password": password}))

        if (data := self.server.recv(256).decode()):
            print(data)
            if data == "Succes":
                return True
            
            elif data == "Bad username / password":
                return False
            
            else:
                return False
            
    def register(self, username: str, password: str) -> None:
        self.server.send(pickle.dumps({"action": "register",
                                       "username": username,
                                       "password": password}))

        return True
