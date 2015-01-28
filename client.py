import sys
import os
import rpyc

def showSharedFiles(directory):
  print os.listdir(directory)

def openAndPack(filename):
    """
    Open the passed file in read-binary mode
    and write the binary to a string.
    """
    file = open(filename, 'rb')
    return file.read()

def receiveAndUnpack(binary, filename):
    """
    Open File to write to and write input
    binary to the new file
    """
    file = open(filename, 'wb')
    file.write(binary)

'''
Set client variables
   name          = user's name
   shareFolder   = path to folder with shared files
   receiveFolder = path to folder to store received files
'''
name            = raw_input("Enter Your Name:")
shareFolder     = sys.argv[1]
receiveFolder   = sys.argv[2]
firstRun        = True

while True:

    if(firstRun):
        # Connect to RPyC with input ip, if no input
        #   ip then default to localhost.
        try:
            c = rpyc.connect(sys.argv[3], 18861)
        except:
            c = rpyc.connect("localhost", 18861)

        # In order to print the messages from others while the client thread
        # is waiting for keyboard input, start up a background listening thread.
        bgsrv = rpyc.BgServingThread(c)

        # Make files in shareFolder availble to other
        #   users by adding to the server.
        fileNames = []
        fileBins = []
        for file in os.listdir(shareFolder):
            fileNames.append(file)
            fileBins.append(openAndPack(shareFolder + "/" + file))
        c.root.addUser(name, fileNames, fileBins)
        firstRun = False

    # Send the function to print a message to my screen to the server
    c.root.setCallback(showSharedFiles)
    userInput = raw_input("Type 'ls' to show available files, '#<userID>:<docID>' to download, or 'q' to quit.\n")
    if userInput == "ls":
        display = c.root.showFiles()
        print display
    elif userInput[0] == "#":
        userID = userInput[1]
        print userID
        docID = userInput[3]
        print docID
        fileInfo = c.root.sendFile(userID, docID)
        fileInfo[0] = str(fileInfo[0])
        fileName = receiveFolder + "/" + fileInfo[0]
        receiveAndUnpack(fileInfo[1], fileName)
        #selects user
        #selects file
        #asks server for file using user/filename
        #calls recieve and unpack for previous fileName and returned binary
    elif userInput == "q":
        #disconnect and remove user from the server
        print "You quitin' dis shit.....nah"


bgsrv.stop()
c.close()