from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
# from simulation.navy_area import Area_Model
# from simulation.navy_uuv import UUV_Model
# from simulation.navy_dive import DIVE_Model
from simulation.navy_area import area
from simulation.navy_uuv import uuv
from simulation.navy_dive import diveTeam
import numpy as np
import csv

# from ..node_graph import *

class NODE_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_input_port("start")

        #experiment design 
        document = 'C:\\Users\\USER\\Desktop\\Code\\Python_c\\simul_mcm\\user_interface\\simulation\\file\\NOB_Mixed_512DP_v1.csv' #name of DOE file 
        # document = 'simul_test.csv.(1)_restored.csv'
        self.replications = 1 #number of replications per experiment 100
        #opening an outfile 
        self.out_file = open("NOB_Mixed_512DP_v1_out.csv", 'w') #opening an output write file 
        self.owriter = csv.writer(self.out_file, delimiter=',') #creating a csv writer object 

        #Parsing the DOE data 
        self.in_file = open(document, 'r') #opening the file 
        self.in_reader = csv.reader(self.in_file) #creating a csv reader object 

        #copying the headers and printing them to the outfile 
        self.headers = next(self.in_reader) 
        self.headers = self.headers + ["totalTargets", "numMines", "numNonMines", "numUndetected", 
                    "numDetected", "numClassified", "numMILCOS", "numNOMBOS", 
                    "numNotClassified", "numFalseNeg", "numFalsePos", "completionTime"] 

        # print(headers)
        self.owriter.writerow(self.headers) #writing the headers plus the names of the other 
        # for row in self.in_reader: #examining each row or disaster from the entire data set 
        #     temp = run_model(row) #running the scenario 
        #     self.owriter.writerow(temp) #writing the data to the outfile 
            # for i in range(self.replications): #replicating each experiment 
                # temp = run_model(row) #running the scenario 
                # self.owriter.writerow(temp) #writing the data to the outfile 


        # self.in_file.close() 
        # self.out_file.close()

    def ext_trans(self, port, msg):
        
        if port == "start":
            self.row_reading()
      
    def output(self): 

       pass
            
    def int_trans(self):
        pass

    def row_reading(self):
        for row in self.in_reader: #examining each row or disaster from the entire data set 
            temp = run_model.secnarioRunner(self, row) #running the scenario 
            self.owriter.writerow(temp) #writing the data to the outfile 
    
        self.in_file.close() 
        self.out_file.close()

