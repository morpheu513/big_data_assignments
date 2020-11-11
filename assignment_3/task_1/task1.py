from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import sys


w=sys.argv[1]
path1=sys.argv[2]
path2=sys.argv[3]


spark = SparkSession\
        .builder\
        .appName("task1")\
        .getOrCreate()

df = spark.read.csv(path2,header='true')

rec = df.filter((df['word']==w) & (df['recognized']=='True') ).groupBy('word').agg({"Total_Strokes":"avg"}).collect()
unrec = df.filter((df['word']==w) & (df['recognized']=='False')).groupBy('word').agg({"Total_Strokes":"avg"}).collect()

if rec:
        for i,j in rec:
	        print(round(j,5));
else:
        print("0.00000")

if unrec:
        for i,j in unrec:
	        print(round(j,5));
else:
        print("0.00000")




