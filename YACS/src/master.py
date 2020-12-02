import socket
import threading
import sys, json
import queue
import random
import time
import logging
from datetime import datetime


def addToDict_and_queue(job_id,map_tasks,reduce_tasks):
    dictLock.acquire()
    #print("dictlock released \n")
    #queueLock.acquire()
    #print("Queuelock released \n") 
   # print("Acquired Dict and queue lock")
    jobDict[job_id]=[[],[],0]
    for i in map_tasks:
        jobDict[job_id][0].append(i['task_id'])
        mapQ.put((job_id,i['task_id'],i['duration']))

    #print("MAP : ",mapQ,"\n")

    for j in reduce_tasks:
        jobDict[job_id][1].append(j['task_id'])
        jobDict[job_id][2]+=1
        redQ.put((job_id,j['task_id'],j['duration']))

    #print("REDUCE : ",redQ,"\n")
    #print(mapQ.queue[-1])
    #print(redQ.queue[-1])
    #print("Brahmilamila")
    #queueLock.release()
    #print("#queueLock released \n")
    dictLock.release()
    #print("dictlock released \n")
   # print("Releasing Dict and queue lock")

def listen_incoming_jobs(receive_jobs_addr):
    jobs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    jobs_sock.bind(receive_jobs_addr)
    jobs_sock.listen(5)

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
                print("GOT JOB WITH ID: ", job_id)
                
                now = datetime.now()
                currTime = now.strftime("%H:%M:%S")
                logging.info('JOB,'+job_id+','+currTime)
                
                map_tasks = data["map_tasks"]
                reduce_tasks = data["reduce_tasks"]

                addToDict_and_queue(job_id,map_tasks,reduce_tasks)

                #for i in map_tasks:
                    #pass
                    #print(i)

                #print(data["job_id"])
                
            else:
                #print("No more incoming jobs..")
                break
            #finalAnswer.release()
            #print("Released job lock")

        conn.close()

def remDict(job_id,task_id):
    dictLock.acquire()
    print("acquired dict lock in rem dict")

    if 'M' in task_id:
        jobDict[job_id][0].remove(task_id)
    else:
        jobDict[job_id][1].remove(task_id)
        if jobDict[job_id][1]==[]:
            #print("JOBS ARE ACTUALLY GETTING COMPLETED")
            print("Job with ID: ", job_id," COMPLETED\n")

    dictLock.release()
    print("released dict lock")

def updateSlots(worker_id):
    workLock.acquire()
    print("Work lock acquired in update slots")

    workers_array[int(worker_id)-1][1]+=1   #might have to change logic here

    workLock.release()
    #print("Work lock released")



def listen_worker_updates(worker_updates_addr):
    updates_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    updates_sock.bind(worker_updates_addr)
    updates_sock.listen(5)

    while True:
        print("Listening to Updates from workers....")
        conn, worker_address = updates_sock.accept()
        while True:
            #finalAnswer.acquire()
            #print("Acquired worker lock")
            data = conn.recv(2048)
            if data:
                data=data.decode('utf-8')
                worker_id,job_id,task_id=data.split(',')
                print("WORKER ",worker_id,"CAME BACK")
                remDict(job_id,task_id)
                updateSlots(worker_id)

            else:
              #  print("All workers have finished executing..")
                break
            
            #finalAnswer.release()
            #print("Released worker lock")

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
        message=isEnd+','+str(task[0])+','+str(task[1])+','+str(task[2])+','+schedule_algo  #SENDING SCHEDULING ALGO EVERYTIME
        toWorker.send(message.encode()) #send task to worker


def round_robin(item):
    done=False
    while not done:
        rr_choice[0]=(rr_choice[0]+1)%len(workers_array)

        workLock.acquire()
       # print("Work lock acquired")

        if workers_array[rr_choice[0]][1]!=0:
            workers_array[rr_choice[0]][1]-=1
            
            workLock.release()
           # print("Work lock released")

            sendTask(item,workers_array[rr_choice[0]])
            done=True

def least_loaded(item):
    done=False
    while not done:
        workLock.acquire()
       # print("Work lock acquired")

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

        workLock.release()
       # print("Work lock released")

        

def random_sched(item):
    done=False
    while not done:
        choice=random.randrange(0,len(workers_array))

        workLock.acquire()
        #print("Work lock acquired")

        if workers_array[choice][1]!=0:
            workers_array[choice][1]-=1
            
            workLock.release()
          #  print("Work lock released")

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
            dictLock.acquire() #CHANGED THIS LOCK (ADDED IT BACK)
            flag=1
            item=-1
            #queueLock.acquire()
            #print("queue lock acquired")
            if not redQ.empty():
                amogha=redQ.queue[0]
                if jobDict[amogha[0]][0] == []:#potential dict lock needed here,  need to send some sort of flag indication last reduce task for logging?
                    flag=0
                    item=redQ.get()
                    jobDict[item[0]][2]-=1
                    print("popped reduce queue",item,"\n")
            if flag==1 and not mapQ.empty():
                item=mapQ.get()
            if item!=-1:
                scheduleItem(item)
            dictLock.release()
            #queueLock.release()
            #time.sleep(2) 
        else:
            print("slots are filled go die") 
        #dictLock.release()
            #print("queue lock released")
        
        
        

if __name__ == '__main__':
    

    path_to_config  = sys.argv[1]
    schedule_algo = sys.argv[2]

    config_file = open(path_to_config)
    config = json.load(config_file)
    
    fileName=schedule_algo+'/master'+schedule_algo+'.csv'
    logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')

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

    dictLock=threading.Lock()
    #queueLock=threading.Lock() 
    workLock=threading.Lock()

    incJob = threading.Thread(target=listen_incoming_jobs,args=((receive_jobs_addr),))
    incJob.start()

    incWork = threading.Thread(target=listen_worker_updates,args=((worker_updates_addr),))
    incWork.start()

    scheduler=threading.Thread(target=scheduleTasks)
    scheduler.start()
