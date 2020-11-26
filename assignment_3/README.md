# Assignment 3
Chuck code for the third assignment here.

## Spec Sheet:
The link to the specification sheet can be found [here](https://forum.pesu.io/uploads/short-url/potTewXPT3ETwqWvNvwQdHW35WJ.pdf)
<br>
The spec sheet is present on this repository as well so you can just check that out. 

## Dataset link:
The Data set can be downloaded from [here](https://drive.google.com/drive/folders/1gRKrDTdjMHwwaWfesPGw76xHyUZTVIJl)
<br>
Make sure you download both the files.

## Installing Spark:
The demo video made by KVS showing installation can be viewed [here](https://vimeo.com/459271132/18111a409c)

First download the archived file from Apache's [website](https://www.apache.org/dyn/closer.lua/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz)
<br>
Once thats done extract the files into 
```
/usr/local
```
<br>
Add these lines into the bashrc file:
To open the bashrc file using nano type:
```
sudo nano ~/.bashrc
```

Once opened add these lines at the bottom:
```
# Spark Variables
export SPARK_HOME=/usr/local/spark-3.0.0-bin-hadoop3.2
#change the above location to where you have extracted spark 

export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

export PYSPARK_PYTHON=python3
```
Save this file and type ``` source ~/.bashrc```
<br>
Add these line into your ```$SPARK_HOME/bin/load-spark-env.sh``` file:
```
export SPARK_LOCAL_IP="127.0.0.1"
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```

To check if it's installed properly. Start all hadoop daemons by typing:
```
start-all.sh
```

To check if you've set up all variables correctly type the following command:
```
spark-submit --version
```

The obtained output should be similar to this:
```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.0.0
      /_/
                        
Using Scala version 2.12.10, OpenJDK 64-Bit Server VM, 1.8.0_272
Branch HEAD
Compiled by user ubuntu on 2020-06-06T13:05:28Z
Revision 3fdfce3120f307147244e5eaf46d61419a723d50
Url https://gitbox.apache.org/repos/asf/spark.git
Type --help for more information.
```
To enter the spark shell type the following command:
```
spark-shell --master yarn 
```
You should obtain an output similar to this:

```
2020-10-31 23:42:09,482 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
2020-10-31 23:42:16,913 WARN yarn.Client: Neither spark.yarn.jars nor spark.yarn.archive is set, falling back to uploading libraries under SPARK_HOME.
Spark context Web UI available at http://localhost:4040
Spark context available as 'sc' (master = yarn, app id = application_1604167857726_0001).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.0.0
      /_/
         
Using Scala version 2.12.10 (OpenJDK 64-Bit Server VM, Java 1.8.0_272)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 

```
To browse the YARN resource manager and see all running clusters go to your browser and type:
```
http://localhost:8088/cluster
```
## Running Spark Jobs:
To run a spark job follow these steps:
1. First start all of hadoops daemons by typing ```start-all.sh```. 
alternatively you can start hadoops dfs first by typing ```start-dfs.sh``` then followed by ```start-yarn.sh``` to start YARN.
2. You need to upload both the datasets onto hadoop. This can be done my executing the following commands:
```
hdfs dfs -mkdir /<Dir-Name> #use this only if you want to make a directory on hadoop before uploading

hdfs dfs -put '<path-to-file-on-host-pc>' /<path-to-directory-on-hdfs>
```
3. Running the job:
      * Task 1: The spark job can be run by executing the following command(only for task 1):
      ```
      spark-submit <filename.py> <word> hdfs://localhost:9000/<pth-to-dataset-1> hdfs://localhost:9000/<path-to-dataset-2>
      ```
      * Task 2: The spark job can be run by executing the following command(only for task 2):
      ```
      spark-submit <filename.py> <word> <strokes> hdfs://localhost:9000/<path-to-dataset-1> hdfs://localhost:9000/<path-to-dataset-2>
      ```
## Hands on Session:
The hands on session with Spark can be found [here](https://vimeo.com/459272013/f8197d7732)
<br>
The source code used in this video can be downloaded from [here](https://drive.google.com/file/d/1dSqOgDfDjCzGPkBfW8nN5krfInGC_PvV/view)
<br> 
The dataset used for this hands on session can be found [here](https://drive.google.com/file/d/1Ei6JZ7SF5ze00xsKPU9EHKGzxR3c3uCm/view)
