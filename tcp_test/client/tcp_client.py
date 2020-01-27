"""Test application for tcp client."""
import os
import sys
sys.path.append(os.path.abspath(".."))
from tcp_tools import TcpClient

FILE = "resources/clientdata.txt"
FILE = "resources/bird.jpg"
# FILE = 'resources/tb1.pdf'

def get_address():
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = input("Address: ")
    return ip

def tcp_client_test():
    """TCP client function"""
    client = TcpClient(FILE)
    client.printFileInfo()
    client.set_ip(get_address())
    # Create a TCP socket at client side
    client.createTcpSocket()
    client.sendFile()
    client.close()


def tcp_client_simple_test():
    """TCP client function"""
    client = TcpClient(FILE)
    client.set_ip(get_address())
    # Create a TCP socket at client side
    client.createTcpSocket()
    print("sending Hello")
    client.sendData(b"Hello")
    client.close()


if __name__ == "__main__":
    tcp_client_test()
    # tcp_client_simple_test()
