#!/bin/sh
CONVERGE=1
rm v* log*

$HADOOP_HOME/bin/hadoop dfsadmin -safemode leave
hdfs dfs -rm -r /output* 

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
-mapper "/home/morpheus/big_data_assignments/assignment_2/task_1/mapper.py" \  #change the path
-reducer "/home/morpheus/big_data_assignments/assignment_2/task_1/reducer.py '/home/morpheus//home/morpheus/big_data_assignments/assignment_2/v'"  \  #change the path
-input /web-Google.txt \
-output /output1 #has adjacency list

COUNT=1

while [ "$CONVERGE" -ne 0 ]
do
	echo "Count: $COUNT"
	$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
	-mapper "/home/morpheus/big_data_assignments/assignment_2/task_2/mapper.py '/home/morpheus/big_data_assignments/assignment_2/v' " \  #change the path
	-reducer "/home/morpheus/big_data_assignments/assignment_2/task_2/reducer.py" \  #change the path
	-input /output1 \
	-output /output2
	touch v1
	chmod 777 v1
	hadoop fs -cat /output2/* > /home/morpheus/big_data_assignments/assignment_2/v1 #change the path
	CONVERGE=$(python3 /home/morpheus/big_data_assignments/assignment_2/check_conv.py >&1)  #change the path
	hdfs dfs -rm -r /output2
	echo $CONVERGE
	let COUNT++

done
