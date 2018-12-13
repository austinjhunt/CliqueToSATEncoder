#!flask/bin/python
import os
import sys
import multiprocessing as mp
from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)



def readDimacsString(dimacsdict,k,vetuple): 
	v,e = vetuple[0],vetuple[1]

	# this will be one text file 
	# want the dimacs string
	# split on \n\n
	# res[1] will be string of all literals

	# only worry about this instance if the current k < = v
	if k <= v: 
		try:
			fileName = "graph_" + str(v) + "E_" + str(e) + "E.txt"
			print("in directory k= ",k)
			f = open(fileName,"r")
			contents = f.read()

			try: 
				dimacsstring = contents.split('\n\n')[1]
				dimacsstring = dimacsstring.strip(' \t\n\r')
				dimacsdict["k_" + str(k) + "_" + fileName[:-4]] = dimacsstring[15:]
				return dimacsdict 
			except:
				pass 
		except: 
			pass

		


def docurrentkstuff(dimacsdict, k,owd,v_e_list):

	# merge the two lists 
	os.chdir(owd)
	# go to this k's directory
	path = "clique_of_k_" + str(k)

	os.chdir(path)

	# Setup a list of processes that we want to run
	# Want one process for smaller sizes
	# 2 processes for big size
	childprocesses = [mp.Process(target=readDimacsString, args=(dimacsdict,k,arglist)) for arglist in v_e_list]
	# Run the processes
	for p in childprocesses:
		p.start()
		print("Starting",p)

	# Exit the completed processes
	for p in childprocesses:
		print("Ending",p)
		p.join()
	return dimacsdict




@app.route('/')
def output():
	# dont worry about serving templates
	# just pass list of dimacs strings to minisat.js
	# let minisat generate list of corresponding outputs, 
	# then minisat will post them back to server (here), and they will be written to the proper files
	path = "tests2"
	if os.getcwd() != 'tests2':
		os.chdir(path) 
	owd = os.getcwd()
	
	# init dimacs list to [], allow all processes to append
	manager = mp.Manager()
	dimacsdict = manager.dict()

	# use many different values of k (2 <= k <= 30)
	# use one process per k
	klist = [2,6,10,11,20]
	v_e_list = [[5,4], [10,15], [20,30], [50,80],[100,200],[1000,2000]]
	kprocesses = [mp.Process(target=docurrentkstuff, args=(dimacsdict,k,owd,v_e_list)) for k in klist]
	for kp in kprocesses:
		kp.start()
	for kp in kprocesses:
		kp.join()

	print(dimacsdict)

	# now dimacs list is list of all dimacs strings, pass to js
	#print(dimacslist)
	return render_template('index.html',ddict=dimacsdict) 



import glob

@app.route('/receiver', methods = ['POST'])
def worker():

	#get solutions from js 
	solutions = request.form['solutionsdict[]']
	print(solutions)

	



	return solutions


if __name__ == '__main__':
	# run!
	app.run("0.0.0.0","8000")









