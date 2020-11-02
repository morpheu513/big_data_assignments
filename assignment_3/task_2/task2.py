from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import sys


w=sys.argv[1]
k=sys.argv[2]
path1=sys.argv[3]
path2=sys.argv[4]


spark = SparkSession\
        .builder\
        .appName("task2")\
        .getOrCreate()

df1 = spark.read.csv(path1,header='true')
df2 = spark.read.csv(path2,header='true')



both = df1.join(df2,['key_id','word'])


req = both.filter((both['word']==w) & (both['recognized']=='False') & (both['Total_Strokes']<int(k))).groupBy('countrycode').count().orderBy('countrycode').collect()

for row in req:
	print(row['countrycode']+','+str(row['count']))










