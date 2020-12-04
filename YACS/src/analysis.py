import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

n_machines = int(sys.argv[1])

for algo in ['RR','LL','RANDOM']:
    scheduling_algo = algo

    master_path = '../data/'+scheduling_algo+'/master'+scheduling_algo+'.csv'
    main_worker_path = '../data/'+scheduling_algo+'/worker'
    workers = list()
    for i in range(n_machines):
        workers.append(pd.read_csv(main_worker_path+str(i+1)+'.csv'))
    

    #reading files
    df_master_initial = pd.read_csv(master_path)


    #calculating mean/median task and job completion times
    df_master = df_master_initial.loc[df_master_initial['Type'] == 'JOB']
    df_worker = pd.concat(workers)
    #df_worker = pd.concat([df_w1,df_w2,df_w3])

    mean_task = df_worker.loc[df_worker['Type'] == 'TASK']['Time'].astype(float).mean()
    median_task = df_worker.loc[df_worker['Type'] == 'TASK']['Time'].astype(float).median()

    df_master['ID']=df_master['ID'].astype(int)
    df_master = df_master.set_index('ID')
    df_master = df_master.sort_index()
    df_master['Time'] = pd.to_datetime(df_master['Time'])

    #df_worker = pd.concat([df_w1,df_w2,df_w3])
    df_worker = pd.concat(workers)
    df_worker = df_worker.loc[df_worker['Type'] == 'JOB']
    df_worker['ID']=df_worker['ID'].astype(int)
    df_worker = df_worker.set_index('ID')
    df_worker = df_worker.sort_index()
    df_worker['Time'] = pd.to_datetime(df_worker['Time'])

    exec_times = np.ndarray(shape=(len(df_master.index),1))
    for i in range(len(df_worker.index)):
        tot_exec_time = 0
        #print(df_worker['Time'].iloc[i]," : ",df_master['Time'].iloc[i])
        if df_worker['Time'].iloc[i]>df_master['Time'].iloc[i]:
        	exec_time = df_worker['Time'].iloc[i] - df_master['Time'].iloc[i]
        else:
        	exec_time = df_master['Time'].iloc[i] - df_worker['Time'].iloc[i]
        try:
            minutes = time_exec.minutes
        except:
            minutes = 0
    
        
        tot_exec_time =int(exec_time.seconds)
        #print(tot_exec_time)
        exec_times[i] = tot_exec_time   
    print("FOR:",algo)
    print("Mean task completion time: ",mean_task)
    print("Median task completion time: ",median_task)
    print("Mean job completion time: ",exec_times.mean())
    print("Median job completion time: ", np.median(exec_times))
    print("\n")


    #plotting graphs
    df_master = df_master_initial.loc[df_master_initial['Type'] == 'WORKER'] 
    t_d = dict()
    for i in np.unique(df_master['Time'].values):
        df_temp = df_master.loc[df_master['Time']==i]
        temp = df_temp['ID'].value_counts().index
        templist = [0] * n_machines
        for j in temp:
            templist[j-1] = df_temp['ID'].value_counts().loc[j]
        t_d[str(i)] = templist

    #colors=["#0000FF", "#00FF00", "#FF0066"]
    colors = plt.cm.get_cmap('tab20',n_machines)

    plt.figure(figsize=(15,8))
    #fig, ax = plt.subplots()
    for d_keys , d_vals in zip(t_d.keys(), t_d.values()):
        for i in range(n_machines):
            plt.scatter(d_keys , d_vals[i], color = colors(i), s=800)


plt.show()
