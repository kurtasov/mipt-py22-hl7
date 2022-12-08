import socketserver
from socket import SOL_SOCKET, SO_REUSEPORT

class HL7Message:
    def __init__(self, msg):
        self.msg = msg.decode('utf-8').splitlines()[1:]
        self.segments = {}

    def parse(self):
        self.segments = dict(zip([seg.split('|')[0] for seg in self.msg], [seg.split('|')[1:] for seg in self.msg]))
        return self.segments

class MLLPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096)
        while True:
            self.data += self.request.recv(4096)
            if not self.data:
                break
            print(f"Получено сообщение от {self.client_address[0]}: {self.data}")

            hl7msg = HL7Message(self.data)






class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
 daemon_threads = True
 allow_reuse_address = True


if __name__ == "__main__":
 HOST, PORT = "localhost", 5001
 with MyServer((HOST, PORT), MLLPHandler) as server:
   server.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, True)
   server.serve_forever()
