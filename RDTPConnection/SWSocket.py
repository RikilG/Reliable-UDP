from .SocketCore import Socket
from .Packet import Packet
from .Packet import ACK, SYN, FIN, NUL, BEG, END

class RDTPSocket(Socket):
    """This class implements the Stop and Wait kind of protocol over the 
    sockets by overriding the send_stream and inbound_stream methods. 
    """
    # implement packet division, transfer, in-order and reliability

    def __init__(self, ip=None, port=None):
        super().__init__(ip, port)
    
    #################### Sender Methods ####################

    def send_stream(self, data, chunk_size=2**11):
        # start with a Begining BEG signal
        self.sendTillAck(Packet(self.seqNo, self.ackNo, BEG, f"{len(data)}"))
        s = 0
        while True:
            self.sendTillAck(Packet(self.seqNo, self.ackNo, 0, data[s:s+chunk_size]))
            s += chunk_size
            print(f"\r{round(min(len(data),s)*100/len(data),1)}%...", end='')
            if s > len(data): break
        # end the data transfer with a END signal
        self.sendTillAck(Packet(self.seqNo, self.ackNo, END))
        print("Success!")

    ################### Receiver Methods ###################
    
    def inbound_stream(self, data_len):
        # TODO: NOTE: need to take care of FIN packet if it is sent
        data = bytearray()
        while True: # receive data until end packet
            response = self.receive(timeout=60)
            if response == "timeout":
                continue # TODO: End connection due to no response for a long time
            if response.getFlag(FIN):
                pass # TODO: manage finish signal
            # Append data and ACK your response
            data += response.data
            packet = Packet(self.seqNo, self.ackNo, ACK)
            self.send(packet)
            print(f"\r{round(len(data)*100/data_len, 1)}%...", end='')
            if response.getFlag(END):
                break;
        print("Success!")
        return data