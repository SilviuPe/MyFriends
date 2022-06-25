class User(object):
    def __init__(self, username: str, address: tuple) -> None:
        self.address, self.username = address, username
    
    def addr(self) -> tuple: return self.address
    
    def user(self) -> str: return self.username