class run_model(NODE_Model):

    """The row should be read in from a csv reader with pre-ordered values""" 
    def __init__(self,row):
        pass

        # self.secnarioRunner(row)
    ############################## 
    # the scenario 
    ############################## 
    def secnarioRunner(self,row): 

        #makes a copy of the input data 
        self.data = list(row) #list 
        #pops items from the list to feed into the class instances 
        #x, y, target type, size, detected, classified, identified, neutralized 
        self.targets = np.array([[],[],[],[],[],[],[],[]]) 
        #Dictionary of areas, UUVs and dive teams: keys=id number, values= objects
        self.areas = {} 
        self.uuvs = {} 
        self.divers = {} 
        
        #resets the class id attribute 
        area.id = 0 
        uuv.id = 0 
        diveTeam.id = 0 
        #planning process 
        self.numUUVs = 5 #number of UUVs available (must be divisible by 5) 30
        self.numDivers = 1 #number of dive teams 10
        self.QRouteLength = 3 #length of q-route 30
        self.rowNames = ["a", "b", "c", "d", "e"] #names of the 5 rows 
        self.rowWidths = [.1, .2, .3, .2, .1] #the sizes of the areas 
        #the HQ ship is just outside of the q-route in safe waters 
        self.xHQ = 1 #NM 
        self.yHQ = sum(self.rowWidths)/2.0 #half the distance up on the y-axis 
        #scenario data 
        self.UUVsPerRow = int(1.0 * self.numUUVs/len(self.rowWidths)) #UUVs per row in the q-route 
        self.areaLen = (1.0 * self.QRouteLength) / self.UUVsPerRow #length of each UUV search area 

        #creates each individual search area 
        for i in self.rowWidths: 
            for j in range(self.UUVsPerRow): 
               self.areas[area.id] = area(self.areaLen, i) 

        #combining the areas 
        i = 1 
        for name in self.rowNames: 
            #builds an empty area for each row 
            self.areas[name] = area(length=0, width=0, encompass=set(name)) 
            
            #adds smaller areas to the end of the row area 
            for j in range(self.UUVsPerRow): 
                self.areas[name] = self.areas[name].builder(i, self.areas, True) 
                i += 1 

        #creates the combined mine threat area 
        self.areas["MTA"] = area(0,0) #creates an empty area for t 
        
        #adds rows to the MTA 
        for name in self.rowNames: 
            self.areas["MTA"] = self.areas["MTA"].builder(name, self.areas, False) 

        #mining the area 
        densityNonMines = int(self.data.pop()) 
        densityMines = int(self.data.pop()) 
        self.targets = self.areas["MTA"].mining(densityMines, densityNonMines, self.targets) 
        
        # print(f"{densityNonMines} \ {densityMines} \ {targets}")

        #building the UUV objects 
        for i in range(5): 
            transitSpeed= float(self.data.pop()) 
            deploy = float(self.data.pop()) 
            recover = float(self.data.pop()) 
            searchSpeed = float(self.data.pop()) 
            searchTime = float(self.data.pop()) 
            altitude = float(self.data.pop()) 
            spacing = float(self.data.pop()) 
            passes = int(self.data.pop()) 
            sensor = float(self.data.pop()) 
            detRate = float(self.data.pop())
            milcoRate = float(self.data.pop()) 
            nombosRate = float(self.data.pop()) 

            #each UUV in a row is built off of the same inputs 
            #detRate, milcoRate, and nombosRate are random uniforms numbers +/- .01 
            for j in range(self.UUVsPerRow): 
                self.uuvs[uuv.id] = uuv(transitSpeed=transitSpeed, deploy=deploy, recover=recover, searchSpeed=searchSpeed, searchTime=searchTime, altitude=altitude, spacing=spacing, passes=passes, sensor=sensor, detRate=np.random.uniform(detRate-.01,detRate+.01), milcoRate=np.random.uniform(milcoRate-.01,milcoRate+.01), nombosRate=np.random.uniform(nombosRate-.01, nombosRate+.01), originX=self.xHQ, originY=self.yHQ) 

        #initializes the clock to 0 
        completionTime = 0 
        test_time = 0
        
        #UUVs search their entire areas 
        for UUV in self.uuvs: 
            #detect, classify and localize 
            while self.uuvs[UUV].isActive: 
                self.targets = self.uuvs[UUV].mission(self.areas[UUV],self.targets) 

            test_time +=1
            # print(f"test score {test_time}")
            #reaquire and identify 
            self.targets = self.uuvs[UUV].reacquisitionIdentify(self.areas[UUV],self.targets) 
        
            #waits until all UUV searches and identifications are complete before starting neutr 
            if self.uuvs[UUV].clock > completionTime: 
                completionTime = self.uuvs[UUV].clock #the longest search sets the clock 

        
        #Making the dive team objects 
        resupply = int(self.data.pop()) 
        timeNonMine = float(self.data.pop()) 
        timeMine = float(self.data.pop()) 
        restTime = float(self.data.pop()) 
        sortieTime = float(self.data.pop()) 

        # print(f"making the dive team {resupply} \ {timeNonMine} \ {timeMine} \ {restTime} \ {sortieTime}")
        #builds the dive team object 
        for i in range(self.numDivers): 
            #time for all teams is the completion time of the last UUV search 
            self.divers[diveTeam.id] = diveTeam(timeNonMine=timeNonMine, 
                resupply=resupply, timeMine=timeMine, 
                restTime=restTime, sortieTime=sortieTime, originX=self.xHQ, 
                originY=self.yHQ, clock=completionTime) 
    
        #dive teams conduct prosecution until no MILCOs and false positives are left 
        while self.divers[self.numDivers].isActive: 

            #each team conducts 1 prosecution before looping back through 
            for team in self.divers: 
                self.targets = self.divers[team].prosecute(self.areas["MTA"],self.targets) 
            
                #last mine neutralized sets the clock 
                if self.divers[team].clock > completionTime: 
                    completionTime = self.divers[team].clock 

        
        #calculates output statistics 
        totalTargets = len(self.targets[1]) 
        numMines = sum(self.targets[2]) 
        numNonMines = sum(np.logical_not(self.targets[2])) 
        numUndetected = sum(np.logical_not(self.targets[4])) 
        numDetected = sum(self.targets[4]) 
        numClassified = sum(self.targets[4] * self.targets[5]) 

        numMILCOS = sum(self.targets[2]*self.targets[4]*self.targets[5]) 
        numNOMBOS = sum(np.logical_not(self.targets[2])*self.targets[4]*self.targets[5]) 
        numNotClassified = sum(self.targets[4] * np.logical_not(self.targets[5])) 
        numFalseNeg = sum(self.targets[2] * self.targets[4]*np.logical_not(self.targets[5])) 
        numFalsePos = sum(np.logical_not(self.targets[2]) * self.targets[4]*np.logical_not(self.targets[5])) 
        
        # print(f"Done result {totalTargets} \ {numMines} \ {numNonMines} \ {numUndetected} \ {numDetected} \ {numClassified} \ {numMILCOS} \ {numNOMBOS} \ {numNotClassified} \ {numFalseNeg} \ {numFalsePos}")

        return row + [totalTargets, numMines, numNonMines, numUndetected, 
        numDetected, numClassified, numMILCOS, numNOMBOS, 
        numNotClassified, numFalseNeg, numFalsePos, completionTime] 