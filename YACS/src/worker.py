import socket
import threading
import time
import sys
import logging
from datetime import datetime


def add_to_pool(isEnd,job_id,task_id,duration):
    
    poolLock.acquire()

    #adding task details to the pool
    pool.append([isEnd,job_id,task_id,duration])

    poolLock.release()


def listen_to_master(messages_addr):

    #defining the socket on which the worker and master communicate
    task_launch_message = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    task_launch_message.bind(messages_addr)
    task_launch_message.listen()
    
    while True:
        #establish connection with the master
        conn, master_address = task_launch_message.accept()
        
        while True:
            #receiving data from the master
            data = conn.recv(2048)
            
            if data:
                
                data = data.decode('utf-8')
                isEnd,job_id,task_id,duration,schedule_algo=data.split(',')
                
                if logFlag[0]:
                    #initialize logging files and parameters
                    
                    fileName='../data/'+schedule_algo+'/worker'+worker_id+'.csv' 
                    logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')
                    logging.info('Type,ID,Time')
                    logFlag[0]=0
                
                now = datetime.now()

                #storing start time of the task
                taskLog[task_id]=now
                
                #adding the task to the pool
                add_to_pool(isEnd,job_id,task_id,int(duration))

            else:
                #print("Master chan is silent")
                break

        conn.close()


def sendNotif(job_id,task_id):
    
    #sends updates to the master about the job status
    #communication happens over port 5001
    print("TASK "+task_id+" DONE")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as toMaster:
        toMaster.connect(("localhost", 5001))
        message=worker_id+','+job_id+','+task_id
        toMaster.send(message.encode()) 


def working():

    while True:

        #acquire the lock to prevent race conditions
        poolLock.acquire()

        if pool:
            time.sleep(1)

            #stores tasks which have have been completed and need to be removed the pool
            need_to_pop = list()

            for i in range(len(pool)):

                pool[i][3]=pool[i][3]-1
                
                if pool[i][3]==0:
                
                    currTime = datetime.now()
                
                    #calculating the time taken for the completion of the task
                    timeDiff=currTime-taskLog[pool[i][2]]
                    taskTime=timeDiff.total_seconds()

                    #logging the task completion time
                    logging.info('TASK,'+pool[i][2]+','+str(taskTime))
                    
                    if pool[i][0]=="1":

                        #checking if the job has been completed and logging the job completion time
                        jobTime=currTime.strftime("%H:%M:%S")
                        logging.info('JOB,'+pool[i][1]+','+jobTime)
                
                    #sending a message to the master that a particular task has completed
                    sendNotif(pool[i][1],pool[i][2])
                    
                    need_to_pop.append(i)
        
            for i in sorted(need_to_pop,reverse=True):
                pool.pop(i)

        #release lock as updation of shared data structure has finished
        poolLock.release()


if __name__ == '__main__':

    #reading in the port number and id of the worker as system arguments
    port  = int(sys.argv[1])
    worker_id = sys.argv[2]
    
    #Flag variable to check if we need to create the log file
    logFlag=[1]  
    
    #keeps track of start time of task in order to calculate the task run time
    taskLog={}

    pool=[]

    '''
    pool is a list which contains the tasks currently running in the pool.
    Since this is a shared data structure we will need to add a lock when we update its contents
    '''

    poolLock=threading.Lock()

    #defining the port number on which the wroker needs to communicate with the master
    messages_addr = ('localhost', port)

    #defining a thread which is used by the worker to listen to the master
    masterListen = threading.Thread(target=listen_to_master,args=((messages_addr),))
    masterListen.start()

    # defining a thread which performs the working or execution of tasks on the worker
    doTask= threading.Thread(target=working)
    doTask.start()
