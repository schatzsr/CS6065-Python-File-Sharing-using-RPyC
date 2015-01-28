import rpyc

''' Class to store all external function calls
'''
class Service(rpyc.Service):
    def on_connect(self):
        pass

    def on_disconnect(self):
        print "Someone left!"

    def exposed_setCallback(self,showMe):
        c.setCallback(showMe)

    def exposed_say(self, shareFolder):
        c.say(shareFolder)

    def exposed_addUser(self, name, fileNames, fileBins):
        c.addUser(name, fileNames, fileBins)

    def exposed_sendFile(self, userID, docID):
        return c.sendFile(userID, docID)

    def exposed_showFiles(self):
        return c.showFiles()

''' A chat server class
  This stores a single state for all the clients
  in the self.callbacks private variable
'''
class FileshareServer:
    def __init__(self):
        self.callbacks  = []
        self.users      = []

    # Append the function call (remote) to the list of clients
    def setCallback(self, showMe):
        self.callbacks = self.callbacks + [showMe]

    # Send that message to everyone's showMe method
    def say(self, shareFolder):
        for fn in self.callbacks:
            try:  # Put in a try/except block just in case we lost net connection
                fn(shareFolder)
            except:
                pass

    def addUser(self, name, fileNames, fileBins):
        user = UserFileShare(name)
        user.setSharedFiles(fileNames, fileBins)
        self.users.append(user)

    def sendFile(self, userID, docID):
        print(userID, docID)
        dindex = 0
        uIndex = 0
        print(1)
        for user in self.users:
            dindex = 0
            print(2)
            print(type(uIndex), type(userID))
            if uIndex == int(userID):
                print(3)
                for file in user.getFileNames():
                    if dindex == int(docID):
                        print(4)
                        rtrn = []
                        rtrn.append(user.getFileNames()[dindex])
                        rtrn.append(user.getFileBin(dindex))
                        print (type(rtrn[0]), type(rtrn[1]))
                        return rtrn
                    else:
                        dindex += 1
            else:
                uIndex += 1

    def showFiles(self):
        ucount = 0
        rtrn = "User and Files\n"
        for user in self.users:
            fcount = 0
            name = user.getName()
            rtrn += str(ucount) + ": " + name + "\n"
            ucount += 1
            for fileN in user.getFileNames():
                rtrn += "   "
                rtrn += str(fcount) + ":" + fileN + "\n"
                fcount += 1
        if ucount == 0:
            return "No users present"
        else:
            print rtrn
            return rtrn


class UserFileShare:
    def __init__(self, name):
        print name
        self.name       = name
        self.fileNames  = []
        self.fileBins   = []
        print "User " + name + "'s files have been added."

    def setSharedFiles(self, fileNames, fileBins):
        self.fileNames  = fileNames
        self.fileBins   = fileBins

    def getName(self):
        return self.name

    def getFileNames(self):
        return self.fileNames

    def getFileBin(self, index):
        return self.fileBins[index]

if __name__ == "__main__":
  from rpyc.utils.server import ThreadedServer
  c = FileshareServer()
  t = ThreadedServer(Service, port = 18861)
  t.start()

