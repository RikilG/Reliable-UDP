# Declaring bit constants
ACK = 0b10000000 # ACK bit - acknowledgement
SYN = 0b01000000 # SYN bit - synchronize
FIN = 0b00100000 # FIN bit - finish
NUL = 0b00010000 # NUL bit - null
BEG = 0b00001000 # CTL bit - beginning of data
END = 0b00000100 # END bit - end of data

class Packet:
    
    def __init__(self, seqNo, ackNo, flags, data="", binary=None):
        # content-length field is < 2 bytes only (6 bytes for header, 2 for safety!)
        assert len(data) <= 0b1111111111111000 # 0xffff
        assert type(data) in [str, bytes, bytearray]
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
        dataLen0 = (len(data) >> 8) & 0b11111111
        dataLen1 = (len(data)) & 0b11111111
        checksum = (((seqNo + ackNo + flags + dataLen0 + dataLen1) ^ 0b11111111) + 1) & 0b11111111
        # 6 byte headers
        self.headers = bytearray([seqNo, ackNo, flags, checksum, dataLen0, dataLen1])
        if type(data) == str:
            self.payload = data.encode('utf-8')
        else:
            self.payload = data
        self.binary = self.headers + self.payload
    
    def toBytes(self):
        return self.binary
    
    def toPacket(x): # static func, NO self keyword req
        v = ( ( sum(x[0:6]) & 0b11111111 ) == 0 )
        assert v == True, "Checksum verification failed!"
        return Packet(x[0], x[1], x[2], x[6:], x)
        
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
    NUL: {self.getFlag(NUL)},
    BEG: {self.getFlag(BEG)},
    END: {self.getFlag(END)}
]
content-length: {len(self.data)},
data: 
{self.data}
        """