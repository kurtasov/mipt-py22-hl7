import socketserver
from socket import SOL_SOCKET, SO_REUSEPORT

class HL7Message:
	def __init__(self, msg=''):
		self.msg = msg
		self.segments = {}

	def parse(self):
		self.segments = dict(zip([segment.split('|')[0] for segment in self.msg], [segment.split('|')[1:] for segment in self.msg]))
		self.segments['MSH'].insert(0, '|')

		for key in self.segments:
			self.segments[key].insert(0, None)

		return self.segments

class MLLPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(4096)
            if not self.data:
                break
            if self.data.decode('utf-8')[0:1] == '\x0b':
                hl7_message = HL7Message()
                hl7_message.msg = self.data.decode('utf-8')
            if self.data.decode('utf-8')[0:5] == '\x1c\r':
                hl7_message.msg = hl7_message.msg.splitlines()[1:]
                print(f"Получено сообщение от {self.client_address[0]}: {hl7_message.msg}")
                s = hl7_message.parse()
                # print(s)
                print(s['PV1'][7])


class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
 daemon_threads = True
 allow_reuse_address = True


if __name__ == "__main__":
 HOST, PORT = "localhost", 5001
 with MyServer((HOST, PORT), MLLPHandler) as server:
   server.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, True)
   server.serve_forever()
