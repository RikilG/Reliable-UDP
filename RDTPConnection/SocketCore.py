import socket
import random
from .Packet import Packet
from .Packet import ACK, SYN, FIN, NUL, BEG, END

"""This class implements the Stop and Wait kind of protocol over the 
sockets by overriding the sender and receiver methods. 
"""

class Socket:
    # implement packet division, transfer, in-order and reliability

    def __init__(self, ip=None, port=None):
        self.local_ip = "127.0.0.1"
        self.target_address = (ip, port)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.seqNo = 0
        self.ackNo = 0
        self.conn_status = "OPEN"
        self.app_data = None
        self.receiver = False
    
    def bind(self, port):
        self.socket.bind((self.local_ip, port))
    
    def close(self):
        if self.conn_status == "ESTABLISHED":
            if self.receiver: # if you are the server, just send FIN and exit
                self.send(Packet(self.seqNo, self.ackNo, FIN))
            else:
                self.terminate()
        self.socket.close()

    def send(self, data, no_incr=False):
        assert type(data) == Packet
        if self.receiver:
            self.socket.sendto(data.toBytes(), self.conn_address)
        else:
            self.socket.sendto(data.toBytes(), self.target_address)
        if no_incr == False:
            self.seqNo = (self.seqNo + 1) % 256
        # print(":::SENDING >>", data)

    def receive(self, timeout=5, bufsize=2**12):
        self.socket.settimeout(timeout)
        try:
            binary, address = self.socket.recvfrom(bufsize)
            if self.conn_status == "OPEN":
                self.conn_address = address
            if self.conn_status == "ESTABLISHED" and address != self.conn_address:
                # packet from different sender drop it as we are connected with diff sender
                return self.receive(timeout, bufsize)
            message = Packet.toPacket(binary)
            # print(":::RECEIVING >>", message)
            if self.conn_status == "ESTABLISHED" and not message.getFlag(FIN) and message.ackNo < self.seqNo:
                if message.getFlag(ACK): # its an ACK for some old packet, drop it
                    print("^^^Received ack for past packet^^^")
                else: # its a data packet already received by us. just ack it
                    print("^^^Acking old data packet^^^")
                    self.send(Packet(message.ackNo, message.seqNo+1, ACK), no_incr=True)
                # return the next packet
                return self.receive(timeout, bufsize)
            if self.conn_status == "ESTABLISHED" and not message.getFlag(FIN) and message.ackNo != self.seqNo :
                # ackNo does not match our seqNo
                print("^^^Incorrect Packet received^^^")
                self.close()
                exit() # TODO: perform more graceful termination
        except socket.timeout:
            return "timeout"
        self.ackNo = (message.seqNo + 1) % 256
        return message
    
    def ping(self):
        # NUL packet, try 3 times at max
        response = self.sendTillAck(Packet(0, 0, NUL), resend=3)
        if response is None or response == "resend-limit-excedeed":
            return False
        else:
            return True
    
    def sendTillAck(self, packet, resend=12): # max-resend for 1 min
        response = None
        i = 0
        while type(response) is not Packet:
            # send packet
            self.send(packet)
            # wait for ACK
            response = self.receive()
            if type(response) == Packet and response.getFlag(ACK):
                break
            self.seqNo = (self.seqNo - 1) % 256
            if type(resend) == int:
                i += 1
                if i == resend: return "resend-limit-excedeed"
        self.ackNo = (response.seqNo + 1) % 256
        return response
    
    #################### Sender Methods ####################

    def handshake(self):
        print("Initiating connection...")
        # check if host is online with ping
        if not self.ping():
            return "Ping Error"
        # generate a random starting sequence number
        self.seqNo = random.randint(0, 2**8-1)
        # Send SYN and await for SYN-ACK packet from receiver
        response = self.sendTillAck(Packet(self.seqNo, 0, SYN))
        if not (response.getFlag(ACK) and response.getFlag(SYN) and response.ackNo == self.seqNo):
            print("Incorrect handshake packet received")
            return 1
        self.ackNo = response.seqNo + 1
        self.conn_status = "ESTABLISHED"
        # complete handshake
        self.send(Packet(self.seqNo, self.ackNo, ACK))
        print("Connection accepted by target")

    # OVERRIDE THIS METHOD
    def send_stream(self, data, chunk_size=2**11):
        # start with a Begining BEG signal and End with END signal
        # implement in child socket class which provide reliability
        pass

    def terminate(self):
        print("Terminating connection...")
        response = self.sendTillAck(Packet(self.seqNo, self.ackNo, FIN))
        # send ack for fin-ack packet and terminate
        self.send(Packet(self.seqNo, self.ackNo, FIN|ACK))
        self.conn_status == "OPEN"
        print("Terminated connection with receiver")

    ################### Receiver Methods ###################
    
    def inbound_conn(self, packet):
        self.seqNo = random.randint(0, 2**8-1)
        self.ackNo = packet.seqNo + 1
        # send SYN-ACK packet and wait for response to complete handshake
        self.sendTillAck(Packet(self.seqNo, self.ackNo, SYN | ACK))
        self.conn_status = "ESTABLISHED"
        print("\n>> Inbound connection accepted >>")
    
    # OVERRIDE THIS METHOD
    def inbound_stream(self):
        # TODO: NOTE: need to take care of FIN packet if it is sent
        # ACK for BEG and Stop receiveing when END packet is received
        pass
    
    def inbound_term(self):
        # send FIN-ACK packet, assume terminated if no ACK after 3 resends
        self.sendTillAck(Packet(self.seqNo, self.ackNo, FIN | ACK), resend=3)
        # end connection
        self.conn_status = "OPEN"
        print("<< Inbound connection terminated <<")
    
    def listen(self, on_data_run):
        # set the socket to be receiver type
        self.receiver = True
        timeout = 3600
        while True:
            # listen for connections
            response = self.receive(timeout=timeout) # 1hr

            if response is None: continue
            elif self.conn_status == "ESTABLISHED" and response == "timeout":
                print(f"<< Connection timeout: {timeout}s, Disconected <<")
                self.conn_status = "OPEN"
                timeout = 3600
            elif type(response) == str: print(response)
            # on SYN packet
            elif response.getFlag(SYN) and self.conn_status == "OPEN": # SYN flag
                self.inbound_conn(response)
                if self.conn_status == "ESTABLISHED":
                    timeout = 30
            # on NUL packet i.e., we receive ping
            elif response.getFlag(NUL): # NUL flag
                self.send(Packet(0, 0, ACK))
            # on FIN packet, terminate inbound connection
            elif self.conn_status == "ESTABLISHED" and response.getFlag(FIN):
                self.inbound_term()
                timeout = 3600
            # on BEG packet, start data collection
            elif self.conn_status == "ESTABLISHED" and response.getFlag(BEG):
                # ACK the BEG packet first
                self.send(Packet(self.seqNo, self.ackNo, ACK))
                data = self.inbound_stream(int(response.data))
                on_data_run(data)
            # any other packet, Don't care
            else: pass