import sys
from MiloContainer import MiloContainer
from tkinter import * # GUI Stuff
import tkinter.filedialog as filedialog
# import logging
# logging.basicConfig(filename='log.txt', level=logging.DEBUG)

root = Tk()

def main(argv):
    #root = Tk()
    init(root)
    
    # Runs main loop
    root.mainloop()

# Initializes main window
def init(window):
    BUTTON_HEIGHT = 3 # Size in terms of characters
    BUTTON_WIDTH = 9

    window.title("PyMilo GUI v1.0")
    window.minsize(1280, 720)
    
    # Toolbar
    menu = Menu(window)
    window.config(menu=menu)

    # Drop Down Button - File (Open, Exit)
    ddbFile = Menu(menu)
    menu.add_cascade(label="File", menu=ddbFile)
    ddbFile.add_command(label="Open", command=buttonOpenFile)
    ddbFile.add_separator()
    ddbFile.add_command(label="Exit", command=buttonExitProgram)

    # Help
    menu.add_cascade(label="Help")
    
    '''
    # Button - Open file
    openFile = Button(window)
    openFile["text"] = "Open"
    openFile["command"] = buttonOpenFile
    openFile["width"] = BUTTON_WIDTH
    openFile["height"] = BUTTON_HEIGHT

    # Button - Exit program
    exitProgram = Button(window)
    exitProgram["text"] = "Exit"
    exitProgram["command"] = buttonExitProgram
    exitProgram["width"] = BUTTON_WIDTH
    exitProgram["height"] = BUTTON_HEIGHT

    openFile.pack() # gird()
    exitProgram.pack()
    '''
    

# Open file function
def buttonOpenFile():
    file = filedialog.askopenfilename(title="Open", filetypes=[("MILO", ("*.milo", "*.milo_ps2", "*.milo_ps3", "*.milo_xbox", "*.milo_wii"))])
    
    if file:
        try:
            # Open file
            milo = MiloContainer(file)
            #logging.debug("Opened file {}".format(file))

            print("Opened file", file)
            pass
        except:
            # Handle Exception
            print("Error opening file")
            pass
    else:
        print("File dialog closed")

# Exit program function
def buttonExitProgram():
    print("Program exited")
    root.destroy()

if __name__ == "__main__":
    main(sys.argv)