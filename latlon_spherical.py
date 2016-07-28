# -*- coding: utf-8 -*-

from math import radians, degrees, sin, cos, tan, atan2
from math import sqrt, pi, fabs, log
import dms

EARTH_RADIUS = 6371.009 # In KM

class LatLon(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
    
    def toString(self, dms_format, precision):
        """
        Return a string representation of ‘self’ point, formatted as degrees, degrees+minutes, 
        or degrees+minutes+seconds.
        
        Arguments :
            dms_format -- {string} -- Return value format as 'd', 'dm', 'dms' for deg, deg+min, deg+min+sec (default=dms)
            precision -- {int} -- Number of decimal to use (default: 1 for dms, 2 for dm, 4 for d).
            
        Example:
            > point = LatLon(51.521470, -0.138833)
            > point.toString('d', 6)
            > 51.521470°N, 000.138833°W
        """
        
        return dms.toLat(self.lat, dms_format, precision) + ', ' + dms.toLon(self.lon, dms_format, precision)
        
    
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
        Return the midpoint between 'self' point and the supplied point.
        
        Arguments:
            point -- {LatLon} -- Latitude/longitude of destination point.
            return -- {LatLon} -- Midpoint between 'self' point and the supplied point.
            
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
    def intermediatePointTo(self, point, fraction):
        """
        Return the point at given fraction between ‘this’ point and specified point.
        
        Arguments:
            point -- {LatLon} -- Latitude/longitude of destination point.
            fraction -- {float} -- Fraction between the two points (0 = this point, 1 = specified point).
        Return:
            {LatLon} -- Midpoint between 'self' point and the supplied point.
        
        Example:
            > p1 = LatLon(52.205, 0.119)
            > p2 = new LatLon(48.857, 2.351)
            > mid_point = p1.intermediatePointTo(p2, 0.25)  # 51.3721°N, 000.7073°E
        """
        
        if not isinstance(point, LatLon):
                raise TypeError('point is not LatLon object')
        
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(point.lat)
        lon2 = radians(point.lon)
        
        cos_lat1  = cos(lat1)
        cos_lon1 = cos(lon1)
        sin_lat1 = sin(lat1)
        sin_lon1 = sin(lon1)
        cos_lat2 = cos(lat2)
        cos_lon2 = cos(lon2)
        sin_lat2 = sin(lat2)
        sin_lon2 = sin(lon2)
        
        # Distance between points
        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1
        a = sin(delta_lat/2) * sin(delta_lat/2) + \
               cos(lat1) * cos(lat2) * \
               sin(delta_lon/2) * sin(delta_lon/2)
        distance = 2 * atan2(sqrt(a), sqrt(1-a))
        
        A = sin((1-fraction) * distance) / sin(distance)
        B = sin(fraction * distance) / sin(distance)
        
        x = A * cos_lat1 * cos_lon1 + B * cos_lat2 * cos_lon2
        y = A * cos_lat1 * sin_lon1 + B * cos_lat2 * sin_lon2
        z = A * sin_lat1 + B * sin_lat2
        
        lat3 = atan2(z, sqrt(x**2 + y**2))
        lon3 = atan2(y, x)

        return LatLon(degrees(lat3), (degrees(lon3) + 540)%360-180) # Normalise to -180..+180

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
