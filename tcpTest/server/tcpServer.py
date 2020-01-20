import os
import sys
import socket
sys.path.append(os.path.abspath(".."))
from tcpTools import tcpServer


def tcpServerTest():
    """TCP server function"""
    server = tcpServer()
    # Create a TCP socket at client side
    server.createTcpSocket()
    server.receiveFile()
    server.close()


def tcpServerSimpleTest():
    """TCP server function"""
    server = tcpServer()
    # Create a TCP socket at client side
    server.createUpdSocket()
    server.TCPSocket.bind(server.server_data['address'])
    print("Server bound on: %s:%s" % server.server_data['address'])
    while(True):
      data = server.recieveData()[0]
      if data == server.EOF_MSG:
        break
      print('received: %s' % server.decode(data))
    server.close()


if __name__== "__main__":
  tcpServerTest()
  # tcpServerSimpleTest()