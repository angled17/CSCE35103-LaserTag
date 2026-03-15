import threading
import socket


class UDPServerThread(threading.Thread):
    def __init__(self, socket, queue):
        super().__init__(daemon=True)
        self.socket = socket
        self.queue = queue
        self.running = True

        # Socket Values
        self.buffer_size = 1024

        
    def run(self):
        while self.running:
            try:
                bytesAddressPair = self.socket.recvfrom(self.buffer_size)
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]
                
                self.queue.put((message.decode(), address))

                self.socket.sendto("Message Recieved".encode(), address)
            except socket.error:
                pass

    def stop(self):
        self.running = False
        self.socket.close()