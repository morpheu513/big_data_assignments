import socket
import threading

import sys, json

path_to_config  = sys.argv[1]
schedule_algo = sys.argv[2]

config_file = open(path_to_config)
config = json.load(config_file)

receive_jobs_addr = ('localhost', 5000)
worker_updates_addr = ('localhost', 5001)

def listen_incoming_jobs(receive_jobs_addr):
    jobs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    jobs_sock.bind(receive_jobs_addr)
    jobs_sock.listen()

    while True:
        print("Listening to jobs....")
        conn, client_address = jobs_sock.accept()
        while True:
            data = conn.recv()
            if data:
                pass
            else:
                print("No more incoming jobs..")
                break

        conn.close()


def listen_worker_updates(worker_updates_addr):
    updates_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    updates_sock.bind(worker_updates_addr)
    updates_sock.listen()

    while True:
        print("Listening to Updates from workers....")
        conn, worker_address = updates_sock.accept()
        while True:
            data = conn.recv()
            if data:
                pass
            else:
                print("All workers have finished executing..")
                break

        conn.close()