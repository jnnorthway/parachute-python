"""Test application for tcp server."""
import os
import sys
sys.path.append(os.path.abspath(".."))
from tcp_tools import TcpServer


def tcp_server_test():
    """TCP server test function"""
    server = TcpServer()
    # Create a TCP socket at client side
    server.createTcpSocket()
    server.receiveFile()
    server.close()


def tcp_server_simple_test():
    """TCP server test function"""
    server = TcpServer()
    # Create a TCP socket at client side
    server.createUpdSocket()
    server.TCPSocket.bind(server.server_data["address"])
    print("Server bound on: %s:%s" % server.server_data["address"])
    while True:
        data = server.recieveData()[0]
        if data == server.EOF_MSG:
            break
        print("received: %s" % server.decode(data))
    server.close()


if __name__ == "__main__":
    tcp_server_test()
    # tcp_server_simple_test()
