#!/bin/sh
CONVERGE=1
rm v* log*

$HADOOP_HOME/bin/hadoop dfsadmin -safemode leave
hdfs dfs -rm -r /output* 

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
-mapper "/home/morpheus/big_d/task_1/mapper.py" \
-reducer "/home/morpheus/big_d/task_1/reducer.py '/home/morpheus/big_d/task_1/v'"  \
-input /dataset-A2 \
-output /output1 #has adjacency list


while [ "$CONVERGE" -ne 0 ]
do
	$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
	-mapper "/home/morpheus/big_d/task_1/mapper2.py '/home/morpheus/big_d/task_1/v' " \
	-reducer "/home/morpheus/big_d/task_1/reducer2.py" \
	-input /output1 \
	-output /output2
	touch v1
	chmod 777 v1
	hadoop fs -cat /output2/* > /home/morpheus/v1
	CONVERGE=$(python3 /home/morpheus/big_d/task_1/check_conv.py >&1)
	hdfs dfs -rm -r /output2
	echo $CONVERGE

done
