import SocketServer, PBpinguino

a = PBpinguino.TAPinguino()
a.pin_mode(10, "output")

class MyTCPHandler(SocketServer.BaseRequestHandler):
   """
   The RequestHandler class for our server.

   It is instantiated once per connection to the server, and must
   override the handle() method to implement communication to the
   client.
   """

   def handle(self):
      # self.request is the TCP socket connected to the client
      self.data = self.request.recv(1024).strip()
      #print "{} wrote:".format(self.client_address[0])
      #print self.data
      # just send back the same data, but upper-cased
      #self.request.sendall(self.data.upper())
      if self.data == "1":
         a.digital_write(10, "high")
      else:
         a.digital_write(10, "low")

if __name__ == "__main__":
   HOST, PORT = "localhost", 55555

   # Create the server, binding to localhost on port 9999
   server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

   # Activate the server; this will keep running until you
   # interrupt the program with Ctrl-C
   server.serve_forever()
