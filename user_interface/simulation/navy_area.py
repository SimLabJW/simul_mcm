# from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np 
import matplotlib.pyplot as plt 
import csv 

############################## 
# General Functions and Variables 
############################## 
 
def listStructure(myList): 
    #this function takes the array of targets and refits the vectors to their intended data types 
    #x[0], y[1], targetType[2], size[3], detected[4], classified[5], neutralized[6], actionNeeded[7] 
    myList[0].astype(float) 
    myList[1].astype(float) 
    myList[2].astype(int) 
    myList[3].astype(float) 
    myList[4].astype(int) 
    myList[5].astype(int) 
    myList[6].astype(int) 
    myList[7].astype(int) 

    return myList 



# #########################################
# class Area_Model(BehaviorModelExecutor):
#     def __init__(self, instance_time, destruct_time, name, engine_name):
#         BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
#         self.init_state("Wait")
#         self.insert_state("Wait", Infinite)
#         self.insert_state("Generate",1)
    
#         self.insert_input_port("start")


#     def ext_trans(self, port, msg):
        
#         if port == "start":
#             pass

      
#     def output(self): 

#        pass
            
#     def int_trans(self):
#         pass
    


############################## 
# Search Area Class 
############################## 
class area(): 
    """Object to build Search Area 
    length: length of the area on the x-axis(float type) 
    width: width of the area on the y-asis (float type) 
    refX: x coordinate of the bottom right corner (float type) 
    refY: y coordinate of the bottom right corner (float type) 
    encompass: set of all areas that made an area (set)""" 
    
    id = 0 #number of areas created 
 
    def __init__(self, length, width, refX=0, refY=0, encompass=set()): 
    
        self.length = float(length) #length of area in miles (float type) 
        self.width = float(width) #width of area in miles (float type) 
        self.refX = refX #latitude of bottom left corner 
        self.refY = refY #longitude of bottom left corner 
        area.id += 1 # increment the counter 
        self.id = area.id #id number of the assigned instance 
        self.encompass = encompass | set([self.id]) #the set of all encompassing sets 
    
    def __repr__(self): 
        #the instance representation 
        print(self.encompass) 
        return "len=%.2f, wid=%.2f, position=(%.2f, %.2f), id=%d, encompassing\
            areas:" % (self.length, self.width, self.refX, self.refY, self.id) 
    
    #places mines and non-mines (assuming only Manta bottom mines) 
    def mining(self, densityMines, densityNonMines, targets, sizeMine=0.98, meanSize=1, 
        stdSize=0.5): 
        """densityMines: mines per square mile 
        densityNonMines: non-mines per square mile 
        sizeMine: diameter of mines (meters) 
        meanSize: mean diameter of non-mines (meters) 
        stdSize: standard deviation of non-mine diameter (meters) 
        targets is array of targets""" 
        #Generating the targets and randomly positioning them within the search area 
        areaSize = self.length * self.width #area of search area 
        numMines = int(densityMines * areaSize) #number of mines in the area 
        numNonMines = int(densityNonMines * areaSize) #number of non-mines in the area 
        total = numMines + numNonMines 
        x = np.random.uniform(0, self.length, total) #array of random x coordinates for each target 
        y = np.random.uniform(0, self.width, total) #array of random y coordinates for each target 
        
        #Determining whether the objects are mines or non-mines 
        nonMineType = np.zeros(numNonMines, dtype=bool) #array of 0s to represent number of non-mines 
        mineType = np.ones(numMines, dtype=bool) #array of 1s to represent number of mines 
        targetType = np.concatenate((nonMineType, mineType)) #combined array of the 0 array and 1 array 
        np.random.shuffle(targetType) #scrambling the array of mines and non-mines 
        
        #calculating the area of target 
        size = np.ones(total) * sizeMine #array where all sizes are set to mine shaped diameter 
        size = np.where(targetType, size, np.random.normal(1,0.3,total)) #logical array 
        #if NOMBOS, then reassigns the diameter to a normal random number 
        size = np.pi * (size/2.0)**2 #array converting all diameters to areas 
        
        #initializes all shapes to be undetected, unclassified and unneutralized 
        detected = np.zeros(total, dtype= bool) #array of Falses to represent undetected targets 
        classified = np.zeros(total, dtype= bool) #array of Falses to represent unclassified targets 
        identified = np.zeros(total, dtype= bool) #array of Falses to represent unidentified targets 
        neutralized = np.zeros(total, dtype=bool) #array of Falses to represent unneutralized targets 
        
        #populates the scenario mine list into an 8 dimensional array 
        newTargets = np.vstack((x, y, targetType, size, detected, classified, identified, neutralized)) 
        
        #concatenates the old targets with the new targets 
        targets = np.hstack((targets,newTargets)) 
        listStructure(targets) #reformating the targets list 
        return targets 
    
    
    #combines areas 
    def builder(self, adjoining, dictionary, addLength): 
        """adjoining: area to be positioned next to or below the subject area 
        dictionary: the areas dictionary 
        #addLength: combine "other" left (True) or below (False)""" 
        
        #if the stationary area has no length or width attributes 
        if self.length == 0 and not addLength: #if also adding to the width 
            self.length = dictionary[adjoining].length #set the equal to the adjoining area 
        if self.width ==0 and addLength: #if adding to the length 
            self.width = dictionary[adjoining].width #set it equal to the adjoining area 
        
        #updating the reference points of the adjoining area 
        offsetX = self.refX + self.length * addLength #offset in x direction for the other area 
        offsetY = self.refY + self.width * (not addLength) #offset in y direction for the other area 
        
        #for each area in the encompassing set of areas in the adjoining area 
        for item in dictionary[adjoining].encompass: 
            #try because not all encompassing areas exist due to combining areas using the same name 
            try: 
                dictionary[item].refX += offsetX #adding to the x position if adding to the length 
                dictionary[item].refY += offsetY #adding to the y position if adding to the width 
            except: 
                pass 
        
        #updating the length and width of the new area 
        #new length is addition of previous two lengths if adding length 
        updateLen = self.length + dictionary[adjoining].length * addLength 
        #new width is addition of previous two widths 
        updateWid = self.width + dictionary[adjoining].width * (not addLength) 
        
        #union of the sets of encompassing areas for both areas 
        encomp = self.encompass | dictionary[adjoining].encompass 
        #returning a new area object with new parameters 
        return area(length=updateLen, width=updateWid, refX=self.refX, refY=self.refY, encompass = encomp) #returns new area 

        #plotting an area 
    def plotArea(self, target): 
        """This function plots the search area 
        light grey: undetected targets 
        blue: MILCOs 
        red: false negatives 
        green: NOMBOS 
        yellow: false positives 
        green: prosecuted""" 
        
        
        targets = listStructure(target) 
        #x[0], y[1], targetType[2], size[3], detected[4], classified[5], neutralized[6], actionNeeded[7] 
        #arrays 
        x = targets[0] 
        y = targets[1] 
        targetType = targets[2] 
        size = targets[3] 
        detected = targets[4] 
        classified = targets[5] 
        neutralized = targets[6] 
        
        #subsetting certain objects in order to colorcode them 
        size = size * 20 #setting the size of target markers 
        undetected = np.ma.masked_where(detected, size) #masking everything that has been detected 
        milco = np.ma.masked_where(targetType * detected * classified==False, size) 
        #masking non-mines and false-negatives
        falseNeg = np.ma.masked_where(targetType * detected * 
        np.logical_not(classified)==False, size) #masking non-mines and MILCOs 
        nombos = np.ma.masked_where(np.logical_not(targetType) * detected * 
        classified==False, size) #masking mines and false-positives 
        falsePos = np.ma.masked_where(np.logical_not(targetType) * detected * 
        np.logical_not(classified)==False, size) #masking mines and NOMBOS 
        prosecuted = np.ma.masked_where(neutralized==False, size) #masking everything that hasn't been prosecuted 
        #plotting 
        plt.close() #clear any old plots 
        # plt.subplot(111, axisbg='lightblue') #plotting one subplot to make the background lightblue 
        plt.xlim(0, self.length) #setting x limits 
        plt.ylim(0, self.width) #setting y limits 
        plt.scatter(x, y, s=undetected, marker='o', c="lightgrey", linewidth='0.5') #plotting undetected targets 
        plt.scatter(x, y, s=milco, marker='o', c="blue", linewidth='0.5') 
        #plotting MILCOs# 
        plt.scatter(x, y, s=falseNeg, marker='o', c="red", linewidth='0.5') 
        #plotting false negs 
        plt.scatter(x, y, s=nombos, marker='o', c="green", linewidth='0.5') 
        #plotting NOMBOS 
        plt.scatter(x, y, s=falsePos, marker='o', c="yellow", linewidth='0.5') 
        #plotting false pos 
        plt.scatter(x, y, s=prosecuted, marker='o', c="green", linewidth='0.5') 
        #plotting prosecuted targets 
        plt.axis('scaled') 
        plt.show() 