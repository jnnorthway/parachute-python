import os
import socket
import sys
import time


class tcp_tools:
    def __init__(self):
        self.ACK_MSG = b"<ACK>"
        self.EOF_MSG = b"<EOF>"
        self.timeout = 3.0
        self.max_attempts = 3
        self.encoding = "utf-8"
        self.server_data = {
            # "address": ("192.168.56.1", 20001),
            # "address": ("127.0.0.1", 20001),
            "address": ("10.0.0.3", 20001),
            # "buffer": 8192
            "buffer": 1024,
        }
        self.TCPSocket = None
        self.connection = None
        self.file = None
        self.file_name = None
        self.file_size = 0
        self.msg_sent = 0
        self.msg_received = 0
        self.progress = 0

    def printProgress(self):
        progress_str = "\rProgress: [%s] %s"
        columns = int(os.popen("stty size", "r").read().split()[1])
        columns -= len(progress_str)
        size_received = self.progress * self.server_data["buffer"]
        percentage = min(1, size_received / self.file_size)
        percent_buffer = ""
        for i in range(columns):
            if (percentage * columns) >= i:
                percent_buffer += "#"
            else:
                percent_buffer += " "
        format_percent = f"{percentage:.0%}"
        sys.stdout.write(progress_str % (percent_buffer, format_percent))

    def clearProgress(self):
        columns = int(os.popen("stty size", "r").read().split()[1])
        buffer = "\r"
        for _ in range(columns):
            buffer += " "
        buffer += "\r"
        sys.stdout.write(buffer)

    def createTcpSocket(self):
        if self.TCPSocket is None:
            print("Creating socket.")
            self.TCPSocket = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM,
            )

    def printFileInfo(self):
        self.fileInfo(self.file)
        print("file path: %s" % self.file)
        print("file size: %d bytes" % self.file_size)

    def fileInfo(self, file_path):
        self.file = file_path
        self.fileName()
        if self.file_size == 0:
            self.file_stats = os.stat(self.file)
            self.file_size = self.file_stats.st_size

    def fileName(self):
        self.file_name = os.path.split(self.file)[1]

    def decode(self, data):
        return data.decode(self.encoding)


class tcp_client(tcp_tools):
    def __init__(self, file_path):
        super().__init__()
        self.fileInfo(file_path)

    def recieveData(self):
        assert self.TCPSocket, "No socket available."
        try:
            data = self.TCPSocket.recv(self.server_data["buffer"])
        except Exception:
            return None
        self.msg_received += 1
        return data

    def sendData(self, data):
        assert self.TCPSocket, "No socket available."
        if isinstance(data, int):
            data = str(data)
        if isinstance(data, str):
            data = str.encode(data)
        assert isinstance(data, bytes), "data not in byte form."
        self.TCPSocket.send(data)
        self.msg_sent += 1
        self.progress += 1

    def sendFile(self):
        start_time = time.time()
        self.createTcpSocket()
        self.TCPSocket.connect(self.server_data["address"])
        print("sending file: %s" % self.file)
        self.sendData(self.file_name)
        self.recieveData()
        self.sendData(self.file_size)
        self.recieveData()
        f = open(self.file, "rb")
        data = f.read(self.server_data["buffer"])
        while data:
            # Send to server using created TCP connection
            self.sendData(data)
            self.printProgress()

            data = f.read(self.server_data["buffer"])
        f.close()
        self.sendData(self.EOF_MSG)
        print("\nFile sent.")
        print("Send time: %f" % (time.time() - start_time))

    def close(self):
        self.TCPSocket.close()


class tcp_server(tcp_tools):
    def __init__(self):
        self.resource_path = "resources"
        super().__init__()

    def recieveData(self):
        assert self.connection, "No socket available."
        try:
            data = self.connection.recv(self.server_data["buffer"])
        except Exception:
            return None
        self.msg_received += 1
        self.progress += 1
        return data

    def sendData(self, data):
        assert self.connection, "No socket available."
        if isinstance(data, str):
            data = str.encode(data)
        assert isinstance(data, bytes), "data not in byte form."
        self.connection.send(data)
        self.msg_sent += 1

    def receiveFile(self):
        # Listen for incoming datagrams
        message = None
        data = b""
        self.TCPSocket.bind(self.server_data["address"])
        self.TCPSocket.listen(1)
        print("Server listening on: %s:%s" % self.server_data["address"])
        self.connection = self.TCPSocket.accept()[0]
        while True:
            message = self.recieveData()
            if self.file is None:
                self.file = os.path.join(self.resource_path, self.decode(message))
                start_time = time.time()
                self.sendData(self.ACK_MSG)
                print("receiving file: %s" % self.file)
            elif self.file_size == 0:
                self.file_size = int(self.decode(message))
                self.sendData(self.ACK_MSG)
                self.printFileInfo()
            else:
                data += message
                self.printProgress()
                if len(data) >= self.file_size:
                    break
        f = open(self.file, "wb")
        f.write(data)
        print("\nFile written: %s" % self.file)
        f.close()
        print("Receive time: %f" % (time.time() - start_time))
        self.file_name = None

    def close(self):
        self.connection.close()
        self.TCPSocket.close()
