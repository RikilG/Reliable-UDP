from .SRSocket import RDTPSocket

class RDTPSender:
    """A Wrapper class to enclose sender/client methods 
    and prSWovide abstraction to RDTPSocket class"""

    def __init__(self):
        """RDTPSender class constructor"""
        self.socket = RDTPSocket()

    def connect(self, ip, port=8448):
        """Start a RDTP connection to remote host with given 
        ip and port number (default 8448)"""
        self.socket.target_address = (ip, port)
        res = self.socket.handshake()
        if res == "Ping Error":
            print("Timeout: Receiver unreachable or bad connection: Ping Error")
            self.close()
            exit() # TODO: try a softer exit method
            return False
        return self.socket.conn_status == "ESTABLISHED"

    def send(self, data):
        """Method to send data using RDTP over established 
        connection"""
        assert self.socket.conn_status == "ESTABLISHED", "Connection not established"
        if type(data) == str: data = data.encode('utf-8')
        assert type(data) in [bytes, bytearray], "Invalid data type"
        print("Sending data")
        self.socket.send_stream(data)

    def close(self):
        """Method to close the socket properly"""
        self.socket.close()
