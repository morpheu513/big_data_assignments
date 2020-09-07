#v2 is ready bichhesss
#im sending test ndjson for easier use or else death with that many values
import pandas as pd
import datetime
var='airplane'
myBoy=pd.read_json('test.ndjson', lines=True)
cond1=myBoy[myBoy['word'] == var]
cond2=cond1[cond1['recognized']==True] 
for i in range(len(cond2.index)):
    print(var+":1") #change this to stdout later
#have fun reducing bbz


print("OUTPUT GAP BETWEEN BOTH THE MAPPERS") #self explanatory chingchong

#chennaiaiaiaiaiaia chennai express
#same myBoy dataframe
var='airplane'
myGirl=pd.read_json('test.ndjson', lines=True)
cond1=myGirl[myGirl['word'] == var]
cond2=cond1[cond1['recognized']==False] #False here
reqColumn=list(cond2['timestamp'])
for newbaby in reqColumn:
    newbaby=str(newbaby)
    year=int(newbaby[0:4])
    month=int(newbaby[5:7])
    day=int(newbaby[8:10])
    currDate=datetime.datetime(year, month, day)
    dayNo=currDate.weekday()

    if dayNo>4:
        print(var+":1") #change this to stdout later


#reducer for this also jai