"""Test application for tcp client."""
from tcp_tools import TcpClient

FILE = "resources/clientdata.txt"
FILE = "resources/bird.jpg"
# FILE = 'resources/tb1.pdf'


def tcp_client_test():
    """TCP client function"""
    client = TcpClient(FILE)
    client.printFileInfo()
    # Create a TCP socket at client side
    client.createTcpSocket()
    client.sendFile()
    client.close()


def tcp_client_simple_test():
    """TCP client function"""
    client = TcpClient(FILE)
    # Create a TCP socket at client side
    client.createTcpSocket()
    print("sending Hello")
    client.sendData(b"Hello")
    client.close()


if __name__ == "__main__":
    tcp_client_test()
    # tcp_client_simple_test()