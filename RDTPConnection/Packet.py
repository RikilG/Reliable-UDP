# Declaring bit constants
ACK = 0b10000000 # ACK bit - acknowledgement
SYN = 0b01000000 # SYN bit - synchronize/connect
FIN = 0b00100000 # FIN bit - finish/disconnect
NUL = 0b00010000 # NUL bit - null/ping
BEG = 0b00001000 # CTL bit - beginning of data
END = 0b00000100 # END bit - end of data

class Packet:
    """Packet class following RDTP packet specifications.
    6 byte header: consists of sequence no, acknowledgement no, flags, checksum, data-length
    payload: cannot exceed 2**15(safe limit). UDP packet max size is 2**16 including headers
    """
    
    def __init__(self, seqNo, ackNo, flags, data="", data_index=0, binary=None):
        """Packet class constructor"""
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
        self.data_index = data_index
        if binary != None:
            self.binary = binary
            return
        if type(data) == str:
            self.payload = data.encode('utf-8')
        else:
            self.payload = data
        dataLen0 = (len(data) >> 8) & 0b11111111
        dataLen1 = (len(data)) & 0b11111111
        checksum = (((seqNo + ackNo + flags + data_index + dataLen0 + dataLen1 + sum(self.payload)) ^ 0b11111111) + 1) & 0b11111111
        # 6 byte headers
        self.headers = bytearray([seqNo, ackNo, flags, data_index, dataLen0, dataLen1, checksum])
        self.binary = self.headers + self.payload
    
    def toBytes(self):
        return self.binary
    
    def toPacket(x):
        """A (static) method which converts a given binary/bytes/bytearray 
        to packet class object"""
        v = ( ( sum(x) & 0b11111111 ) == 0 )
        if v != True: raise Exception("Checksum verification failed!")
        return Packet(x[0], x[1], x[2], x[7:], x[3], x)
        
    def getFlag(self, x):
        """Return wheter corresponding flag is set or not"""
        return (self.flags & x) > 0
    
    def __str__(self):
        """Called by print(), one of python dunder/magic methods"""
        flags = ""
        if self.getFlag(ACK):
            flags += "\tACK: Acknowledgement\n"
        if self.getFlag(SYN):
            flags += "\tSYN: Syncronize/Connect\n"
        if self.getFlag(FIN):
            flags += "\tFIN: Finish/Terminate\n"
        if self.getFlag(NUL):
            flags += "\tNUL: Ping Packet\n"
        if self.getFlag(BEG):
            flags += "\tBEG: Data Begin\n"
        if self.getFlag(END):
            flags += "\tEND: Data End\n"
        
        return f"""PACKET:
seqNo: {self.seqNo},
ackNo: {self.ackNo},
flags: [
{flags}],
data-index: {self.data_index},
content-length: {len(self.data)},
data: {self.data}
        """