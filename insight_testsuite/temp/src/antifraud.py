#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys # 
import csv # To read csv file
import time # To count for how much time used

class paymo(object):

	'''
	This class: paymo, is used to build up a graph to represent users' relationship by using the DICTIONARY data structure. The following two methods are included for an paymo_conn object: 1, paymoGraph　==> build a users' graph based on current transaction records. 2, paymoDegree  ==> calculate degree between any two users up to 4. 3, Calculate the number of degree and generate 3 different output files. 4, flatten_lists: a short function to change a list_of_list to a list
	'''
	
	#Build an graph based on current user transactions ==> graph: {usrid1:[usrid2, usrid3, ...]}, where usrid is of integer type
	def paymoGraph(self, batchFile):

		graph = dict()
		with open(batchFile,'rU') as f_batch_handle: #rU: read it with an universal newline mode
			f_batch = csv.reader(f_batch_handle)
			i = 0; #used to count how many transaction records
    			for line in f_batch: #deal with each record

    		        	try:    # skip inappropriate rows: rows without user ids
    		        		usr1 = int(line[1]) #user ids are in the 2nd and 3rd postion of the list
    		        		usr2 = int(line[2])
					i += 1
    				except:
					#print("Inappropriate transaction record")
            				continue

        			if usr1 not in graph: #add a new key-value pair
        		    		graph[usr1] = list() # construct value with a list data structure
			        	graph[usr1].append(usr2)
        			else:			   #append a new value for existing keys
					graph[usr1] = list(set(graph[usr1])) 
					graph[usr1].append(usr2)
            
        			if usr2 not in graph:
            				graph[usr2] = list()
            				graph[usr2].append(usr1)
        			else:
            				graph[usr2] = list(set(graph[usr2])) 
            				graph[usr2].append(usr1)        
        
		f_batch_handle.close()   #close f_batch_handle
		self.graph = graph # set the instance attribute graph


	# a short function to change a list_of_list to a list ==> flatten a nested list
	def flatten_lists(self,lst):
    		flatten = [entry for sublist in lst for entry in sublist]
		flatten = list(set(flatten)) # remove duplicated elements
    		return flatten


	#calculate degree between any two users up to 4; if any one user is not part of the built graph, return 0.
	def paymoDegree(self, graph, usr1, usr2):
		
		if (usr1 not in self.graph) or (usr2 not in self.graph): #either usr1 or usr2 not in the current transaction
			degree = 0
			return degree #degree is 0

		dist1 = self.graph[usr2]
		if usr1 in dist1:
			degree = 1
			return degree #degree is 1

		dist2 = self.flatten_lists([self.graph[key2] for key2 in dist1]) # find "a friend of a friend"
		if (usr1 not in self.graph[usr2]) and (usr1 in dist2):
			degree = 2
			return degree #degree is 2

		dist3 = self.flatten_lists([self.graph[key3] for key3 in dist2])# find a friend with degree 3
 		if (usr1 not in dist2) and (usr1 in dist3):
			degree = 3
			return degree #degree is 3     

		dist4 = self.flatten_lists([self.graph[key4] for key4 in dist3])# find a friend with degree 4
 		if (usr1 not in dist3) and (usr1 in dist4):
			degree = 4
			return degree #degree is 4


	#Calculate the number of degree between two users; Generate 3 different output files based on 3 different features[with degrees: 1, 2 and 4, respectively]
	def paymoOutput(self,graph,streamFile,outFile1,outFile2,outFile3):
		start_time = time.time() # start stopwatch
		output1 = open(outFile1,'w')
		output2 = open(outFile2,'w')
		output3 = open(outFile3,'w')
		i = 0 # In order to count how many transactions

		with open(streamFile,'rU') as f_stream_handle: #rU: open a file with an universal newline mode
			f_stream = csv.reader(f_stream_handle)
			for line in f_stream:
				try:   # skip inappropriate rows: rows without user ids
            				usr1 = int(line[1])
            				usr2 = int(line[2])
					i += 1
        			except:
					#print("Inappropriate transaction record")
					continue
	
				degree = digWallet.paymoDegree(digWallet.graph, usr1, usr2)
				#print("The degree is %s"%degree)
				if degree == 0: #Write to output files
					output1.write("unverified \n")
            				output2.write("unverified \n")
	            			output3.write("unverified \n")
				elif degree == 1:
					output1.write("trusted \n")
        	    			output2.write("trusted \n")
        	    			output3.write("trusted \n")
				elif degree == 2:
					output1.write("unverified \n")
        	    			output2.write("trusted \n")
        	    			output3.write("trusted \n")
				elif degree == 3:
					output1.write("unverified \n")
        	    			output2.write("unverified \n")
        	    			output3.write("trusted \n")						
				elif degree == 4:
					output1.write("unverified \n")
        	    			output2.write("unverified \n")
        	    			output3.write("trusted \n")
				else: #beyond degree of 4
					output1.write("unverified \n")
        	    			output2.write("unverified \n")
        	    			output3.write("unverified \n")
	
		f_stream_handle.close()          #close f_stream_handle and output files 
		output1.close()                   
		output2.close()
		output3.close()

		time_used = ((time.time()-start_time)/i)# How much average time needed of each transaction for all 3 cases together
		print("Average elapsed time of one transaction for all 3 cases together is %s s"%time_used) 
	


if __name__ == '__main__':

	# Get the input arguments
	try:
		batchFile = sys.argv[1]
		streamFile = sys.argv[2]
		outFile1 = sys.argv[3]
		outFile2 = sys.argv[4]
		outFile3 = sys.argv[5]
	except: #Type filenames mannually for inappropriate input arguments
		print("Oops! Please type the correct filenames.")
		batchFile = raw_input("Batch payment file: \n")
		streamFile = raw_input("Stream payment file: \n")
		outFile1 = raw_input("Out file1: \n")
		outFile2 = raw_input("Out file2: \n")
		outFile3 = raw_input("Out file3: \n")
	
	#Initialize an paymo type object, named as digWallet
	digWallet = paymo() 
	
	#Build an graph based on current user transactions
	digWallet.paymoGraph(batchFile)
	#print(digWallet.graph.keys()[0:5])
	#print("There are %s keys in the graph"%len(digWallet.graph))
	#print("The size of the graph is about %f Mb"%(sys.getsizeof(digWallet.graph)/1e6))
		

	#Calculate the number of degree between two users; Generate 3 different output files based on 3 different features[with degrees: 1, 2 and 4, respectively]
	digWallet.paymoOutput(digWallet.graph,streamFile,outFile1,outFile2,outFile3)

