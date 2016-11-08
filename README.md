# Table of Contents

1. Repo directory structure
2. Summary of code 
3. Details of implementation
4. Test code
5. Example

## 1, Repo directory structure


	├── README.md 
	├── run.sh
	├── image
	│  	└── graph.png    
	├── src
	│  	└── antifraud.py
	├── paymo_input
	│   └── batch_payment.csv
	|   └── stream_payment.csv
	├── paymo_output
	│   └── output1.txt
	|   └── output2.txt
	|   └── output3.txt
	└── insight_testsuite
	 	   ├── run_tests.sh
	 	   ├── results.txt
           ├── temp
           ├──  └── ...
		   └── tests
	        	└── test-1-paymo-trans
        		│   ├── paymo_input
        		│   │   └── batch_payment.csv
        		│   │   └── stream_payment.csv
        		│   └── paymo_output
        		│       └── output1.txt
        		│       └── output2.txt
        		│       └── output3.txt
        		└── test-2-my-design
            		 ├── paymo_input
        		     │   └── batch_payment.csv
        		     │   └── stream_payment.csv
        		     └── paymo_output
        		         └── output1.txt
        		         └── output2.txt
        		         └── output3.txt


## 2, Summary of code
### additional libraries
* import sys: In ordre to fetch the command line arguments
* import csv: In order to read csv file
* import time: In order to count for how much time elapsed

### code in python
In order to figure out the relationship of two customers in transatction, I build a class named paymo, which includes three main methods: 
* paymoGraph　==> Build users' graph based on current transaction records. 
* paymoDegree ==> Calculate the number of degree between any two users up to 4. 
* paymoOutput ==> Calculate the number of degree for each incoming record from stream_payment.txt and generate 3 different output files. 
    
## 3, Detail of implementation
The transaction data for each record is stored in the following format:
    `2016-11-02 09:49:29, 47424, 5995, 19.45, Food for 🌽 😎`
Thus, before doing data analysis, one need to split the data in a list and make sure the second and third represent user ids. The second and third elements are further converted to integer type. Then, 

* Buld a graph with dictionary data structure: `{id1: [id2, id3, id4, id5, ...], id2:[id1, id5, id8], ..}`
* Calculate the number of degree between two users
* Type: `python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt` to run the code; Or simply type `./run.sh` from the terminal
* Check the output files in `paymo_output` folder

## 4, Test code
* Go to directory: `insight_testsuite/tests`
* Create your own input and output test files
* Type `./run_tests.sh` from the terminal to test whether your code works or not

## 5, Example
After checking my code, I build my own transaction records stored in the required format. The relationship among users is shown in the diagram.
<img src="./image/graph.png" width="500">

Thus, the number of degree between different users should be
* 1 and 2 ==> degree: 1
* 1 and 11 ==> degree: 2
* 1 and 7 ==> degree: 2
* 1 and 9 ==> degree: 3
* 1 and 12 ==> degree: 4
* 1 and 13 ==> degree: 5
* 2 and 3 ==> degree: 2
* 1 and 4 ==> degree: 0 [no connection]

The output file `output1.txt` for the above diagram with Feature 1[up to degree 1] is as following: 

    trusted
    unverified 
    unverified 
    unverified 
    unverified 
    unverified 
    unverified 
    unverified 


The output file `output2.txt` for the above diagram with Feature 2 [up to degree 2] is as following: 

    trusted
    trusted
    trusted
    unverified 
    unverified 
    unverified 
    trusted 
    unverified 

    
The output file `output3.txt` for the above diagram with Feature 3[up to degree 4] is as following: 

    trusted
    trusted 
    trusted 
    trusted 
    trusted 
    unverified 
    trusted 
    unverified 
