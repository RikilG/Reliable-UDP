from .Socket import RDTPSocket
from .Packet import Packet

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
        assert self.socket.conn_status == "ESTABLISHED"
        if type(data) == str: data = data.encode('utf-8')
        assert type(data) in [bytes, bytearray], "Invalid data type"
        self.socket.send_stream(data)

    def close(self):
        self.socket.close()
