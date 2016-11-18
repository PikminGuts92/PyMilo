import os # file/stream
import struct

class AwesomeReader():

    def __init__(self, filePath, bigEndian = False):
        self.__endianChar = ">" if bigEndian else "<"
        
        try:
            self.__stream = open(filePath, "rb")
        except:
            self.__stream = None
    
    def __del__(self):
        self.__stream.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__stream.close()
    
    def getBigEndian(self):
        return self.__endianChar == ">"
    
    def setBigEndian(self, bigEndian):
        self.__endianChar = ">" if bigEndian else "<"

    def getPosition(self):
        if self.__stream == None:
            return 0
        else:
            return self.__stream.tell()
    
    def setPosition(self, position):
        if self.__stream == None:
            return
        else:
            self.__stream.seek(position, 0)
    
    def readBytes(self, length):
        return self.__stream.read(length)
    
    def readHalf(self):
        return 0.0

    # Reads single precision floating-point (32-bit)
    def readSingle(self):
        return struct.unpack(self.__endianChar + "f", self.__stream.read(4))[0]
    
    # Reads double precision floating-point (64-bit)
    def readDouble(self):
        return struct.unpack(self.__endianChar + "d", self.__stream.read(8))[0]
    
    # Reads 8-bit integer
    def readInt8(self):
        return struct.unpack(self.__endianChar + "b", self.__stream.read(1))[0]
    
    # Reads 8-bit unsigned integer
    def readUInt8(self):
        return struct.unpack(self.__endianChar + "B", self.__stream.read(1))[0]
    
    # Reads 16-bit integer
    def readInt16(self):
        return struct.unpack(self.__endianChar + "h", self.__stream.read(2))[0]

    # Reads 16-bit unsigned integer
    def readUInt16(self):
        return struct.unpack(self.__endianChar + "H", self.__stream.read(2))[0]
    
    # Reads 24-bit integer
    def readInt24(self):
        data = self.readBytes(3)
        
        if self.getBigEndian():
            data.reverse()
        
        return (data[0] << 0 | data[1] << 8 | data[2] << 16)

    # Reads 24-bit unsigned integer

    # Reads 32-bit integer
    def readInt32(self):
        return struct.unpack(self.__endianChar + "i", self.__stream.read(4))[0]
    
    # Reads 32-bit unsigned integer
    def readUInt32(self):
        return struct.unpack(self.__endianChar + "I", self.__stream.read(4))[0]
    
    # Reads 64-bit integer
    def readInt64(self):
        return struct.unpack(self.__endianChar + "q", self.__stream.read(8))[0]

    # Reads 64-bit unsigned integer
    def readUInt64(self):
        return struct.unpack(self.__endianChar + "Q", self.__stream.read(8))[0]
    
    # Reads null-termined string
    def readNullString(self):
        return ""
    
    # Reads string with 32-bit length preceding
    def readString(self):
        return ""

    # Reads string with given length
    def readString(self, length):
        return ""
    