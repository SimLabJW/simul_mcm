import sys 
import csv 
import chardet
from Defualt import * 
# 파일명
document = 'outters.csv'

# Daraframe형식으로 엑셀 파일 읽기
in_file = open(document, 'r')
in_reader = csv.reader(in_file)
headers = next(in_reader) 


print(headers)

headers = headers + ["totalTargets", "numMines", "numNonMines", "numUndetected", 
            "numDetected", "numClassified", "numMILCOS", "numNOMBOS", 
            "numNotClassified", "numFalseNeg", "numFalsePos", "completionTime"] 

list=  list(row)