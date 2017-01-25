import sys
from MiloContainer import MiloContainer

'''
    Arguments: [ miloPath, outputMiloPath ]
'''
def main(argv):
    if len(argv) < 3:
        print("Args: miloPath outputMiloPath")
        return
    
    milo = MiloContainer(argv[1])
    milo.writeRawBytesToFile(argv[2])
    print("Saved milo file to", argv[2])

if __name__ == "__main__":
    main(sys.argv)