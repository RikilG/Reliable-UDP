import socket
import random
from .Packet import Packet
from .Packet import ACK, SYN, FIN, NUL, BEG, END


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
        self.receiver = False
    
    def bind(self, port):
        self.socket.bind((self.local_ip, port))
    
    def close(self):
        if self.conn_status == "ESTABLISHED":
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
        # print("SENDING>>", data)

    def receive(self, timeout=5, bufsize=2**12):
        self.socket.settimeout(timeout)
        try:
            binary, address = self.socket.recvfrom(bufsize) #1024 is buffersize
            self.conn_address = address
            message = Packet.toPacket(binary)
            # print("RECEIVING>>", message)
            if self.conn_status == "ESTABLISHED" and not message.getFlag(FIN) and message.ackNo < self.seqNo:
                if message.getFlag(ACK): # its an ACK for some old packet, drop it
                    print("Received old ack for some old packet")
                    return None
                else: # its a data packet already received by us. just ack it
                    print("Acking old data packet")
                    self.send(Packet(self.seqNo, message.seqNo+1, ACK), no_incr=True)
                    return None
            elif self.conn_status == "ESTABLISHED" and not message.getFlag(FIN) and message.ackNo != self.seqNo :
                # ackNo does not match our seqNo
                print("Incorrect ACK received")
                print(message)
                return None
        except socket.timeout:
            return "timeout"
        except Exception as e:
            print(e)
            return None
        self.ackNo = (message.seqNo + 1) % 256
        return message
    
    def sendTillAck(self, packet):
        response = None
        while response is None:
            # send packet
            self.send(packet)
            # wait for ACK
            response = self.receive()
            if type(response) == Packet and response.getFlag(ACK):
                break
            self.seqNo = (self.seqNo - 1) % 256
        self.ackNo = (response.seqNo + 1) % 256
    
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

    def send_stream(self, data, chunk_size=2**11):
        # start with a Begining BEG signal
        packet = Packet(self.seqNo, self.ackNo, BEG)
        self.sendTillAck(packet)
        s = 0
        while s+chunk_size <= len(data):
            packet = Packet(self.seqNo, self.ackNo, 0, data[s:s+chunk_size])
            self.sendTillAck(packet)
            s += chunk_size
        if s < len(data):
            packet = Packet(self.seqNo, self.ackNo, 0, data[s:])
            self.sendTillAck(packet)
        # end the data transfer with a END signal
        packet = Packet(self.seqNo, self.ackNo, END)
        self.sendTillAck(packet)

    def terminate(self):
        response = None
        while response == None: # 
            # send FIN packet
            packet = Packet(self.seqNo, self.ackNo, FIN)
            self.send(packet) # don't increment seqno until target accepts FIN
            # wait for fin-ack from receiver
            response = self.receive()
            if response is not None and response.getFlag(ACK) and response.getFlag(FIN):
                break
        # host fin-ack received
            self.seqNo = (self.seqNo - 1) % 256
        self.ackNo = (response.seqNo + 1) % 256
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
        self.send(packet)
        # wait for response to complete handshake
        response = self.receive()
        if response == None:
            print("Timeout: No packet response for handshake")
            return
        elif response.getFlag(ACK) and response.ackNo == self.seqNo:
            self.conn_status = "ESTABLISHED"
        print(">> Inbound connection accepted >>")
    
    def inbound_stream(self):
        # TODO: NOTE: need to take care of FIN packet if it is sent
        data = bytearray()
        response = None
        # ACK the BEG packet first
        packet = Packet(self.seqNo, self.ackNo, ACK)
        self.send(packet)
        while response is None or not response.getFlag(END):
            response = self.receive()
            if response != "timeout" and response != None:
                data += response.data
                # ACK your response
                packet = Packet(self.seqNo, self.ackNo, ACK)
                self.send(packet)
        self.seqNo = (self.seqNo + 1) % 256
        self.ackNo = (response.seqNo + 1) % 256
        # ACK the END packet
        packet = Packet(self.seqNo, self.ackNo, ACK)
        self.send(packet)
        return data
    
    def inbound_term(self):
        response = None
        i = 0
        while response is None:
            if i==5: break # send at most 5 packets
            packet = Packet(self.seqNo, self.ackNo, FIN | ACK)
            self.send(packet)
            i+=1
            response = self.receive()
            if response is not None and response.getFlag(ACK):
                break;
            self.seqNo = (self.seqNo - 1) % 256
        # end connection
        self.conn_status = "OPEN"
        print("<< Inbound connection terminated <<")
    
    def listen(self, on_data_run):
        self.receiver = True
        timeout = 3600
        while True:
            # listen for connections
            response = self.receive(timeout=timeout) # 1hr
            if response is None: continue
            elif self.conn_status == "ESTABLISHED" and response == "timeout":
                print(f"Connection timeout: {timeout}s, Disconected")
                self.conn_status = "OPEN"
                timeout = 3600
            elif type(response) == str: print(response)
            # on SYN packet
            elif response.getFlag(SYN) and self.conn_status == "OPEN": # SYN flag
                # print("Receiver: Initializing inbound connection")
                self.inbound_conn(response)
                if self.conn_status == "ESTABLISHED":
                    timeout = 30
            # if we receive ping
            elif response.getFlag(NUL): # NUL flag
                # print("Receiver: Ping packet received")
                packet = Packet(0, 0, ACK)
                self.send(packet)
            elif self.conn_status == "ESTABLISHED" and response.getFlag(FIN):
                # FIN packet received send FIN-ACK packet
                # print("Receiver: Terminating inbound connection")
                self.inbound_term()
                timeout = 3600
            elif self.conn_status == "ESTABLISHED" and response.getFlag(BEG):
                # print("Receiver: Data inbound")
                data = self.inbound_stream()
                on_data_run(data)
            else: # any other packet, Don't care
                pass