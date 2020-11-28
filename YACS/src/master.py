import socket
import threading
import random
import sys, json

def round_robin():
    pass

def random_scheduler():
    pass

def least_loaded():
    pass

def listen_incoming_jobs(receive_jobs_addr):
    jobs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    jobs_sock.bind(receive_jobs_addr)
    jobs_sock.listen()

    while True:
        print("Listening to jobs....")
        conn, client_address = jobs_sock.accept()
        while True:
            #finalAnswer.acquire()
            #print("Acquired job lock")
            data = conn.recv(2048)
            if data:
                data = data.decode('utf-8')
                data = json.loads(data) 

                job_id = data["job_id"]
                map_tasks = data["map_tasks"]
                reduce_tasks = data["reduce_tasks"]

                for i in map_tasks:
                    print(i)

                #print(data["job_id"])
                
            else:
                print("No more incoming jobs..")
                break
            #finalAnswer.release()
            #print("Released job lock")

        conn.close()


def listen_worker_updates(worker_updates_addr):
    updates_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    updates_sock.bind(worker_updates_addr)
    updates_sock.listen()

    while True:
        print("Listening to Updates from workers....")
        conn, worker_address = updates_sock.accept()
        while True:
            #finalAnswer.acquire()
            #print("Acquired worker lock")
            data = conn.recv()
            if data:
                pass
            else:
                print("All workers have finished executing..")
                break
            
            #finalAnswer.release()
            #print("Released worker lock")

        conn.close()

if __name__ == '__main__':
    

    path_to_config  = sys.argv[1]
    schedule_algo = sys.argv[2]

    config_file = open(path_to_config)
    config = json.load(config_file)

    receive_jobs_addr = ('localhost', 5000)
    worker_updates_addr = ('localhost', 5001)

    #finalAnswer=threading.Lock()

    incJob = threading.Thread(target=listen_incoming_jobs,args=((receive_jobs_addr),))
    incJob.start()

    incWork = threading.Thread(target=listen_worker_updates,args=((worker_updates_addr),))
    incWork.start()
