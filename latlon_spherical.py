# -*- coding: utf-8 -*-

from math import radians, degrees, sin, cos, tan, atan2
from math import sqrt, pi, fabs, log
import dms

EARTH_RADIUS = 6371.009 # In KM

class LatLon(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
    
    def toString(dms_format, dp):
        return dms.toLat(this.lat, format, dp) + ', ' + Dms.toLon(this.lon, format, dp);
        
        
    def distanceTo(self, point, radius=None):
        if not isinstance(point, LatLon):
            raise TypeError('point is not LatLon object')
            
        if radius is None:
            radius = EARTH_RADIUS
        else:
            radius = float(radius)    
        
        R = radius
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(point.lat)
        lon2 = radians(point.lon)
        
        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1
        
        a = sin(delta_lat/2) * sin(delta_lat/2) + \
               cos(lat1) * cos(lat2) * \
               sin(delta_lon/2) * sin(delta_lon/2)
        
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = R * c
        return d

    # see http://mathforum.org/library/drmath/view/55417.html    
    def bearingTo(self, point):
        if not isinstance(point, LatLon):
                raise TypeError('point is not LatLon object')

        lat1 = radians(self.lat)
        lat2 = radians(point.lat)
        delta_lon = radians(point.lon - self.lon)

        y = sin(delta_lon) * cos(lat2)
        x = cos(lat1) * sin(lat2) - \
              sin(lat1) * cos(lat2) * cos(delta_lon)
        b = atan2(y,x)
        return (degrees(b) + 360) % 360
        
    def finalBearingTo(self, point):
        # Get initial bearing from destination point to this point & reverse it by adding 180°
        return (point.bearingTo(self) + 180) % 360
    
    
    def midpointTo(self, point):
        """
        Formula : 
            Bx = cos φ2 ⋅ cos Δλ
            By = cos φ2 ⋅ sin Δλ
            φm = atan2( sin φ1 + sin φ2, √(cos φ1 + Bx)² + By² )
            λm = λ1 + atan2(By, cos(φ1)+Bx) 
        
         see http://mathforum.org/library/drmath/view/51822.html for derivation
        """
        if not isinstance(point, LatLon):
                raise TypeError('point is not LatLon object')
                
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        delta_lon = radians(point.lon - self.lon)
        
        Bx = cos(lat2) * cos(delta_lon)
        By = cos(lat2) * sin(delta_lon)
        
        x = sqrt( (cos(lat1) + Bx ) * (cos(lat1) + Bx) + By*By)
        y = sin(lat1) + sin(lat2)
        lat3 = atan2(y, x)
        lon3 = lon1 + atan2( By, cos(lat1) + Bx )
        
        latlon = LatLon(degrees(lat3), (degrees(lon3)+540)%360-180) #Normalise to -180..+180°
        return latlon
    
    
    # see http://williams.best.vwh.net/avform.htm#Rhumb
    def rhumbDistanceTo(self, point, radius=None):
        if not isinstance(point, LatLon):
                raise TypeError('point is not LatLon object')

        if radius is None:
            radius = EARTH_RADIUS
        else:
            radius = float(radius)    
            
        R = radius
        lat1 = radians(self.lat)
        lat2 = radians(point.lat)
        delta_lat = lat2 - lat1
        delta_lon = radians(fabs(point.lon - self.lon))
    
        # if delta_lon over 180°, take shorter rhumb line across the anti-meridian:
        if fabs(delta_lon) > pi:
            if(delta_lon > 0):
                delta_lon = -(2*pi - delta_lon)
            else:
                delta_lon = 2*pi + delta_lon

        # on Mercator projection, longitude distances shrink by latitude; q is the 'stretch factor'
        # q becomes ill-conditioned along E-W line (0/0); use empirical tolerance to avoid it
        z = tan(lat2/2 + pi/4) / tan(lat1/2 + pi/4)
        if ( z > 0):
            delta_mercator_distance = log( z )
            if fabs(delta_mercator_distance) > 10e-12:
                q = delta_lat/delta_mercator_distance
            else:
                q = cos(lat1)
        else:
            q = cos(lat1)

        # Distance is pythagoras on 'stretched' Mercator projection
        # Angular distance, in radians
        angular_distance = sqrt(delta_lat*delta_lat + q*q*delta_lon*delta_lon)
        d = angular_distance * R
        return d
