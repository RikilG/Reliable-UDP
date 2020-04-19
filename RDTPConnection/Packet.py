import json

ACK = 0b10000000 # ACK bit
SYN = 0b01000000 # SYN bit
FIN = 0b00100000 # FIN bit
NUL = 0b00010000 # NUL bit

class Packet:
    
    def __init__(self, seqNo, ackNo, flags, data="", binary=None):
        # content-length field is < 2 bytes only (6 bytes for header, 2 for safety!)
        assert len(data) <= 0b1111111111111000 # 0xffff
        assert type(data) == str
        assert type(flags) == int
        seqNo = seqNo%256
        ackNo = ackNo%256
        self.seqNo = seqNo
        self.ackNo = ackNo
        self.flags = flags # ACK | SYN | FIN | NUL
        self.data = data
        if binary != None:
            self.binary = binary
            return
        # flagbits = 0b00000000
        # if flags[0]: flagbits | 0b10000000 # ACK bit
        # if flags[1]: flagbits | 0b01000000 # SYN bit
        # if flags[2]: flagbits | 0b00100000 # FIN bit
        # if flags[3]: flagbits | 0b00010000 # NUL bit
        # 1 bit checksum field
        dataLen0 = (len(data) >> 8) & 0b11111111
        dataLen1 = (len(data)) & 0b11111111
        checksum = (((seqNo + ackNo + flags + dataLen0 + dataLen1) ^ 0b11111111) + 1) & 0b11111111
        # 6 byte headers
        self.headers = bytearray([seqNo, ackNo, flags, checksum, dataLen0, dataLen1])
        self.payload = data.encode('utf-8')
        self.binary = self.headers + self.payload
    
    def toBytes(self):
        # return json.dumps(self.data).encode('utf-8')
        return self.binary
    
    def toPacket(x): # static func, NO self req
        # try:
        #     temp = json.loads(x.decode('utf-8'))
        # except Exception as e:
        #     return None
        # return Packet(temp["seqNo"], temp["ackNo"], temp["flags"], temp["attrs"], temp["data"])
        
        # checksum verification
        v = ( ( sum(x[0:6]) & 0b11111111 ) == 0 )
        assert v == True, "Checksum verification failed!"

        # flagbits = x[2]
        # flags = [False] * 4
        # if flagbits & 0b10000000: flags[0] = True # ACK set
        # if flagbits & 0b01000000: flags[1] = True # SYN set
        # if flagbits & 0b00100000: flags[2] = True # FIN set
        # if flagbits & 0b00010000: flags[3] = True # NUL set
        return Packet(x[0], x[1], x[2], x[6:].decode('utf-8'), x)
        
    def getFlag(self, x):
        return (self.flags & x) > 0
    
    def __str__(self):
        return f"""PACKET:
seqNo: {self.seqNo},
ackNo: {self.ackNo},
flags: [
    ACK: {self.getFlag(ACK)},
    SYN: {self.getFlag(SYN)},
    FIN: {self.getFlag(FIN)},
    NUL: {self.getFlag(NUL)}
]
content-length: {len(self.data)},
data: 
{self.data}
        """