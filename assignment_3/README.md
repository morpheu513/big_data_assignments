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
Add these lines into the bashrc file:
```
# Spark Variables
export SPARK_HOME=/usr/local/spark #change this location to where you have extracted spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
Save this file and type ``` source ~/.bashrc```
<br>
Add this line into your ```$SPARK_HOME/bin/load-spark-env.sh``` file:
```
export SPARK_LOCAL_IP="127.0.0.1"
```
To check if its installed properly. Type ```start-all.sh``` to start all hadoop daemons.
Then type this line to start Spark with YARN:
```
spark-shell --master yarn 
```
You should obtain an output similar to this:

```
Spark context Web UI available at http://localhost:4040
Spark context available as 'sc' (master = yarn, app id = application_1597405003831_0005).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.0.0
      /_/
         
Using Scala version 2.12.10 (OpenJDK 64-Bit Server VM, Java 1.8.0_252)
Type in expressions to have them evaluated.
Type :help for more information.
```
## Hands on Session:
The hands on session with Spark can be found [here](https://vimeo.com/459272013/f8197d7732)
<br>
The source code used in this video can be downloaded from [here](https://drive.google.com/file/d/1dSqOgDfDjCzGPkBfW8nN5krfInGC_PvV/view)
<br> 
The dataset used for this hands on session can be found [here](https://drive.google.com/file/d/1Ei6JZ7SF5ze00xsKPU9EHKGzxR3c3uCm/view)
