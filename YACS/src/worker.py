import socket
import threading
import time

import sys
import logging
from datetime import datetime

def add_to_pool(isEnd,job_id,task_id,duration):
    poolLock.acquire()
    #print("append acquired")

    pool.append([isEnd,job_id,task_id,duration])

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
                isEnd,job_id,task_id,duration,schedule_algo=data.split(',')
                
                if logFlag[0]:
                	fileName=schedule_algo+'/worker'+worker_id+'.csv'
                	print("HERE: ",fileName) #FIRST COMMUNICATION HAPPENED, WHY NO TICKING DOWN?
                	logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')
                	logFlag[0]=0
                
                now = datetime.now()
                #currTime = now.strftime("%H:%M:%S")
                taskLog[task_id]=now
                
                add_to_pool(isEnd,job_id,task_id,int(duration))
            else:
              # print("Master chan is silent")
                break
        conn.close()

def sendNotif(job_id,task_id):
    print("TASK "+task_id+" DONE")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as toMaster:
        toMaster.connect(("localhost", 5001))
        message=worker_id+','+job_id+','+task_id
        toMaster.send(message.encode()) #send task


def working():
    while True:

        poolLock.acquire()
       # print("working acquired")

        if pool:
            time.sleep(1)

        need_to_pop = list()

        for i in range(len(pool)):
            print(pool,"\n")
            pool[i][3]=pool[i][3]-1
            if pool[i][3]==0:
                
                currTime = datetime.now()
                #currTime = now.strftime("%H:%M:%S")
                
                timeDiff=currTime-taskLog[pool[i][2]]
                taskTime=timeDiff.total_seconds()     
                logging.info('TASK,'+pool[i][2]+','+str(taskTime))
                
                if pool[i][0]=="1":
                	jobTime=currTime.strftime("%H:%M:%S")
                	logging.info('JOB,'+pool[i][1]+','+jobTime)
                
                
                sendNotif(pool[i][1],pool[i][2])
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
    
    logFlag=[1]  #NEED TO MAYBE CHANGE IMPLEMENTATION OF THIS LATER
    #fileName='worker'+worker_id+'.csv'
    #logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')
    taskLog={}

    poolLock=threading.Lock()

    pool=[]

    masterListen = threading.Thread(target=listen_to_master,args=((messages_addr),))
    masterListen.start()

    doTask= threading.Thread(target=working)
    doTask.start()

    
    
