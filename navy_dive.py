from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
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

############################################
class DIVE_Model(BehaviorModelExecutor):
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
    
############################## 
# EOD Dive Team Class 
############################## 
class diveTeam(DIVE_Model): 
 
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