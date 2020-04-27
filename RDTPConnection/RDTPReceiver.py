from .SWSocket import RDTPSocket

def data_fun_default(data):
    """This is an example function which runs when some data is 
    received by the receiver listening socket. You can print to 
    console, write to file or send it anywhere using this method"""
    print("DATA: ", data)

class RDTPReceiver:
    """A Wrapper class to enclose server/receiver functions and 
    provide abstraction to RDTPSocket class"""

    def __init__(self):
        """RDTPReceiver class constructor"""
        self.socket = RDTPSocket()

    def listen(self, on_data_run=data_fun_default, port=8448):
        """This method binds the socket to given port 
        (default 8448) and starts listening for inbound 
        connections"""
        self.socket.bind(port)
        print("Press Ctrl-C to exit")
        print(f"RDTP receiver listening on port: {port}")
        self.socket.listen(on_data_run)

    def close(self):
        """Method to close the socket properly"""
        self.socket.close()
