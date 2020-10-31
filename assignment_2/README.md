# Assignment 2
Chuck code for the second assignment here. 

## Spec Sheet:
The link to the specification sheet can be found [here](https://forum.pesu.io/uploads/short-url/mAlIiisafHf7Ovcz3L0CkdyZlrI.pdf)
The detailed specifications can be found on [forums](https://forum.pesu.io/t/assignment-2-updated-specifications-latest/13533)

## Dataset link:
The Data set can be downloaded from [here](https://snap.stanford.edu/data/web-Google.txt.gz)

If the link is not working go to [this](https://snap.stanford.edu/data/web-Google.html) site and download the ```web-Google.txt.gz``` file under the ```Files``` section.

## Bash Script to check for convergence
We also need a bash script to check for convergence (this is needed for task 2) this script can be found [here](https://drive.google.com/drive/folders/1mxBS0gKctuPFV-Dss5qvCcUs8P2pffFq) 
This link also contains a python file which is apprently used to check for convergence.
The link to the TA's note for the above on forums is found [here](https://forum.pesu.io/t/important-bash-script-for-convergence-check-assignment-2/13607)

Also Remember 
The lord yeetith and the lord yoinkith away

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