The primary file to be observed here is the clique2sat.py file. The testInstances.py file is the file used for building a web app for automating the testing, which was only PARTIALLY successful. It has some errors with JSON transmission/parsing, so it doesn't return a complete set of test cases. The clique2sat file uses some multiprocessing in an attempt to speed up the testing process. It contains methods for

1) encoding instances of the clique problem into DIMACS format
2) interpreting the results of the sat solver in the context of the clique problem 
