import os
import sys

from tcpTools import tcpClient

sys.path.append(os.path.abspath(".."))

FILE = "resources/clientdata.txt"
FILE = "resources/bird.jpg"
# FILE = 'resources/tb1.pdf'


def tcpClientTest():
    """TCP client function"""
    client = tcpClient(FILE)
    client.printFileInfo()
    # Create a TCP socket at client side
    client.createTcpSocket()
    client.sendFile()
    client.close()


def tcpClientSimpleTest():
    """TCP client function"""
    client = tcpClient(FILE)
    # Create a TCP socket at client side
    client.createTcpSocket()
    print("sending Hello")
    client.sendData(b"Hello")
    client.close()


if __name__ == "__main__":
    tcpClientTest()
#   tcpClientSimpleTest()
