import socket

import sys

if __name__ == '__main__'

    port  = int(sys.argv[1])
    worker_id = sys.argv[2]

    messages_addr = ('localhost', port)

    task_launch_message = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    task_launch_message.bind(messages_addr)

    