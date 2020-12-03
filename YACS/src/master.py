import socket
import threading
import sys, json
import queue
import random
import time
import logging
from datetime import datetime

'''
Once a job has been recieved by master it adds maps tasks to map queue, reduce tasks to reduce queue and adds all the
dependencies to the dictionary(jobDict)
'''
def addToDict_and_queue(job_id,map_tasks,reduce_tasks):

    jobDict[job_id]=[[],[],0]
    
    for i in map_tasks:
        jobDict[job_id][0].append(i['task_id'])
        mapQ.put((job_id,i['task_id'],i['duration']))

    for j in reduce_tasks:
        jobDict[job_id][1].append(j['task_id'])
        jobDict[job_id][2]+=1
        redQ.put((job_id,j['task_id'],j['duration']))

'''
This listens to incoming jobs from requests.py, using sockets. Socket is created and it accepts a json file
This json file is then decoded and extracted values are added to the queues and dictionary using addToDict_and_queue()
Job arrival time is also logged here.
'''
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
                
                #logging the job arrival time
                now = datetime.now()
                currTime = now.strftime("%H:%M:%S")
                logging.info('JOB,'+job_id+','+currTime)
                
                map_tasks = data["map_tasks"]
                reduce_tasks = data["reduce_tasks"]
                #adding received values to the queues and dictionary
                addToDict_and_queue(job_id,map_tasks,reduce_tasks)
                
            else:
                break

        conn.close()

'''
Once a task comes back, dependencies are updated by removing its value from the dict with job_id as key
If values are empty for a job_id, the job is completed
'''
def remDict(job_id,task_id):

    if 'M' in task_id:
        jobDict[job_id][0].remove(task_id)
    
    else:
        jobDict[job_id][1].remove(task_id)
        
        if jobDict[job_id][1]==[]:
            print("Job with ID: ", job_id," COMPLETED\n")

#Adds a slot back to worker when worker sends back task completion message
def updateSlots(worker_id):

    workers_array[int(worker_id)-1][1]+=1

'''
This listens to updates from workers, using socket programming it listens on a port(5001)
Whenever worker sends task completion message, slots are added back to it and dependencies are updated in dictionary (jobDict)
'''
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
                #update dependencies
                remDict(job_id,task_id)
                #update worker slots(add worker slot back)
                updateSlots(worker_id)

            else:
                break
            
        conn.close()

'''
Sends task to the specified worker with the task id, job id and duration  -->using socket programming
'''
def sendTask(task,worker):
    
    #flag to check whether it is the last task of a job so that worker can log job completion time
    isEnd="0"
    
    if jobDict[task[0]][2]==0:
    	isEnd="1"
    	
    now = datetime.now()
    currTime = now.strftime("%H:%M:%S")
    logging.info('WORKER,'+str(worker[0])+','+currTime)
                
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as toWorker:
        toWorker.connect(("localhost", worker[2]))
        #scheduling algorithm is also sent so worker knows where to dump the log files
        message=isEnd+','+str(task[0])+','+str(task[1])+','+str(task[2])+','+schedule_algo 
        toWorker.send(message.encode())

'''
round robin scheduler schedules one one task to each worker and keeps cycling. Next worker to assign task to can be calculated by
the formula next_worker_index=(previous_worker_index+1)/number_of_workers
'''
def round_robin(item):
    done=False
    
    while not done:
        rr_choice[0]=(rr_choice[0]+1)%len(workers_array)

        if workers_array[rr_choice[0]][1]!=0:
            
            workers_array[rr_choice[0]][1]-=1
            sendTask(item,workers_array[rr_choice[0]])
            done=True

'''
Least loaded scheduler will check which worker has most free slots and assign task to that worker
'''
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
       
'''
random scheduler randomly selects worker and checks if it has slots. If it has slots then task is assigned to it or else
another worker is randomly selected. This goes on until a free slot is found
'''
def random_sched(item):
    
    done=False
    
    while not done:
        choice=random.randrange(0,len(workers_array))

        if workers_array[choice][1]!=0:
            
            workers_array[choice][1]-=1
            sendTask(item,workers_array[choice])
            done=True

'''
Scheduling algorithm used depends on user input
RANDOM-->random scheduler
RR-->round robin scheduler
LL-->least loaded scheduler
'''
def scheduleItem(item):
    
    if schedule_algo=="RANDOM":
        random_sched(item)
    
    elif schedule_algo=="RR":
        round_robin(item)
    
    elif schedule_algo=="LL":
        least_loaded(item)
    
    else:
        print("Unexpected scheduling algo, program will not work")

'''
This checks if any of the workers has at least one slot free
'''
def slots_available():
    for i in range(len(workers_array)):
        
        if workers_array[i][1]!=0:  #CHeck here once
            return True
    
    return False

'''
This schedules all the tasks to the workers. There are two queues-> ready queue and map queue. We peek at the reduce queue
and check if its dependancies(map tasks) are all complete using jobDict. If they are, then it is dequeued and then sent to worker. If 
there is no reduce task that can be executed, the map queue is dequeued and a map task is sent to the worker instead. This ensures that
workers will always have tasks to do and will not be bottled by waiting for reduce task dependencies to finish.
'''
def scheduleTasks():
    
    while True:
        #checks is sl
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
            #print("slots are filled")
            pass 

        
if __name__ == '__main__':
    

    path_to_config  = sys.argv[1]
    schedule_algo = sys.argv[2]

    config_file = open(path_to_config)
    config = json.load(config_file)
    
    #Initializing the log file
    fileName='../data/'+schedule_algo+'/master'+schedule_algo+'.csv'
    logging.basicConfig(level=logging.INFO,filename=fileName, filemode='w', format='%(message)s')
    logging.info('Type,ID,Time')

    '''
    Dictionary where job id is key value, and it has map tasks, reduce tasks, and number of reduce tasks left to send out
    Everytime a task comes back as completed it is removed from this dict. This dict is used for the reduce tasks to check if corresponding
    map tasks have been completed. It is also used for logging as the last reduce task needs to be logged by worker to calculate
    job completion time
    '''
    jobDict={}
    
    '''
    There are two queues -> the map queue and the reduce queue. These store the map tasks and reduce tasks in their respective queues
    and are dequeued at time of scheduling
    '''
    mapQ=queue.Queue()
    redQ=queue.Queue()

    '''
    This is a 2D array which keeps track of all the workers-> their ids, port numbers and number of slots. They are dynamically
    assigned, it is read from the config file so the slots,port numbers and number of workers itself are all changeable
    '''
    workers_array = list()
    for i in config["workers"]:
        temp = list()
        temp.append(i["worker_id"])
        temp.append(i["slots"])
        temp.append(i["port"])
        workers_array.append(temp)

    #ports to listen to for receiving jobs and listening to workers
    receive_jobs_addr = ('localhost', 5000)
    worker_updates_addr = ('localhost', 5001)

    rr_choice=[-1]
    '''
    There are 3 threads running on the master
    '''

    #thread that listens to incoming jobs
    incJob = threading.Thread(target=listen_incoming_jobs,args=((receive_jobs_addr),))
    incJob.start()

    #thread that listens to updates from workers
    incWork = threading.Thread(target=listen_worker_updates,args=((worker_updates_addr),))
    incWork.start()

    #thread that schedules tasks on workers
    scheduler=threading.Thread(target=scheduleTasks)
    scheduler.start()
