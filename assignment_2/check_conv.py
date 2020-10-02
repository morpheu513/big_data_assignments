import shutil
import os
count=0
n=0
conv =0.5 

def rewrite_pagerank():
	os.remove("/home/morpheus/big_data_assignments/assignment_2/v") #change the path
	source = "/home/morpheus/big_data_assignments/assignment_2/v1"  #change the path
	destination = "/home/morpheus/big_data_assignments/assignment_2/v" #change the path
	dest = shutil.copyfile(source, destination) 



with open("/home/morpheus/big_data_assignments/assignment_2/v") as file1, open("/home/morpheus/big_data_assignments/assignment_2/v1") as file2:  #change the path
	for line1, line2 in zip(file1, file2):
		count+=1
		old_pagerank=float(line1.split(",")[1])
		new_pagerank=float(line2.split(",")[1])

		if(abs(old_pagerank-new_pagerank) < conv):
			n+=1

	if(n==count):
		print(0)
	else:
		rewrite_pagerank()
		print(1)
