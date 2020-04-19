from .Socket import RDTPSocket

class RDTPSender:

    def __init__(self):
        self.socket = RDTPSocket()

    def connect(self, ip, port=8448): # default listener on port 8448
        self.socket.target_address = (ip, port)
        res = self.socket.handshake()
        if res == "Ping Error":
            print("Receiver not online")
            return False
        return self.socket.conn_status == "ESTABLISHED"

    def send(self, data):
        pass

    def close(self):
        self.socket.close()
