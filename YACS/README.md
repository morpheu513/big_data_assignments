# YACS 
A centralized scheduler implemented in python.
## Table Of Contents:
* [Directory Structure](#directory-structure)
* [Execution](#execution)
* [Libraries Required](#libraries-required)
* [Links](#links)

## Directory Structure:
```
.
|-- data
|   |-- LL
|   |   |-- . 
|   |-- RANDOM
|   |   |-- . 
|   |-- RR
|   |   |-- . 
|   |-- config.json
|-- src
|   |-- analysis.py
|   |-- master.py
|   |-- requests_eval.py
|   |-- requests.py
|   |-- worker.py
```
### Description:
* ```data``` contains the log files along with the config file required for the master. Log files are written as ```.csv``` files into respective folders based on the scheduling algorithm used.
* ```src``` contains the source code for the master, workers, job creation and analysis.

## Execution:
Follow the given steps to execute the source code.
### Start master:
On a new terminal run the ```master.py``` file. This file takes in positional arguments, first one is the path to the ```config.json``` file and the second one is the type of scheduling algorithm to be used. For example if we want to use Round-robin scheduling, we would type:
```
python3 master.py '<path-to-config.json-file>' 'RR'
```
### Start workers:
Depending on the number of workers provided in the ```config.json``` file, we should start those many workers.
<br>

The ```worker.py``` file takes in 2 positional arguments which are as follows, the first one is the port number on which the worker listen to updates from the master and the second one is the worker id.
<br>

Both these values should match with the values provided in the ```config.json``` file. For example if we want to start the worker with id=2 and port number 5000, we would type in the following command:
```
python3 worker.py 5000 1
```
### Generate requests:
Requests or Jobs can be generated using both the ```requests.py``` and ```requests_eval.py``` files. If your using the ```requests.py``` file you should pass a single argument while executing it, which defines the number of jobs/requests generated.
<br>

If your using the ```requests_eval.py``` file you have to provide specific information of the request, like the number of map tasks, duration of job,etc.

### Perform analysis:
To return results like the mean job execution time, mean task execution time, etc the ```analysis.py``` file should be run. This file takes in one argument which is, the number of workers present in the current configuration.
<br>

For example if we have 3 workers in our configuration then the command would be:
```
python3 analysis.py 3
```
**Note:** Ensure that all log files(for all scheduling algorithms) are generated correctly before running the ```analysis.py``` file.


## Libraries Required:
* json
* socket
* time
* sys
* random
* numpy
* pandas
* matplotlib

## Links:
### Drive:
* [Main drive link](https://drive.google.com/drive/folders/1q0n7PEajXKe3edjMJMpfjI0sfZHiadeD?usp=sharing)
* [Spec sheet](https://drive.google.com/file/d/1g6Xcj5gT_n9p4A4HQVPFNsKCaUi2LJNj/view?usp=sharing)
* [Presentation](https://drive.google.com/file/d/1q43w8KYLoJQQA9duxCpvPxIlNf-E5dIs/view?usp=sharing)
* [Config file](https://drive.google.com/file/d/1zevEdi5RCwnRkhW1_p8ogGDw1wpFJHxN/view?usp=sharing)
* [Requests file](https://drive.google.com/file/d/1P7GAD01ky0TN57ATCbMGTbHfU4XFfvMM/view?usp=sharing)
* [Report template](https://drive.google.com/file/d/1DIIITXPPkG1TRLIrkn79F14zS0kpa8WL/view?usp=sharing)

### Forums:
* [Big Data topic](https://forum.pesu.io/c/rr-dept-of-cse/rr-cs-bigdata/701)
* [Spec sheet/dataset](https://forum.pesu.io/t/big-data-2020-class-project-yacs-coding/14044/3)
