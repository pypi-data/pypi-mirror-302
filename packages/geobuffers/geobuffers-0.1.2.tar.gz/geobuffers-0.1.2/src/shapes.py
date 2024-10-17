'''

    Developed by Mikolaj Czerkawski at ESA Phi Lab

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

'''

from pyproj import Geod
from .utils import *

_g = Geod(ellps='clrk66')

def regpol_shape(lon,
                 lat,
                 n,
                 radius=100,
                 azimuth_angle=0,
                ):
    '''
        lat (float) : latitude value
        lon (float) : longitude value
        radius (float) : (metres) distance from center to corner
    '''
    
    azimuth_angle=process_azimuth(azimuth_angle)
    step_angle = 360/n

    vertices = []
    
    for vertex_idx in range(n):
        vertices.append(_g.fwd(lon, lat, azimuth_angle+step_angle*vertex_idx, radius)[:-1])

    return vertices

def fov_shape(lon,
               lat,
               radius=100,
               azimuth_angle=0,
               fov_angle=45):
    '''
        lat (float) : latitude value
        lon (float) : longitude value
        radius (float) : (metres) line of sight
        azimuth_angle (float or string) : (degrees) azimuth angle of the view
        fov_angle (float) : (degrees) field of view angle
    '''

    azimuth_angle=process_azimuth(azimuth_angle)
        
    los = _g.fwd(lon, lat, azimuth_angle, radius)[:-1]
    # sides
    left =  _g.fwd(lon, lat, azimuth_angle - fov_angle/2, radius)[:-1]
    right =  _g.fwd(lon, lat, azimuth_angle + fov_angle/2, radius)[:-1]

    return (lon,lat), left, los, right