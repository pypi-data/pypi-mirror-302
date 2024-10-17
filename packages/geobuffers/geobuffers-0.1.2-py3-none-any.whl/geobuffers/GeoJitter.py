from pyproj import Geod
import random

class GeoJitter():

    def __init__(self, max_radius,latlon=False):
        '''
            max_radius (float) : (metres) maxium distance from origin
            latlon (bool) : set to True if lat,lon format desired (default: False)
        '''
        
        self._g = Geod(ellps='clrk66')
        self.max_radius=max_radius
        self.latlon=latlon

    def __call__(self, *input):
        '''
            input (tuple, list, tensor) : geographic coordinates (order set by the latlon propoerty)
        '''
        
        azimuth_angle = random.uniform(0,360)
        radius = random.uniform(0,self.max_radius)
        
        if self.latlon:
            lat, lon = input
            return self._g.fwd(lon, lat, azimuth_angle, radius)[:-1][::-1]
        else:
            lon, lat = input
            return self._g.fwd(lon, lat, azimuth_angle, radius)[:-1]
