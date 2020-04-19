import socket
import random
from .Packet import Packet
from .Packet import ACK, SYN, FIN, NUL

# TODO: NOTE: apply mods to seq numbers

class RDTPSocket:
    # implement packet division, transfer, in-order and reliability

    def __init__(self, ip=None, port=None):
        self.local_ip = "127.0.0.1"
        self.target_address = (ip, port)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.seqNo = 0
        self.ackNo = 0
        self.conn_status = "OPEN"
        self.app_data = None
    
    def bind(self, port):
        self.socket.bind((self.local_ip, port))
    
    def close(self):
        if self.conn_status == "ESTABLISHED":
            self.terminate()
        self.socket.close()

    def send(self, data, receiver=False, no_incr=False):
        assert type(data) == Packet
        if receiver:
            self.socket.sendto(data.toBytes(), self.conn_address)
        else:
            self.socket.sendto(data.toBytes(), self.target_address)
        if no_incr == False:
            self.seqNo = (self.seqNo + 1) % 256
            self.ackNo = (self.ackNo + 1) % 256

    def receive(self, timeout=5, bufsize=4096):
        self.socket.settimeout(timeout)
        try:
            binary, address = self.socket.recvfrom(bufsize) #1024 is buffersize
            self.conn_address = address
            message = Packet.toPacket(binary)
            if self.conn_status == "ESTABLISHED" and not message.getFlag(FIN) and message.ackNo != self.seqNo :
                print("incorrect ACK received")
                print(message)
        except socket.timeout:
            return None
        except Exception as e:
            print(e)
            return None
        return message
    
    def ping(self):
        flags = NUL
        # NUL packet
        packet = Packet(0, 0, flags)
        self.send(packet)
        response = self.receive()
        if response is None:
            return False
        else:
            return True
    
    #################### Sender Methods ####################

    def handshake(self):
        # check if host is online with ping
        if not self.ping():
            return "Ping Error"
        # generate a random starting sequence number
        self.seqNo = random.randint(0, 2**8-1)
        # SYN packet
        packet = Packet(self.seqNo, 0, SYN)
        self.send(packet)
        # await for SYN-ACK packet from receiver
        response = self.receive()
        if response == None: return 1
        if not (response.getFlag(ACK) and response.getFlag(SYN) and response.ackNo == self.seqNo):
            print("Incorrect handshake packet received")
            print(response)
            print(response.ackNo)
            print(self.seqNo)
            return 1
        self.ackNo = response.seqNo + 1
        self.conn_status = "ESTABLISHED"
        # complete handshake
        packet = Packet(self.seqNo, self.ackNo, ACK)
        self.send(packet)
        print("Connection accepted by target")

    def terminate(self):
        response = None
        while response == None: # 
            # send FIN packet
            packet = Packet(self.seqNo, self.ackNo, FIN)
            self.send(packet, no_incr=True) # don't increment seqno until target accepts FIN
            # wait for fin-ack from receiver
            response = self.receive()
            if response is not None and response.getFlag(ACK) and response.getFlag(FIN):
                break
        # host fin-ack received
        self.seqNo = (self.seqNo + 1)%256
        self.ackNo = (self.ackNo + 1)%256
        # send ack for fin-ack packet and terminate
        packet = Packet(self.seqNo, self.ackNo, FIN|ACK)
        self.send(packet)
        self.conn_status == "OPEN"
        print("Terminated connection with receiver")

    ################### Receiver Methods ###################
    
    def inbound_conn(self, packet):
        self.seqNo = random.randint(0, 2**8-1)
        self.ackNo = packet.seqNo + 1
        # send SYN-ACK packet
        packet = Packet(self.seqNo, self.ackNo, SYN | ACK)
        self.send(packet, receiver=True)
        # wait for response to complete handshake
        response = self.receive()
        if response == None:
            print("Timeout: No packet response for handshake")
            return
        elif response.getFlag(ACK) and response.ackNo == self.seqNo:
            self.conn_status = "ESTABLISHED"
        print(">> Inbound connection accepted")
    
    def inbound_term(self):
        response = None
        i = 0
        while response is None:
            if i==5: break # send at most 5 packets
            packet = Packet(self.seqNo, self.ackNo, FIN | ACK)
            self.send(packet, receiver=True, no_incr=True)
            i+=1
            response = self.receive()
            if response is not None and response.getFlag(ACK):
                break;
        # end connection
        self.conn_status = "OPEN"
        print(">> Inbound connection terminated")
    
    def listen(self):
        while True:
            # listen for connections
            response = self.receive(timeout=3600) # 1hr
            if response == None: return 0
            # on SYN packet
            if response.getFlag(SYN) and self.conn_status == "OPEN": # SYN flag
                print("Receiver: Initializing inbound connection")
                self.inbound_conn(response)
            # if we receive ping
            elif response.getFlag(NUL): # NUL flag
                print("Receiver: Ping packet received")
                packet = Packet(0, 0, ACK)
                self.send(packet, receiver=True)
            elif self.conn_status == "ESTABLISHED" and response.getFlag(FIN):
                # FIN packet received send FIN-ACK packet
                print("Receiver: Terminating inbound connection")
                self.inbound_term()
            else: # any other packet # check if conn est and react
                pass