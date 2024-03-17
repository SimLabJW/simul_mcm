from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
from navy_area import Area_Model
from navy_uuv import UUV_Model
from navy_dive import DIVE_Model

class NODE_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
    

        self.insert_input_port("start")

    def ext_trans(self, port, msg):
        
        if port == "start":
            pass

      
    def output(self): 

       pass
            
    def int_trans(self):
        pass
    
class run_model(NODE_Model):

    """The row should be read in from a csv reader with pre-ordered values""" 
    def __init__(self):
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
        self.Area_Model.area.id = 0 
        self.UUV_Model.uuv.id = 0 
        self.DIVE_Model.diveTeam.id = 0 
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
    
    ############################## 
    # the scenario 
    ############################## 
    def secnarioRunner(self, row): 
        #creates each individual search area 
        for i in self.rowWidths: 
            for j in range(self.UUVsPerRow): 
                Area_Model.areas[Area_Model.area.id] = Area_Model.area(Area_Model.areaLen, i) 

        #combining the areas 
        i = 1 
        for name in self.rowNames: 
            #builds an empty area for each row 
            self.areas[name] = self.area(length=0, width=0, encompass=set(name)) 
            
            #adds smaller areas to the end of the row area 
            for j in range(self.UUVsPerRow): 
                self.areas[name] = self.areas[name].builder(i, self.areas, True) 
                i += 1 

        #creates the combined mine threat area 
        self.areas["MTA"] = self.area(0,0) #creates an empty area for t 
        
        #adds rows to the MTA 
        for name in self.rowNames: 
            self.areas["MTA"] = self.areas["MTA"].builder(name, self.areas, False) 

        #mining the area 
        densityNonMines = int(self.data.pop()) 
        densityMines = int(self.data.pop()) 
        targets = self.areas["MTA"].mining(densityMines, densityNonMines, targets) 
        
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
                self.uuvs[self.uuv.id] = self.uuv(transitSpeed=transitSpeed, deploy=deploy, recover=recover, searchSpeed=searchSpeed, searchTime=searchTime, altitude=altitude, spacing=spacing, passes=passes, sensor=sensor, detRate=np.random.uniform(detRate-.01,detRate+.01), milcoRate=np.random.uniform(milcoRate-.01,milcoRate+.01), nombosRate=np.random.uniform(nombosRate-.01, nombosRate+.01), originX=xHQ, originY=yHQ) 

        #initializes the clock to 0 
        completionTime = 0 
        test_time = 0
        
        #UUVs search their entire areas 
        for UUV in self.uuvs: 
            
            #detect, classify and localize 
            while self.uuvs[UUV].isActive: 
                targets = self.uuvs[UUV].mission(self.areas[UUV],targets) 

            test_time +=1
            # print(f"test score {test_time}")
            #reaquire and identify 
            targets = self.uuvs[UUV].reacquisitionIdentify(self.areas[UUV],targets) 
        
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
            self.divers[self.diveTeam.id] = self.diveTeam(timeNonMine=timeNonMine, 
                resupply=resupply, timeMine=timeMine, 
                restTime=restTime, sortieTime=sortieTime, originX=self.xHQ, 
                originY=self.yHQ, clock=completionTime) 
    
        #dive teams conduct prosecution until no MILCOs and false positives are left 
        while self.divers[self.numDivers].isActive: 

            #each team conducts 1 prosecution before looping back through 
            for team in self.divers: 
                targets = self.divers[team].prosecute(self.areas["MTA"],targets) 
            
                #last mine neutralized sets the clock 
                if self.divers[team].clock > completionTime: 
                    completionTime = self.divers[team].clock 

        
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