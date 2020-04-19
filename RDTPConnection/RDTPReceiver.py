from .Socket import RDTPSocket

class RDTPReceiver:

    def __init__(self):
        self.socket = RDTPSocket()

    def listen(self, port=8448): # default listener port on 8448
        self.socket.bind(port)
        print(f"RDTP receiver listening on port: {port}")
        while self.socket.app_data == None:
            self.socket.listen()
            print()

    def receive(self):
        pass

    def close(self):
        pass
