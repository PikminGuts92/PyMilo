import struct
import zlib
import gzip
from AwesomeReader import *

class CompressionType:
    '''
    Raw data. Uncompressed.
    '''
    NONE = 0
    '''
    Raw data. Compressed with GZip.

    Games:
        Frequency
    '''
    GZIP = 1
    '''
    Structured as milo. No compression.

    Games:
        Rock Band Network
    '''
    MILO_A = 0xCABEDEAF
    '''
    Structured as milo. Compressed with ZLib.

    Games:
        Guitar Hero
        Guitar Hero II
        Guitar Hero Encore: Rocks The 80's
        Rock Band
        Rock Band Track Pack Vol. 1
        Rock Band 2
        AC/DC Live: Rock Band Track Pack
        Rock Band Track Pack Vol. 2
        Rock Band Track Pack: Classic Rock
        Rock Band Country Track Pack
        The Beatles: Rock Band
        Rock Band Metal Track Pack
        LEGO: Rock Band
        Green Day: Rock Band
        Rock Band Country Track Pack 2
    '''
    MILO_B = 0xCBBEDEAF
    '''
    Structured as milo. Compressed with GZip.

    Games:
        Amplitude
        Karaoke Revolution
        Karaoke Revolution Vol. 2
        Karaoke Revolution Vol. 3
    '''
    MILO_C = 0xCCBEDEAF
    '''
    Structured as milo. Compressed with ZLib.

    Games:
        Rock Band 3
        Dance Central
        Dance Central 2
        Dance Central 3
        Rock Band Blitz
    '''
    MILO_D = 0xCDBEDEAF

def decompressBlock(block, compression):
    ZLIB_INFO = bytes([0x78, 0x9C]) # Required for decompression

    if compression == CompressionType.MILO_B:
        # ZLib pre-RB3 compressed
        z = zlib.decompressobj()
        z.decompress(ZLIB_INFO)
        return z.decompress(block)
        
    elif compression == CompressionType.MILO_C:
        # GZIP compressed
        return gzip.decompress(block)

    elif compression == CompressionType.MILO_D:
        # ZLib post-RB3 compressed
        z = zlib.decompressobj()
        z.decompress(ZLIB_INFO)
        return z.decompress(block[4:len(block) -1])

    else:
        # Unsupported or already decompressed
        return block

def compressBlock(block, compression):
    # TODO: Implement compression
    return block

class MiloContainer:

    def __init__(self, miloPath):

        with AwesomeReader(miloPath, False) as ar:
            startingOffset = ar.getPosition()
            magic = ar.readUInt32()

            if not (magic == CompressionType.MILO_A or
                magic == CompressionType.MILO_B or
                magic == CompressionType.MILO_C or
                magic == CompressionType.MILO_D):
                return
            
            self._compression = magic
            offset = ar.readUInt32()

            blockCount = ar.readUInt32()
            ar.readInt32() # Largest block (Not needed)

            
            blockSize = []
            blockCompressed = []
            maxSize = 1 << 24 # 2^24 (~16 million)

            # Reads block sizes
            for i in range(blockCount):
                blockSize.append(ar.readInt32())
                blockCompressed.append(True)
                
                if (self._compression == CompressionType.MILO_D):
                    blockCompressed[i] = blockSize[i] & maxSize == 0
                    blockSize[i] = blockSize[i] & ~maxSize

                elif (self._compression == CompressionType.MILO_A):
                    blockCompressed[i] = False
                
            # Jumps to first block offset
            ar.setPosition(startingOffset + offset)


            miloBytes = bytearray()
            for i in range(blockCount):
                block = ar.readBytes(blockSize[i])

                # Decompress block
                if (blockCompressed[i]):
                    block = decompressBlock(block, self._compression)

                # Write block to 'stream'
                miloBytes.extend(block)
            
            # Sets raw bytes
            self.rawBytes = bytes(miloBytes)

    def writeRawBytesToFile(self, outPath):
        try:
            # Writes bytes to file
            with open(outPath, "wb") as out:
                out.write(self.rawBytes)
        except:
            return