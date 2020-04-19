from .Socket import RDTPSocket

def data_fun_default(data):
    print("DATA: ", data)

class RDTPReceiver:

    def __init__(self):
        self.socket = RDTPSocket()

    def listen(self, on_data_run=data_fun_default, port=8448): # default listener port on 8448
        self.socket.bind(port)
        print(f"RDTP receiver listening on port: {port}")
        # send a routine/method to run in case of data received
        self.socket.listen(on_data_run)
        print()

    def receive(self):
        pass

    def close(self):
        pass
