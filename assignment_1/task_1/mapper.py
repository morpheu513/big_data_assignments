import datetime
#mapper, this whole thing in a for loop, current variable for input is var
var='airplane'
baby={"word": "airplane", "countrycode": "US", "timestamp": "2017-03-08 21:12:07.26604 UTC", "recognized": True, "key_id": "5152802093400064", "drawing": [[[167, 109, 80, 69, 58, 31, 57, 117, 99, 52, 30, 6, 1, 2, 66, 98, 253, 254, 246, 182, 165], [140, 194, 227, 232, 229, 229, 206, 124, 123, 149, 157, 159, 153, 110, 82, 77, 74, 109, 121, 127, 120]], [[207, 207, 210, 221, 238], [74, 103, 114, 128, 135]], [[119, 107, 76, 70, 49, 39, 60, 93], [72, 41, 3, 0, 1, 5, 38, 70]]]}
if baby['word']==var:
    if baby['recognized']==True:
        print(var+":1")
#enjoy reducing lmao


#mapper 2, this thing also in a for loop, input is same var
newbaby={"word": "airplane", "countrycode": "US", "timestamp": "2017-03-12 17:02:16.9625 UTC", "recognized": False, "key_id": "4572612074143744", "drawing": [[[205, 192, 182, 185, 194, 200, 215, 217, 200, 193, 189, 188], [81, 81, 87, 109, 124, 126, 117, 105, 78, 75, 76, 79]], [[192, 202, 252, 254, 255, 252, 243, 205], [85, 86, 76, 79, 91, 93, 94, 111]], [[181, 117, 48, 23, 9, 5, 0, 4, 11, 27, 114, 132, 155, 182, 205], [83, 104, 108, 106, 110, 112, 130, 151, 159, 167, 181, 178, 166, 147, 126]], [[94, 71, 69, 73, 93, 141, 130, 125, 120, 119], [102, 27, 2, 0, 10, 24, 29, 40, 70, 103]], [[127, 138, 161, 188, 193, 194], [182, 202, 225, 224, 219, 206]]]}
if newbaby['word']==var:
    if newbaby['recognized']==False:
        year=int(newbaby['timestamp'][0:4])
        month=int(newbaby['timestamp'][5:7])
        day=int(newbaby['timestamp'][8:10])
        currDate=datetime.datetime(year, month, day)
        dayNo=currDate.weekday()

        if dayNo>5:
            print(var+":1")

#enjoy reducing this also, gege