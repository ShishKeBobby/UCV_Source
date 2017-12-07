import math
import haversine

class halfversine:
    def calcHeading(self,lat,lon,plat,plon):
        #shift to radians
        self.lat = math.radians(lat)
        self.lon = math.radians(lon)
        self.plat = math.radians(plat)
        self.plon = math.radians(plon)
        self.currentPos = (self.lat, self.lon)
        self.previousPos = (self.plat, self.plon)
        self.distance = haversine(self.currentPos,self.previousPos)*1000 #convert Km to m


