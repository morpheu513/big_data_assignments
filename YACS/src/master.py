import socket
import threading
import sys, json
import queue
import random
import time
import logging
from datetime import datetime


def addToDict_and_queue(job_id,map_tasks,reduce_tasks):

    jobDict[job_id]=[[],[],0]
    
    for i in map_tasks:
        jobDict[job_id][0].append(i['task_id'])
        mapQ.put((job_id,i['task_id'],i['duration']))

    for j in reduce_tasks:
        jobDict[job_id][1].append(j['task_id'])
        jobDict[job_id][2]+=1
        redQ.put((job_id,j['task_id'],j['duration']))


def listen_incoming_jobs(receive_jobs_addr):
    
    jobs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    jobs_sock.bind(receive_jobs_addr)
    jobs_sock.listen(5)

    while True:
        print("Listening to jobs....")
        conn, client_address = jobs_sock.accept()
        
        while True:

            data = conn.recv(2048)
            if data:
                data = data.decode('utf-8')
                data = json.loads(data) 
                
                job_id = data["job_id"]
                print("GOT JOB WITH ID: ", job_id)
                
                now = datetime.now()
                currTime = now.strftime("%H:%M:%S")
                logging.info('JOB,'+job_id+','+currTime)
                
                map_tasks = data["map_tasks"]
                reduce_tasks = data["reduce_tasks"]

                addToDict_and_queue(job_id,map_tasks,reduce_tasks)
                
            else:
                break

        conn.close()


def remDict(job_id,task_id):

    if 'M' in task_id:
        jobDict[job_id][0].remove(task_id)
    
    else:
        jobDict[job_id][1].remove(task_id)
        
        if jobDict[job_id][1]==[]:
            print("Job with ID: ", job_id," COMPLETED\n")


def updateSlots(worker_id):

    workers_array[int(worker_id)-1][1]+=1


def listen_worker_updates(worker_updates_addr):
    
    updates_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    updates_sock.bind(worker_updates_addr)
    updates_sock.listen(5)

    while True:
        
        print("Listening to Updates from workers....")
        conn, worker_address = updates_sock.accept()
        
        while True:
            
            data = conn.recv(2048)
            if data:
                
                data=data.decode('utf-8')
                worker_id,job_id,task_id=data.split(',')
                print("WORKER ",worker_id,"CAME BACK")
                remDict(job_id,task_id)
                updateSlots(worker_id)

            else:
                break
            
        conn.close()


def sendTask(task,worker):
    
    isEnd="0"
    
    if jobDict[task[0]][2]==0:
    	isEnd="1"
    	
    now = datetime.now()
    currTime = now.strftime("%H:%M:%S")
    logging.info('WORKER,'+str(worker[0])+','+currTime)
                
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as toWorker:
        toWorker.connect(("localhost", worker[2]))
        message=isEnd+','+str(task[0])+','+str(task[1])+','+str(task[2])+','+schedule_algo 
        toWorker.send(message.encode())


def round_robin(item):
    done=False
    
    while not done:
        rr_choice[0]=(rr_choice[0]+1)%len(workers_array)

        if workers_array[rr_choice[0]][1]!=0:
            
            workers_array[rr_choice[0]][1]-=1
            sendTask(item,workers_array[rr_choice[0]])
            done=True


def least_loaded(item):
    
    done=False
    
    while not done:

        maxWorker=0

        for i in range(1,len(workers_array)):
            
            if workers_array[maxWorker][1]<workers_array[i][1]:
                maxWorker=i
        
        if workers_array[i]==0:
            time.sleep(1)
        
        else:
            workers_array[maxWorker][1] -= 1
            sendTask(item,workers_array[maxWorker])
            done=True
       

def random_sched(item):
    
    done=False
    
    while not done:
        choice=random.randrange(0,len(workers_array))

        if workers_array[choice][1]!=0:
            
            workers_array[choice][1]-=1
            sendTask(item,workers_array[choice])
            done=True


def scheduleItem(item):
    
    if schedule_algo=="RANDOM":
        random_sched(item)
    
    elif schedule_algo=="RR":
        round_robin(item)
    
    elif schedule_algo=="LL":
        least_loaded(item)
    
    else:
        print("Unexpected scheduling algo, program will not work")


def slots_available():
    for i in range(len(workers_array)):
        
        if workers_array[i][1]!=0:  #CHeck here once
            return True
    
    return False

def scheduleTasks():
    
    while True:
        
        if slots_available():
            
            flag=1
            item=-1

            if not redQ.empty():
                
                amogha=redQ.queue[0]
                if jobDict[amogha[0]][0] == []:
                    
                    flag=0
                    item=redQ.get()
                    jobDict[item[0]][2]-=1
            
            if flag==1 and not mapQ.empty():
                item=mapQ.get()
            
            if item!=-1:
                scheduleItem(item)
        
        else:
            #print("slots are filled go die")
            pass 

        
if __name__ == '__main__':
    

    path_to_config  = sys.argv[1]
    schedule_algo = sys.argv[2]

    config_file = open(path_to_config)
    config = json.load(config_file)
    
    fileName='../data/'+schedule_algo+'/master'+schedule_algo+'.csv'
    logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')
    logging.info('Type,ID,Time')
    workers_array = list()

    jobDict={}
    
    mapQ=queue.Queue()
    redQ=queue.Queue()

    for i in config["workers"]:
        temp = list()
        temp.append(i["worker_id"])
        temp.append(i["slots"])
        temp.append(i["port"])
        workers_array.append(temp)

    receive_jobs_addr = ('localhost', 5000)
    worker_updates_addr = ('localhost', 5001)

    rr_choice=[-1]

    incJob = threading.Thread(target=listen_incoming_jobs,args=((receive_jobs_addr),))
    incJob.start()

    incWork = threading.Thread(target=listen_worker_updates,args=((worker_updates_addr),))
    incWork.start()

    scheduler=threading.Thread(target=scheduleTasks)
    scheduler.start()
