import rpyc

def showMe(message):
  print "->", message

def openAndPack(filename):
    f = open(filename, 'rb')
    pFile = f.read()


c = rpyc.connect("localhost", 18861)

# In order to print the messages from others while the client thread
# is waiting for keyboard input, start up a background listening thread.
bgsrv = rpyc.BgServingThread(c)

name = raw_input("Enter Your Name:")

# Send the function to print a message to my screen to the server
c.root.setCallback(showMe)

while True:
  msg = raw_input()
  c.root.say(name + ":" + msg)


bgsrv.stop()
c.close()
