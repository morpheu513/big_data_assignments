# Assignment 1
Chuck code for the first assignment here. 

## Dataset link:
https://drive.google.com/drive/folders/10xfNXqxSpF_aHyhoo8dizGXUAxhOw_Va

Dont bother uploading the Datasets to github because then we would have to use something called git-lfs to handle these large datasets(makes sense cuz its Big Data).

Also Remember 
The lord yeetith and the lord yoinkith away

## Running Hadoop Map-Reduce:
Since get hadoop up and running is a big pain, here are the list of steps youll need to do to get your hadoop map-reduce up and running. 
This is written assuming yo already have hadoop and yarn installed in pesudo distributed mode.

### Step 1: Starting Hadoop
Start hadoop's distributed file system using:
```
start-dfs.sh
```

This should get 4 processes up and running type in ```jps``` to see all running processes you should have:
```
SecondaryNameNode
NameNode
Jps
DataNode
```
After this start the yarn processes by running: 
```
start-yarn.sh
```
Now you should have 6 processes up and running. 
Again you can check all the processes running at any given time by typing
```
jps
```
Once we have started yarn the following processes show up:
```
SecondaryNameNode
NameNode
NodeManager
DataNode
ResourceManager
Jps
```

If either you ```NameNode``` or ```DataNode``` don't show up, you can try formatting them and starting then again. 
Format the ```NameNode``` using:
```
hdfs namenode -format
```
Use this command to stop all processes:
```
stop-all.sh
```

### Step 2: Uploading Input Files to Hadoop
Once we have gotten all the processes up and running you need to run add you input files into hdfs. this can be done in the following way:

Create a directory on hdfs using:
```
hdfs dfs -mkdir /<Dir-Name>
```

To upload a file to hdfs:
```
hdfs dfs -put '<path-to-file-on-host-pc>' /<path-to-directory-on-hdfs>
```

### Step 3: Running Hadoop Map-Reduce

Once we have gotten all the input files uploaded onto hdfs we can run the hadoop's map reduce using the following command(remember this works for python files):
```
hadoop jar '<path-to-hadoop-streaming-file>' \
-mapper '<path-to-mapper-file>' \
-reducer '<path-to-reducer-file>' \
-input <path-to-uploaded-input-files-on-hdfs> \
-output <path-to-output-directory-on-hdfs>
```

For example on my computer the following command is executed as:
```
hadoop jar '/home/morpheus/hadoop/hadoop-3.2.0/share/hadoop/tools/lib/hadoop-streaming-3.2.0.jar' \
-mapper '/home/morpheus/Big_Data_assignments/Week_1/mapper.py' \ 
-reducer '/home/morpheus/Big_Data_assignments/Week_1/reducer.py' \ 
-input /input/plane_carriers.ndjson \
-output /output/task_2
```

### Step 4: Displaying output

To display your output type in:
```
hdfs dfs -cat /<path-to-output-directory-on-hdfs>/part-00000
```
For the previous example the output can by displayed by using:
```
hdfs dfs -cat /output/task_2/part-00000
```
