import numpy as np 
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

         # Add a print statement to check the values of targets[1] and targets[3]
        # print(f"Value of targets[1]: {targets[1]}, Value of targets[3]: {targets[3]}")
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
        inRangeX = np.logical_and(targets[0] > area.refX, targets[0] < area.refX + area.length) 
        inRangeY = np.logical_and(targets[1] > area.refY, targets[1] < area.refY + area.width) 
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
 