import math
class navigate:
    def heading(self,latS,lonS,latM,lonM,headingM,headingS):
        latS = math.radians(42.624914)
        lonS = math.radians(-83.147876)
        latM = math.radians(42.624862)
        lonM = math.radians(-83.147861)
        R = 6371*1000 #radius of the earth in meters
        headingM = math.radians(270)
        headingS = math.radians(100)

        #convert lat lon to xy
        xS = R*math.cos(latS)*math.cos(lonS)
        yS = R*math.cos(latS)*math.sin(lonS)

        xM = R*math.cos(latM)*math.cos(lonM) - xS
        yM = R*math.cos(latM)*math.sin(lonM) - yS

        xS = 0
        yS = 0

        #now we have a local coord system with slave at center
        #now we need to find the point 2 meters behind the master
        #find the line through master along it's orientation
        #we have polar coords, convert to xy with an R of 2 meters

        xGoal = 2*math.cos(-1*headingM)+xM
        yGoal = 2*math.sin(-1*headingM)+yM

        #xGoal and yGoal are 2 meters behind vehicle
        #now we find the line from xS yS to xG yG

        dist = math.sqrt(xGoal*xGoal + yGoal*yGoal)
        #find heading to new goal point
        headingG = math.atan2(yGoal,xGoal)+headingS
        distG = math.sqrt(yGoal*yGoal+xGoal*xGoal)

        self.headingDeg = math.degrees(headingG) #angle to turn
        self.distanceToTravel = distG #distance to travel
