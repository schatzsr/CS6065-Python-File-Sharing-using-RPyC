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

  def exposed_say(self, message):
    c.say(message)

''' A chat server class
  This stores a single state for all the clients
  in the self.callbacks private variable
'''
class ChatServer:
  def __init__(self):
    self.callbacks = []

  # Append the function call (remote) to the list of clients
  def setCallback(self, showMe):
    self.callbacks = self.callbacks + [showMe]

  # Send that message to everyone's showMe method
  def say(self, message):
    for fn in self.callbacks:
      try:  # Put in a try/except block just in case we lost net connection
        fn(message)
      except:
        pass

if __name__ == "__main__":
  from rpyc.utils.server import ThreadedServer
  c = ChatServer()
  t = ThreadedServer(Service, port = 18861)
  t.start()

