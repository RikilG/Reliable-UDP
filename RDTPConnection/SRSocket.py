from math import ceil
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
        self.chunk_size = 2**11 # default 2*11. try to not exceed this value
        self.win_size = 128 # should not go beyond 128 as our index width is 8 bytes
    
    #################### Sender Methods ####################

    def send_window(self, data, win_start, win_end, acked):
        for p in range(win_start, win_end):
            if acked[p] == 0:
                self.send(Packet(self.seqNo, self.ackNo, 0, data[p], p-win_start))

    def send_stream(self, data):
        chunk_size = self.chunk_size
        # divide the input data into chunks to fit in packets
        data = [ data[i*chunk_size:(i+1)*chunk_size] for i in range(ceil(len(data)/chunk_size)) ]
        # start with a Begining BEG signal
        self.sendTillAck(Packet(self.seqNo, self.ackNo, BEG, f"{len(data)}"))
        win_size = self.win_size
        # keep track of successfully send packets using a acked array
        acked = [0]*len(data)
        for i in range(ceil(len(data)/win_size)): # for each window
            win_start = i*win_size
            win_end = min((i+1)*win_size, len(data))
            # wait for acks and mark which are received
            while sum(acked[win_start:win_end]) != len(acked[win_start:win_end]):
                self.send_window(data, win_start, win_end, acked)
                response = None
                while response != "timeout" and sum(acked[win_start:win_end]) != len(acked[win_start:win_end]):
                    response = self.receive()
                    if type(response) == Packet and response.getFlag(ACK) and response.data_index+win_start < len(acked):
                        acked[ response.data_index + win_start ] = 1
                print(f"\r{round(sum(acked)*100/len(acked),1)}%...", end='')
        # END signal not required as we come out of loop only if all packets are ACKed
        # end the data transfer with a END signal
        self.sendTillAck(Packet(self.seqNo, self.ackNo, END), resend=2)
        print("Success!")

    ################### Receiver Methods ###################
    
    def inbound_stream(self, data_len):
        # TODO: NOTE: need to take care of FIN packet if it is sent
        chunk_size = self.chunk_size
        win_size = self.win_size
        data = [ 0 for i in range(data_len) ]
        received = [0]*len(data)
        for i in range(ceil(len(data)/win_size)): # for each window
            win_start = i*win_size
            win_end = min((i+1)*win_size, len(data))
            while sum(received[win_start:win_end]) != len(received[win_start:win_end]):
                response = self.receive()
                if type(response) is Packet and response.getFlag(FIN):
                    pass # TODO: manage finish signal
                if type(response) is Packet and response.data_index + win_start < len(data):
                    data[ response.data_index + win_start ] = response.data
                    received[ response.data_index + win_start ] = 1
                    self.send(Packet(self.seqNo, self.ackNo, ACK, data_index=response.data_index))
                print(f"\r{round(sum(received)*100/len(received), 1)}%...", end='')
            if response.getFlag(END):
                break;
        response = self.receive() # wait for END packet
        while response == "timeout" or not response.getFlag(END):
            if type(response) == Packet: 
                self.send(Packet(response.ackNo, response.seqNo+1, ACK, data_index=response.data_index))
            response = self.receive()
        self.send(Packet(self.seqNo, self.ackNo, ACK))
        print("Success!")
        return b''.join(data)