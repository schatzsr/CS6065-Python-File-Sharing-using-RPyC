import sys,rpyc

def openAndPack(filename):
    #Open the passed file in read-binary mode
    #   and write the binary to a string.
    file = open(filename, 'rb')
    str = file.read()

def recieveAndUnPack(binary, filename):
    #Open File to write to and write input
    #   binary to the new file
    file = open(filename, 'wb')
    file.write(binary)

# Connect to RPyC with input ip, if no input
#   ip then default to localhost.
try:
    c = rpyc.conect(sys.argv[3], 18861)
except:
    c = rpyc.connect("localhost", 18861)

# In order to print the messages from others while the client thread
# is waiting for keyboard input, start up a background listening thread.
bgsrv = rpyc.BgServingThread(c)

# Set client variables
#   name          = user's name
#   shareFolder   = path to folder with shared files
#   receiveFolder = path to folder to store received files
name            = raw_input("Enter Your Name:")
shareFolder     = sys.argv[1]
receiveFolder   = sys.argv[2]

# Send the function to print a message to my screen to the server
c.root.setCallback(showMe)

while True:
  msg = raw_input()
  c.root.say(name + ":" + msg)


bgsrv.stop()
c.close()
