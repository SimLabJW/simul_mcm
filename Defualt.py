import numpy as np 
import matplotlib.pyplot as plt 
############################## 
# General Functions and Variables 
############################## 
#cartesian calculator 
def distCalculator(x1, y1, x2, y2): 
    """x1: vector of x coordinates 
    y1: array of y coordinates 
    x2: array of x coordinates 
    y2: array of y coordinates""" 
    return np.sqrt((x1-x2)**2 + (y1-y2)**2) #returns a vector of the distance of the two points 
 
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

############################## 
# Search Area Class 
############################## 
class area(object): 
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
        detected = np.zeros(total, dtype= bool) #array of Falses to represent undetected 
        targets 
        classified = np.zeros(total, dtype= bool) #array of Falses to represent unclassified targets 
        identified = np.zeros(total, dtype= bool) #array of Falses to represent unidentified targets 
        neutralized = np.zeros(total, dtype=bool) #array of Falses to represent unneutralized targets 
        
        #populates the scenario mine list into an 8 dimensional array 
        newTargets = np.vstack((x, y, targetType, size, detected, classified, identified, 
        neutralized)) 
        
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

############################## 
# 
# UUV Class 
# 
############################## 
class uuv(object): 
    """transitSpeed (kts) 
    deploy (min) 
    recover (min) 
    searchTime (hrs) 
    searchTime (hrs) 
    altitude (meters) 
    spacing (meters) 
    passes (1, 2, ...) 
    sensor (meters) 
    setRate (0 - 50) 
    milcoRate (0-50) 
    nombosRate (0-50) 
    originX (-inf, 0) 
    originY (-inf, 0) 
    """ 
    id = 0 
    
    def __init__(self, transitSpeed=15, deploy=10, recover=10, 
        searchSpeed=4, searchTime=4, altitude=5, spacing=90, passes= 1, 
        sensor=3000, detRate=50, milcoRate=50, nombosRate=50, originX=0, originY=0): 
        
        #UUV attributes 
        self.transitSpeed = float(transitSpeed) #transit speed from base to search area on RHIB 
        self.deploy = deploy/60.0 #time to deploy UUV (converted to hrs) 
        self.recover = recover/60.0 #time to recover UUV after mission (converted to hrs) 
        self.searchSpeed = float(searchSpeed) #speed of UUV during search 
        self.searchTime = float(searchTime) #time of missions 
        self.altitude = altitude * 0.0005399568 #altitude of UUV during search (converted to NM) 
        self.spacing = spacing * 0.0005399568 #track spacing (converted to NM) 
        self.passes = int(passes) #number of passes per track 
        self.sensor = sensor * 0.0005399568 #track spacing (converted to NM) 
        self.detRate = detRate #detect rate (lateral range curve shape parameter) 
        self.milcoRate= milcoRate #classification rate MILCO (lateral range curve shape parameter) 
        self.nombosRate = nombosRate #classification rate NOMBOS (lateral range curve shape parameter) 
        self.originX = originX #staging area x-coordinate 
        self.originY = originY #staging area y-coordinate 
        uuv.id += 1 # increment the counter 
        self.id = uuv.id 
        #working variables 
        self.currentTrack = 0 #which track is the UUV searching 
        self.currentPass = 0 #current pass for given track 
        self.currentX = self.originX 
        self.currentY = self.originY 
        self.missionClock = 0 #clock per mission 
        self.numMissions = 0 #number of missions 
        self.clock = 0 #time of completion of last mission 
        self.isActive = True #is UUV still searching 
    
    #calculates the probability using inverse square law 
    def probability(self, area, targets, ability): 
        yCoord = area.refY + self.currentTrack * self.spacing #determines y coordinate based on current search track 
        y = targets[1] #array of y coordinate of the target 
        size = targets[3] #array of the sizes of the target 
        cpa = distCalculator(0, yCoord, 0, y) #array of closest points of approach to all mines per track 
        probability = 1-np.exp(((-2)* ability * size * self.altitude)/ (self.searchSpeed*(self.altitude**2+cpa**2))) #array of probabilities based on inverse cube law 
        probability = np.where(cpa < self.sensor, probability, 0) #array setting probabilities to 0 if out of range 
        return probability #returns array of probabilities 
 
    #conducts search on a track 
    def searchTrack(self, area, targets): 
 
        #calculates probabilities to each target for each 
        P_d = self.probability(area, targets, self.detRate) #P{detect} 
        P_milco = self.probability(area, targets, self.milcoRate) * P_d #P{classify as MILCO}*Pd 
        P_nombos = self.probability(area, targets, self.nombosRate) * P_d #P{classify as NOMBOS} 
        
        #x[0], y[1], targetType[2], size[3], detected[4], classified[5], identified[6], neutralized[7] 
        #arrays 
        targetType = np.array(targets[2]) 
        detected = targets[4] 
        classified = targets[5] 
        identified = targets[6] 
        
        #post mission analysis - looking at sonar data 
        look = np.random.uniform(0, 1, len(targetType)) #random numbers of each mine 
        #take a look if not classified 
        targets[4] = np.where(classified, detected, look<P_d) #array 
        #classifies MILCO or false negative 
        targets[5] = np.where(np.logical_and(targetType==True, classified==False), 
        look<P_milco, classified) #array 
        #classifies NOMBOS or false positive 
        targets[5] = np.where(np.logical_and(targetType==False,classified==False), 
        look<P_nombos, classified)#array 
        #which targets are MILCOS and which are false positives 
        #recalculates after search 
        detected = targets[4] #array 
        #recalculates after search 
        classified = targets[5] #array 
        #determines if MILCO or false positive 
        isMILCO = targetType * detected * classified #array 
        isFalsePos = np.logical_not(targetType) * detected * np.logical_not(classified) 
        
        #updates whether identification is needed 
        targets[6] = np.where(np.logical_or(isMILCO, isFalsePos),True , identified) 
        #array 
        
        #increment number of passes per track and adds time to the clock 
        self.currentPass += 1 
        self. clock += area.length / self.searchSpeed 
        
        return targets 
    
    def mission(self, area, targets): 
        #Checks if the mission possible with this UUV 
        #UUV must be able to make it down and back in one mission 
        possible = (self.searchSpeed * self.searchTime) > (2 * area.length) 
        if not possible: 
            print ("Track too long for this UUV") 
            self.isActive = False #finishes up the the UUV's tasking 
            return 
        

        #determines how many search tracks are in an area 
        totalTracks = int(area.width / self.spacing) + 2 #continues outside of area to ensure all area is covered 
        
        #Is the mission needed 
        self.isActive = (self.currentTrack <= totalTracks) #is the search complete 
        if not self.isActive: 
            return targets 

        #counts number of missions conducted 
        self.numMissions += 1 
        
        #UUV mission 
        
        #transit to search area 
        yCoord = area.refY + self.currentTrack * self.spacing #determines y coordinate based on current search track 
        self.clock += distCalculator(self.originX, self.originY, 0, yCoord) / self.transitSpeed #transiting to search area 
        #deploying UUV 
        self.clock += self.deploy #time to deploy UUV 
        tracksThisMission = 0 #current number of tracks searched 
        
        #conduct search 
        #assuming the operators recover UUV from same side deployed 
        timePerTrack = area.length / self.searchSpeed #time to conduct one search track 
        while (self.missionClock + 2 * timePerTrack) < self.searchTime: #continue if next 2 tracks don't take too long 
            self. missionClock += 2 * timePerTrack #adding the time of 2 tracks 
            tracksThisMission += 2 
        self.clock += self.missionClock #adds mission time to the active clock 
        
        #recovering UUV and returning to ship 
        self.clock += self.recover #time to recover UUV
        yCoord = (tracksThisMission/self.passes) * self.spacing #integer division to determine current track 
        self.missionClock += distCalculator(self.originX, self.originY, 0, yCoord) / self.transitSpeed #transiting back to ship 
        #charging UUV batteries 
        self.missionClock = 0 #assumes UUV and team is ready for another mission immediately after PMA 
        
        
        #Post Mission Analysis 
        for i in range(tracksThisMission): 
            targets = self.searchTrack(area, targets) #doing the PMA for this track 
            
            self.clock += timePerTrack #adding time of PMA for this track 

            #after a track is compelte 
            if self.currentPass == self.passes: 
                self.currentTrack += 1 
                self.currentPass = 0 #which track is the UUV searching 

        return targets 
        
 
    def reacquisitionIdentify(self, area, targets): 
    
        #determines if contacts are in the search area 
        inRangeX = np.logical_and(targets[0] > area.refX, targets[0] < area.refX + 
        area.length) 
        inRangeY = np.logical_and(targets[1] > area.refY, targets[1] < area.refY + 
        area.width) 
        inArea = np.logical_and(inRangeX, inRangeY) 
        #time to conduct R&ID "star pattern" with 20 passes at 5 meters per pass 
        rID = (20 * 5 * 0.0005399568) / self.searchSpeed #0.0005399568 is the conversion from meters to NM 
        
        #finds closest mine for first R&ID mission 
        dist = distCalculator(targets[0], targets[1], self.currentX, self.currentY) 
        #array of distances to all targets 
        dist = np.where(np.logical_and(targets[6], inArea), dist, 10000000) #distance is set to infinity if already identified or out of area 
        closest = np.argmin(dist) #finds the index of the closest mine 
        #Reacquisition and identify next target as long as time remains in the mission 
        while min(dist) < 10000: #if distance is less than infinity 
        
            #if first target on mission 
            if (self.currentX == self.originX) and (self.currentY == self.originY): 
                self.currentX = xRHIB = targets[0][closest] #the UUV and the RHIB is at the location of the closest target 
                self.currentY = yRHIB = targets[1][closest] 
                self.clock += dist[closest] / self.transitSpeed #clock is advanced to account for transit 
                self.clock += self.deploy #advance the clock for deploying UUV 
                self.missionClock += rID #advancing the mission clock for conducting first star pattern 
                
                #marks the target as identified 
                targets[6][closest] = 0 
            else: 
            
                #is there enough time to conduct another R&ID and make it back to RHIB 
                distNextTarg = distCalculator(targets[0][closest], targets[1][closest], 
                self.currentX, self.currentY) #dist to next target 
                distBackToRHIB = distCalculator(targets[0][closest], targets[1][closest], 
                xRHIB, yRHIB) #dist from next targ back to RHIB
                prosecuteTimeNextTarg = (distNextTarg + distBackToRHIB)/self.searchSpeed + rID #time to do next R&ID and drive back to RHIB 
 
                #if there is enough time for next R&ID 
                if (prosecuteTimeNextTarg + self.missionClock) < self.searchTime: 
                    self.currentX = targets[0][closest] #the UUV and the RHIB is at the location of the closest target 
                    self.currentY = targets[1][closest] 
                    self.missionClock += distNextTarg/self.searchSpeed + rID #advancing the mission clock for conducting first star pattern 
                    
                    #mark the target as identified 
                    targets[6][closest] = 0 
                    
                    #if there is not enough time, then return to ship to recharge 
                else: 
                    distToRHIB = distCalculator(self.currentX, self.currentY, xRHIB, 
                    yRHIB) #distance to the RHIB 
                    self.clock += distToRHIB/self.searchSpeed #time to transit back to RHIB 
                    self.clock += self.recover #recovery time of the UUV 
                    distToShip = distCalculator(xRHIB, yRHIB, self.originX, self.originY) 
                    #dist back to HQ ship 
                    self.clock += distToShip / self.transitSpeed #time to transit back to HQ ship 
                    self.currentX = xRHIB = self.originX #update x position once back onboard the HQ ship 
                    self.currentY = yRHIB = self.originY #update y position once back onboard the HQ ship 
                    self.clock += self.missionClock * 2 #advancing clock to account for the mission plus the post mission analysis/battery charge 
                
 
                #recalculate distances 
                dist = distCalculator(targets[0], targets[1], self.currentX, self.currentY) 
                #calculates distance to all mines 
                dist = np.where(np.logical_and(targets[6], inArea), dist, 10000000) 
                #distance is set to infinity if already prosecuted or out of area 
                closest = np.argmin(dist) #finds the index of the closest mine 
                return targets 
 
 
