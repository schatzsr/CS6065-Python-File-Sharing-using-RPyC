# Intro to Cloud Computing
# Project 1: Python File Sharing using RPyC (RPC)
# Authors: Anthony Kleiser, Sean Schatzman
# https://docs.google.com/document/d/1_ITW-OmGvtsFgbbr-lJQHCyihWIjZMHnFu85CWQSTzo/edit


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
    inputfile = open(filename, 'rb')
    return inputfile.read()

def receiveAndUnpack(binary, filename):
    """
    Open File to write to and write input
    binary to the new file
    """
    inputfile = open(filename, 'wb')
    inputfile.write(binary)

'''
Set client variables
   name          = user's name
   shareFolder   = path to folder with shared files
   receiveFolder = path to folder to store received files
'''
firstRun = True
connected = False

while True:

    if firstRun:

        shareFolder = sys.argv[1]
        receiveFolder = sys.argv[2]
        if not os.path.exists(shareFolder) or not os.path.exists(receiveFolder):
            print "Please enter a valid share and/or receive directory"
            break

        # Connect to RPyC with input ip, if no input ip then default to localhost.
        if len(sys.argv) == 4:
            try:
                c = rpyc.connect(sys.argv[3], 18861)
                connected = True
            except:
                print "Invalid IP Address. Please enter a valid address or start a Localhost"
                break
        elif len(sys.argv) == 3:
            try:
                c = rpyc.connect("localhost", 18861)
                connected = True
            except:
                print "Localhost not found, please start a local server instance or enter a valid IP Address."
                break

        name = raw_input("Enter Your Name:")

        # In order to print the messages from others while the client thread
        # is waiting for keyboard input, start up a background listening thread.
        bgsrv = rpyc.BgServingThread(c)

        # Make files in shareFolder available to other users by adding to the server.
        fileNames = []
        fileBins = []
        for f in os.listdir(shareFolder):
            fileNames.append(f)
            fileBins.append(openAndPack(shareFolder + "/" + f))
        c.root.addUser(name, fileNames, fileBins)
        firstRun = False

    # Send the function to print a message to my screen to the server
    c.root.setCallback(showSharedFiles)
    userInput = raw_input("Type 'ls' to show available files, '#<userID>:<docID>' to download, or 'q' to quit.\n")
    if userInput == "ls":
        display = c.root.showFiles()
        print display
    elif userInput[0] == "#":
        removePound = userInput.replace("#", "")
        inputList = removePound.split(":")
        userID = inputList[0]
        docID = inputList[1]
        fileInfo = c.root.sendFile(userID, docID)
        print(type(fileInfo))
        try:
            fileInfo[0] = str(fileInfo[0])
            fileName = receiveFolder + "/" + fileInfo[0]
            receiveAndUnpack(fileInfo[1], fileName)
            print "File Retrieve Successful"
        except TypeError:
            print "File Retrieve Failed - please ensure valid inputs"
    elif userInput == "q":
        break

if connected:
    bgsrv.stop()
    c.close()