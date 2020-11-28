import socket

import sys

port  = int(sys.argv[1])
worker_id = sys.argv[2]

messages_addr = ('localhost', port)

master_message_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

master_message_sock.bind(messages_addr)