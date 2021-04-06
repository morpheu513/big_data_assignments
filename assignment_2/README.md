# Assignment 2
Chuck code for the second assignment here. 

## Dataset link:
The Data set can be downloaded from [here](https://snap.stanford.edu/data/web-Google.txt.gz)

If the link is not working go to [this](https://snap.stanford.edu/data/web-Google.html) site and download the ```web-Google.txt.gz``` file under the ```Files``` section.

## Running the files:

The mapper and recuder for each task are present under their respective directories. You can test out these files locally(without hadoop) or run them on hadoop's dfs. 


First youll need to start hadoop and its distributed file system. If you havent done this already follow the steps mentinoed [here](https://github.com/morpheu513/big_data_assignments/tree/master/assignment_1#step-1-starting-hadoop) to start hadoop.
<br>
<br>
Before running the ```iterate-hadoop.sh``` file you will first need to change the paths provided in the code as they are all machine specific.

For convenience all places where the path needs to be changed have been marked with the comment  ```#change the path```
<br>
<br>
After you have changed all the paths run the following command to begin calculating the page ranks:
```
bash iterate-hadoop.sh
```

The process will automatically stop after the page ranks converge. 

The final output will be stored in a file called ```v```. The format of this file is:
```
node, page_rank
```