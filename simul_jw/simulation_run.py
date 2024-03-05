import sys 
import csv 
import chardet
from simulation_area import * 
from simulation_uuv import * 
from simulation_dive import * 


############################## 
# the scenario 
############################## 
def secnarioRunner(row): 
    
    """The row should be read in from a csv reader with pre-ordered values""" 
    
    #makes a copy of the input data 
    data = list(row) #list 
    #pops items from the list to feed into the class instances 
    #x, y, target type, size, detected, classified, identified, neutralized 
    targets = np.array([[],[],[],[],[],[],[],[]]) 
    #Dictionary of areas, UUVs and dive teams: keys=id number, values= objects
    areas = {} 
    uuvs = {} 
    divers = {} 
    
    #resets the class id attribute 
    area.id = 0 
    uuv.id = 0 
    diveTeam.id = 0 
    #planning process 
    numUUVs = 5 #number of UUVs available (must be divisible by 5) 30
    numDivers = 1 #number of dive teams 10
    QRouteLength = 3 #length of q-route 30
    rowNames = ["a", "b", "c", "d", "e"] #names of the 5 rows 
    rowWidths = [.1, .2, .3, .2, .1] #the sizes of the areas 
    #the HQ ship is just outside of the q-route in safe waters 
    xHQ = 1 #NM 
    yHQ = sum(rowWidths)/2.0 #half the distance up on the y-axis 
    #scenario data 
    UUVsPerRow = int(1.0 * numUUVs/len(rowWidths)) #UUVs per row in the q-route 
    areaLen = (1.0 * QRouteLength) / UUVsPerRow #length of each UUV search area 
    
    #creates each individual search area 
    for i in rowWidths: 
        for j in range(UUVsPerRow): 
            areas[area.id] = area(areaLen, i) 

    #combining the areas 
    i = 1 
    for name in rowNames: 
        #builds an empty area for each row 
        areas[name] = area(length=0, width=0, encompass=set(name)) 
        
        #adds smaller areas to the end of the row area 
        for j in range(UUVsPerRow): 
            areas[name] = areas[name].builder(i, areas, True) 
            i += 1 

    #creates the combined mine threat area 
    areas["MTA"] = area(0,0) #creates an empty area for t 
    
    #adds rows to the MTA 
    for name in rowNames: 
        areas["MTA"] = areas["MTA"].builder(name, areas, False) 

    #mining the area 
    densityNonMines = int(data.pop()) 
    densityMines = int(data.pop()) 
    targets = areas["MTA"].mining(densityMines, densityNonMines, targets) 
    
    # print(f"{densityNonMines} \ {densityMines} \ {targets}")

    #building the UUV objects 
    for i in range(5): 
        transitSpeed= float(data.pop()) 
        deploy = float(data.pop()) 
        recover = float(data.pop()) 
        searchSpeed = float(data.pop()) 
        searchTime = float(data.pop()) 
        altitude = float(data.pop()) 
        spacing = float(data.pop()) 
        passes = int(data.pop()) 
        sensor = float(data.pop()) 
        detRate = float(data.pop())
        milcoRate = float(data.pop()) 
        nombosRate = float(data.pop()) 

        #each UUV in a row is built off of the same inputs 
        #detRate, milcoRate, and nombosRate are random uniforms numbers +/- .01 
        for j in range(UUVsPerRow): 
            uuvs[uuv.id] = uuv(transitSpeed=transitSpeed, deploy=deploy, recover=recover, searchSpeed=searchSpeed, searchTime=searchTime, altitude=altitude, spacing=spacing, passes=passes, sensor=sensor, detRate=np.random.uniform(detRate-.01,detRate+.01), milcoRate=np.random.uniform(milcoRate-.01,milcoRate+.01), nombosRate=np.random.uniform(nombosRate-.01, nombosRate+.01), originX=xHQ, originY=yHQ) 

    #initializes the clock to 0 
    completionTime = 0 
    test_time = 0
    
    #UUVs search their entire areas 
    for UUV in uuvs: 
        
        #detect, classify and localize 
        while uuvs[UUV].isActive: 
            targets = uuvs[UUV].mission(areas[UUV],targets) 

        test_time +=1
        # print(f"test score {test_time}")
        #reaquire and identify 
        targets = uuvs[UUV].reacquisitionIdentify(areas[UUV],targets) 
    
        #waits until all UUV searches and identifications are complete before starting neutr 
        if uuvs[UUV].clock > completionTime: 
            completionTime = uuvs[UUV].clock #the longest search sets the clock 

    
    #Making the dive team objects 
    resupply = int(data.pop()) 
    timeNonMine = float(data.pop()) 
    timeMine = float(data.pop()) 
    restTime = float(data.pop()) 
    sortieTime = float(data.pop()) 

    # print(f"making the dive team {resupply} \ {timeNonMine} \ {timeMine} \ {restTime} \ {sortieTime}")
    #builds the dive team object 
    for i in range(numDivers): 
        #time for all teams is the completion time of the last UUV search 
        divers[diveTeam.id] = diveTeam(timeNonMine=timeNonMine, 
            resupply=resupply, timeMine=timeMine, 
            restTime=restTime, sortieTime=sortieTime, originX=xHQ, 
            originY=yHQ, clock=completionTime) 
   
    #dive teams conduct prosecution until no MILCOs and false positives are left 
    while divers[numDivers].isActive: 

        #each team conducts 1 prosecution before looping back through 
        for team in divers: 
            targets = divers[team].prosecute(areas["MTA"],targets) 
        
            #last mine neutralized sets the clock 
            if divers[team].clock > completionTime: 
                completionTime = divers[team].clock 

    
    #calculates output statistics 
    totalTargets = len(targets[1]) 
    numMines = sum(targets[2]) 
    numNonMines = sum(np.logical_not(targets[2])) 
    numUndetected = sum(np.logical_not(targets[4])) 
    numDetected = sum(targets[4]) 
    numClassified = sum(targets[4] * targets[5]) 

    numMILCOS = sum(targets[2]*targets[4]*targets[5]) 
    numNOMBOS = sum(np.logical_not(targets[2])*targets[4]*targets[5]) 
    numNotClassified = sum(targets[4] * np.logical_not(targets[5])) 
    numFalseNeg = sum(targets[2] * targets[4]*np.logical_not(targets[5])) 
    numFalsePos = sum(np.logical_not(targets[2]) * targets[4]*np.logical_not(targets[5])) 
    
    # print(f"Done result {totalTargets} \ {numMines} \ {numNonMines} \ {numUndetected} \ {numDetected} \ {numClassified} \ {numMILCOS} \ {numNOMBOS} \ {numNotClassified} \ {numFalseNeg} \ {numFalsePos}")

    return row + [totalTargets, numMines, numNonMines, numUndetected, 
    numDetected, numClassified, numMILCOS, numNOMBOS, 
    numNotClassified, numFalseNeg, numFalsePos, completionTime] 

all_time = 0
#experiment design 
document = 'NOB_Mixed_512DP_v1.csv' #name of DOE file 
# document = 'simul_test.csv.(1)_restored.csv'
replications = 1 #number of replications per experiment 100
#opening an outfile 
out_file = open("NOB_Mixed_512DP_v1_out.csv", 'w') #opening an output write file 
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
        if temp:
            all_time +=1
            print(all_time)
        owriter.writerow(temp) #writing the data to the outfile 


in_file.close() 
out_file.close()