############################## 
# EOD Dive Team Class 
############################## 
class diveTeam(object): 
 
    id = 0 
 
    def __init__(self, speed=25, resupply=5, sortieTime=8, restTime=10, originX=0, 
        originY=0, timeMine=2, timeNonMine=1, isSegment=True, clock=0): 
        #EOD Team Attributes 
        self.speed = speed #transit speed between mines 
        self.speed = float(self.speed) #converts to a float - because not able to initially assign as float 
        self.resupply = resupply #number of explosives per sortie 
        self.sortieTime = float(sortieTime) #max time allowed per sortie 
        self.restTime = float(restTime) #time between sorties 
        self.originX = float(originX) #staging area x-coordinate 
        self.originY = float(originY) #staging area y-coordinate 
        self.timeMine = float(timeMine) #mean prosecution time of a mine 
        self.timeNonMine = float(timeNonMine) #mean prosecution time of a mine 
        self.isSegment = isSegment #is the dive team assigned to a segment of an area 
        self.clock = clock #time of last prosecution 
        diveTeam.id += 1 
        self.id = diveTeam.id
        #Working variables 
        self.currentX = self.originX #current position x-coord 
        self.currentY = self.originY #current position x-coord 
        self.neutOnboard = resupply #remaining bombs on current sortie 
        self.missionClock = 0 #time until next prosecution 
        self.isActive = True 
        
 
    #returns the index of the closest mine shape 
    def nearestObject(self, area, targets): 
        #x[0], y[1], targetType[2], size[3], detected[4], classified[5], identified[6], neutralized[7] 
        #arrays 
        x = targets[0] 
        y = targets[1] 
        targetType = targets[2] 
        classified = targets[5] 
        neutralized = targets[7] 
        remainingMInes = targetType * classified * np.logical_not(neutralized) 
        
        
        #determines if the team is on a mission or back at HQ 
        isResting = (self.currentX==self.originX) and (self.currentY==self.originY) 
        
        #gives commander the option dividing the area into segments 
        #True: assigns segments based on teams id number 
        # -prevents multiple teams from traveling long distances 
        #False: has all teams calculate next closest target based on distance 
        # -near end of scenario, all teams will be going far distances 
        # -longer timeframe 
        # -safer option in case of emergency 
        xRef = self.currentX #if on a mission, then the reference point to its current location 
    
        #if the dive teams are assigned to specific sections 
        if self.isSegment: 
            if isResting: #if at HQ - sets x reference to the segment 
                #the segments are assigned based on number of teams and the dive teams 
                xRef = (self.id - 1)* area.length / diveTeam.id 
        
        #arrays of the distances to all objects based on reference point 
        dist = distCalculator(x, y, xRef, self.currentY) #calculates distance to all mines 
        dist = np.where(remainingMInes, dist, 10000000) #distance is set to remaining mines - infinity if already prosecuted or not a mine 
        
        #finds the closest mine 
        closest = np.argmin(dist) #finds the index of the closest mine 
        if isResting: #recalculates the distance based on current location 
            dist = distCalculator(x, y, self.currentX, self.currentY) 
        distance = dist[closest] #captures the distance to the closest mine 
            
        #does dive team have tasking 
        if sum(remainingMInes)==0: #if not then does nothing 
            self.isActive = False 
        
        return distance, closest #returns a tuple to be used in prosecute function 
        
    
    #function to drive to the next mine and prosecute it 
    def prosecute(self, area, targets): 
    
        #transit to next closest target 
        nearest = self.nearestObject(area, targets) #identifies next nearest object 
        #does nothing if no targets to prosecute 
        if not self.isActive: #if no MILCOS or false positives, then sit and wait 
            return targets 
        
        #if need to return to ship and rest 
        isTimeOut = self.missionClock >= self.sortieTime #is there time left in mission 
        noBombs = self.neutOnboard == 0 #are there any bomblets onboard 
        
        if isTimeOut or noBombs: #return to base if time is out or no more bombs 
            timeToShip = distCalculator(self.currentX, self.currentY, self.originX, 
            self.originY)/self.speed 
            self.missionClock += timeToShip 
            self.currentX = self.originX #changes location to base 
            self.currentY = self.originY 
            self.missionClock += self.restTime #advance the clock to account for rest time 
            self.clock += self.missionClock #adds the time of mission to the team clock 
            
            #rest and resupply 
            self.missionClock = 0 #resets the clock 
            self.neutOnboard = self.resupply #resets number of bomblets 
        
        
        if not self.isActive: #if no MILCOS or false positives, then sit and wait 
            return targets 
        
        distance = nearest[0] #distance to next closest 
        closest = nearest[1] #index of next closest 
        self.missionClock += distance/self.speed #updates the time taken to transit to mine 
        
        #conducts prosecution 
        underwater = np.random.normal(self.timeMine, 0.5) #adds the time taken to prosecute a mine (normally distributed with sigma=.5) 
        self.missionClock += underwater #adds to the clock 
        self.neutOnboard -= 1 #accounts for the used neutralizer 
        #marks the targets as being prosecuted 
        targets[7][closest] = 1 #marks the mine as prosecuted 
        
        #update dive team's position 
        self.currentX = targets[0][closest] 
        self.currentY = targets[1][closest] 
        #adds the time of the mission to the clock 
        self.clock += self.missionClock 
        return targets 
    
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
    numUUVs = 30 #number of UUVs available (must be divisible by 5) 
    numDivers = 10 #number of dive teams 
    QRouteLength = 30 #length of q-route 
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
    
    print(f"{densityNonMines} \ {densityMines} \ {targets}")
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
            uuvs[uuv.id] = uuv(transitSpeed=transitSpeed, deploy=deploy, 
            recover=recover, searchSpeed=searchSpeed, 
            searchTime=searchTime, altitude=altitude, 
            spacing=spacing, passes=passes, sensor=sensor, 
            detRate=np.random.uniform(detRate-.01,detRate+.01), 
            milcoRate=np.random.uniform(milcoRate-.01,milcoRate+.01), 
            nombosRate=np.random.uniform(nombosRate-.01, 
            nombosRate+.01), 
            originX=xHQ, originY=yHQ) 

    #initializes the clock to 0 
    completionTime = 0 
    
    #UUVs search their entire areas 
    for UUV in uuvs: 
        
        #detect, classify and localize 
        while uuvs[UUV].isActive: 
            targets = uuvs[UUV].mission(areas[UUV],targets) 
            
        
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

    print(f"making the dive team {resupply} \ {timeNonMine} \ {timeMine} \ {restTime} \ {sortieTime}")
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
    
    print(f"Done result {totalTargets} \ {numMines} \ {numNonMines} \ {numUndetected} \ {numDetected} \ {numClassified} \ {numMILCOS} \ {numNOMBOS} \ {numNotClassified} \ {numFalseNeg} \ {numFalsePos}")

    return row + [totalTargets, numMines, numNonMines, numUndetected, 
    numDetected, numClassified, numMILCOS, numNOMBOS, 
    numNotClassified, numFalseNeg, numFalsePos, completionTime] 