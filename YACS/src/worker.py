import socket
import threading
import time

import sys

def add_to_pool(worker_id,job_id,task_id,duration):
    poolLock.acquire()
    #print("append acquired")

    pool.append([worker_id,job_id,task_id,duration])

    poolLock.release()
   # print("append released")

def listen_to_master(messages_addr):

    task_launch_message = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    task_launch_message.bind(messages_addr)
    task_launch_message.listen()
    while True:
        #print("Listening to master....")
        conn, master_address = task_launch_message.accept()
        while True:
            data = conn.recv(2048)
            if data:
                data = data.decode('utf-8')
                worker_id,job_id,task_id,duration=data.split(',')
                add_to_pool(worker_id,job_id,task_id,int(duration))
            else:
              # print("Master chan is silent")
                break
        conn.close()

def sendNotif(worker_id,job_id,task_id):
    print("TASK "+task_id+" DONE")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as toMaster:
        toMaster.connect(("localhost", 5001))
        message=worker_id+','+job_id+','+task_id
        toMaster.send(message.encode()) #send task


def working():
    while True:

        poolLock.acquire()
       # print("working acquired")

        time.sleep(1)

        need_to_pop = list()

        for i in range(len(pool)):
            print(pool,"\n")
            pool[i][3]=pool[i][3]-1
            if pool[i][3]==0:
                sendNotif(pool[i][0],pool[i][1],pool[i][2])
                #print("POP: ",pool.pop(i),"\n")
                need_to_pop.append(i)
        
        for i in sorted(need_to_pop,reverse=True):
            pool.pop(i)

        poolLock.release()
       # print("working released")

            



if __name__ == '__main__':

    port  = int(sys.argv[1])
    worker_id = sys.argv[2]
    messages_addr = ('localhost', port)

    poolLock=threading.Lock()

    pool=[]

    masterListen = threading.Thread(target=listen_to_master,args=((messages_addr),))
    masterListen.start()

    doTask= threading.Thread(target=working)
    doTask.start()
    doTask.join()
    
    