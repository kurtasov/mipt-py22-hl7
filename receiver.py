import socketserver
from socket import SOL_SOCKET, SO_REUSEPORT
import datetime

class Patient:
    def __init__(self, hl7data):
        self.name = hl7data['PID'][5]
        self.date_of_birth = datetime.datetime.strptime(hl7data['PID'][7], '%Y%m%d')

    def get_age(self):
        age = datetime.datetime.now() - self.date_of_birth
        return int(age.days/365)


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

    def generate_ack(self):  # TODO: генерировать сообщение с текущей датой и ссылкой на принятое сообщение
        return f'\x0bMSH|^~\\&|Main_HIS|XYZ_HOSPITAL|iFW|ABC_Lab|20160915003015||ACK|9B38584D|P|2.6.1|\rMSA|AA|9B38584D|Everything was okay dokay!|\r\x1c\r'


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

                try:
                    hl7_data = hl7_message.parse()
                except:  # TODO: Реализовать обработку ошибок
                    print("Ошибка парсинга сообщения")
                else:
                    self.request.sendall(hl7_message.generate_ack().encode('utf-8'))
                    pt = Patient(hl7_data)
                    print(f'Поступил пациент {pt.name} возрастом {pt.get_age()} лет')



class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
 daemon_threads = True
 allow_reuse_address = True


if __name__ == "__main__":
 HOST, PORT = "localhost", 5001
 with MyServer((HOST, PORT), MLLPHandler) as server:
   server.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, True)
   server.serve_forever()
