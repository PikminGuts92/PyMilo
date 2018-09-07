import sys
import os
from MiloContainer import MiloContainer

def get_file_names_in_directory(inputDir, workingFiles):
    inputDir = os.path.abspath(inputDir)

    dirs = [f for f in os.listdir(inputDir) if not os.path.isfile(os.path.join(inputDir, f))]

    for dir in dirs:
        get_file_names_in_directory(os.path.join(inputDir, dir), workingFiles)

    files = [f for f in os.listdir(inputDir) if os.path.isfile(os.path.join(inputDir, f))]

    for f in files:
        workingFiles.append(os.path.join(inputDir, f))


def inflate_milos(inputDir, outputDir):
    '''
    '''
    #inFiles = [f for f in os.listdir(inputDir) if os.path.isfile(os.path.join(inputDir, f))]

    files = []
    get_file_names_in_directory(inputDir, files)

    for f in files:
        ext = os.path.splitext(f)[1][1:].lower()
        if ('milo' not in ext):
            continue

        

        newPath = f.replace(inputDir, outputDir)
        splitPath = newPath.split('\\')

        # Moves up one directory if in 'gen'
        if 'gen' in splitPath[-2].lower():
            splitPath = splitPath[:-2] + splitPath[-1:]
            
        newPath = '\\'.join(splitPath)

        milo = MiloContainer(f)
        if not milo.writeRawBytesToFile(newPath):
            print('Unable to save milo to', newPath)
        else:
            print('Saved milo to', newPath)

    pass

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        inflate_milos(sys.argv[1], sys.argv[2])
        pass
    else:
        print('Expected two arguments')
