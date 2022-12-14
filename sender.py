import socket

with socket.create_connection(('127.0.0.1', 2100)) as s:
    hl7_msg = '\x0b'
    hl7_msg += 'MSH|^~\\&|SENDING_APP|SENDING_FACILITY|RECEIVING_APP|RECEIVING_FACILITY|20110613083617||ADT^A04|12345|P|2.3||||'
    hl7_msg += '\r'
    hl7_msg += 'EVN|A04|20110613083617|||'
    hl7_msg += '\r'
    hl7_msg += 'PID|1||135769||SIMPSON^MARGE^||19580319|M|||743 Evergreen Terrace^^Springfield^OR^49007||(999)999-1111^^^marge@example.com|||||1719|99999999||||||||||||||||||||'
    hl7_msg += '\r'
    hl7_msg += 'PV1|1|O|||||7^HOUSE^GREGORY^^MD^^^^|||||||||||||||||||||||||||||||||||||||||||||'
    hl7_msg += '\r'
    hl7_msg += '\x1c'
    hl7_msg += '\r'
    s.send(hl7_msg.encode('utf-8'))
    answer = s.recv(4096).decode('utf-8')
    print(answer)
