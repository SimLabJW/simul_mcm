import sys 
import csv 
import chardet
from Defualt import * 
#experiment design 
document = 'test1.csv' #name of DOE file 
replications = 100 #number of replications per experiment 
#opening an outfile 
out_file = open("outters.csv", 'w') #opening an output write file 
owriter = csv.writer(out_file, delimiter=',') #creating a csv writer object 

#Parsing the DOE data 
in_file = open(document, 'r') #opening the file 
in_reader = csv.reader(in_file) #creating a csv reader object 

#copying the headers and printing them to the outfile 
headers = next(in_reader) 
headers = headers + ["totalTargets", "numMines", "numNonMines", "numUndetected", 
            "numDetected", "numClassified", "numMILCOS", "numNOMBOS", 
            "numNotClassified", "numFalseNeg", "numFalsePos", "completionTime"] 

# print(headers)
owriter.writerow(headers) #writing the headers plus the names of the other 

#parsing the data 
for row in in_reader: #examining each row or disaster from the entire data set 
    for i in range(replications): #replicating each experiment 
        temp = secnarioRunner(row) #running the scenario 
        # print(temp)
        # test_code = area.plotArea(temp)
        owriter.writerow(temp) #writing the data to the outfile 


in_file.close() 
out_file.close()
