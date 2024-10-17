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

from .shapes import *
from shapely.geometry import Polygon


def triangle(point,
           radius=100,
           azimuth_angle=45
          ):
    '''
        Generate a triangle around a point
    '''

    return regpol(point, 3, radius, azimuth_angle)

def square(point,
           radius=100,
           azimuth_angle=45
          ):
    '''
        Generate a square around a point
    '''

    return regpol(point, 4, radius, azimuth_angle)

def hexagon(point,
            radius=100,
            azimuth_angle=0,
           ):
    '''
        Generate a hexagon around a point
    '''
    
    return regpol(point, 6, radius, azimuth_angle)

def regpol(point,
           n,
           radius=100,
           azimuth_angle=0,
           ):
    '''
        Generate a regular polygon around a point

        radius (m) : distance from center to vertex
        azimuth_angle (deg) : rotation in degrees (offset of the first vertex from north-oriented azimuth)
    '''
    
    assert n > 2
    
    lon,lat=point.x,point.y

    reg_points = regpol_shape(lon,
                              lat,
                              n,
                              radius,
                              azimuth_angle
                              )

    return Polygon([*reg_points, reg_points[0]])

def fov(point,
        radius=100,
        azimuth_angle=0,
        fov_angle=45):
    '''
        Generate a field-of-view around a point

        radius (m) : distance from center to vertex
        azimuth_angle (deg) : view azimuth
        fov_angle (deg)  : width of the view in degrees
    '''

    lon,lat=point.x, point.y
                    
    fov_points = fov_shape(lon,lat,radius,azimuth_angle,fov_angle)
    
    return Polygon([*fov_points, fov_points[0]])
