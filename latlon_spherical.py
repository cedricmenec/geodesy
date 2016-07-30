# -*- coding: utf-8 -*-

from math import radians, degrees, sin, cos, tan, atan2, asin, acos
from math import sqrt, pi, fabs, log, isnan, isfinite
import geodesy.dms as dms

EARTH_RADIUS = 6371.009 # In KM

class LatLon(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
    
    def toString(self, dms_format=None, precision=None):
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
        lat2 = radians(point.lat)
        delta_lon = radians(point.lon - self.lon)
        
        Bx = cos(lat2) * cos(delta_lon)
        By = cos(lat2) * sin(delta_lon)
        
        x = sqrt( (cos(lat1) + Bx ) * (cos(lat1) + Bx) + By*By)
        y = sin(lat1) + sin(lat2)
        lat3 = atan2(y, x)
        lon3 = lon1 + atan2( By, cos(lat1) + Bx )
        
        latlon = LatLon(degrees(lat3), (degrees(lon3)+540)%360-180) #Normalise to -180..+180°
        return latlon

    
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


    def destinationPoint(self, distance, bearing, radius=None):
        """
        Return the destination point from ‘self’ point having travelled the given distance on the
        given initial bearing (bearing normally varies around path followed).
        
        Arguments:
            distance -- {int | float} -- Distance travelled, in same units as earth radius (default: kilometres).
            bearing -- {int | float} -- Initial bearing in degrees from north.
            radius -- {int | float} -- (Mean) radius of earth (defaults to radius in kilometres).
            
        Formula:
           φ2 = asin( sin φ1 ⋅ cos δ + cos φ1 ⋅ sin δ ⋅ cos θ )
	       λ2 = λ1 + atan2( sin θ ⋅ sin δ ⋅ cos φ1, cos δ − sin φ1 ⋅ sin φ2 )
           where : φ is latitude, λ is longitude, θ is the bearing (clockwise from north), 
                         δ is the angular distance d/R; d being the distance travelled, R the earth’s radius
            
        Examples:
            > p1 = LatLon(51.4778, -0.0015)
            > p2 = p1.destinationPoint(7794, 300.7);    # 51.5135°N, 000.0983°W
        
        References : 
            http://williams.best.vwh.net/avform.htm#LL
        """
        
        if radius is None:
            radius = EARTH_RADIUS
        else:
            radius = float(radius)
        
        angular_distance = float(distance) / radius
        bearing = radians(float(bearing))
        
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        
        lat2 = asin(sin(lat1) * cos(angular_distance) + cos(lat1) * sin(angular_distance) * cos(bearing))
        x = cos(angular_distance) - sin(lat1) * sin(lat2)
        y = sin(bearing) * sin(angular_distance) * cos(lat1)
        lon2 = lon1 + atan2(y, x)
        
        return LatLon(degrees(lat2), (degrees(lon2) + 540)%360-180)  #normalise to −180..+180°
        
        
    def intersection(point1, bearing1, point2, bearing2):
        """
        Return the point of intersection of two paths defined by point and bearing.
        
        Arguments:
            point1 -- {LatLon} -- First point.
            bearing1 -- {flot | int} -- Initial bearing from first point (in degrees).
            point2 -- {LatLon} -- Second point.
            bearing2 -- {float | int} -- Initial bearing of second point (in degrees).
            
        Example:
            > p1 = LatLon(51.8853, 0.2545)
            > brng1 = 108.547
            > p2 = LatLon(49.0034, 2.5735)
            > brng2 = 32.435
            > pInt = interseection(p1, brng1, p2, brng2)   # 50.9078°N, 004.5084°E
        
        References:
            http://williams.best.vwh.net/avform.htm#Intersection
        """
        
        if not isinstance(point1, LatLon):
                raise TypeError('point1 is not LatLon object')
        if not isinstance(point2, LatLon):
                raise TypeError('point2 is not LatLon object')
                
        lat1 = radians(point1.lat)
        lon1 = radians(point1.lon)
        lat2 = radians(point2.lat)
        lon2 = radians(point2.lon)    
        bearing_13 = radians(float(bearing1))
        bearing_23 = radians(float(bearing2))
        
        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1
        
        # Course from 1 to 2 (angular distance in radians -> adist)
        adist_12 = 2 * asin( sqrt( sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)**2 ))
        if adist_12 == 0:
            return None
                
        # Initial/final bearings between points 
        initial_bearing = acos( ( sin(lat2) - sin(lat1)*cos(adist_12) ) / (sin(adist_12)*cos(lat1)) )
        # Protect against rounding
        if (isnan(initial_bearing)):
            initial_bearing = 0
        final_bearing = acos( (sin(lat1) - sin(lat2)*cos(adist_12) ) / (sin(adist_12)*cos(lat2)) )
        
        if sin(delta_lon) > 0:
            bearing_12 = initial_bearing
        else:
            bearing_12 = 2*pi - initial_bearing
        
        if sin(delta_lon) > 0:
            bearing_21 = 2*pi - final_bearing
        else:
            bearing_21 = final_bearing
        
        a1 = (bearing_13 - bearing_12 + pi) % (2*pi) - pi   # Angle 2-1-3
        a2 = (bearing_21 - bearing_23 + pi) % (2*pi) - pi   # Angle 1-2-3
        
        # Check infinite intersections
        if (sin(a1) == 0) and (sin(a2) == 0):
            return None
        
        # Check ambiguous intersection
        if (sin(a1)*sin(a2) < 0):
            return None
        
        a3 = acos( -cos(a1)*cos(a2) + sin(a1)*sin(a2)*cos(adist_12) )
        adist_13 = atan2( sin(adist_12)*sin(a1)*sin(a2), cos(a2) + cos(a1)*cos(a3) )
        
        lat3 = asin( sin(lat1)*cos(adist_13) + cos(lat1)*sin(adist_13)*cos(bearing_13) )
        delta_lon_13 = atan2( sin(bearing_13)*sin(adist_13)*cos(lat1), cos(adist_13) - sin(lat1)*sin(lat3) )
        lon3 = lon1 + delta_lon_13

        return LatLon(degrees(lat3), (degrees(lon3)+540) % 360 - 180)   # Normalise to -180..+180
        
    def crossTrackDistanceTo(self, path_start, path_end, radius=None):
        """
        Returns (signed) distance from ‘self’ point to great circle defined by start_point and end_point.
        
        Arguments:
            path_start -- {LatLon} -- Start point of great circle path.
            path_end -- {LatLon} -- End point of great circle path.
            radius -- {int | float} -- (Mean) radius of earth (defaults to EARTH_RADIUS in kilometres).
        Return:
            Distance to great circle (-ve if to left, +ve if to right of path)
            
        Example:
            pCurrent = LatLon(53.2611, -0.7972)
            p1 = LatLon(53.3206, -1.7297)
            p2 = LatLon(53.1887,  0.1334)
            d = pCurrent.crossTrackDistanceTo(p1, p2)   # -307.5 m
        """
        
        if not isinstance(path_start, LatLon):
            raise TypeError('path_start is not LatLon object')
        if not isinstance(path_end, LatLon):
            raise TypeError('path_end is not LatLon object')
            
        if radius is None:
            radius = EARTH_RADIUS
        else:
            radius = float(radius)
        
        adist_13 = path_start.distanceTo(self, radius) / radius
        bearing_13 = radians(path_start.bearingTo(self))
        bearing_12 = radians(path_start.bearingTo(path_end))
        
        return asin( sin(adist_13) * sin(bearing_13-bearing_12) ) * radius
        
    def maxLatitude(self, bearing):
        """
        Return maximum latitude reached when travelling on a great circle on given bearing from 'self'
        point. 
        Negate the result for the minimum latitude (in the Southern hemisphere).
        
        Arguments:
            bearing -- {int | float} -- Initial bearing (in degrees)
        Return:
            {float} -- Maximum latitude in degrees
            
        Formula (Clairaut): 
            φmax = acos( | sin θ ⋅ cos φ | )
            
        Example: 
            > p = LatLon(0,0)
            > p.maxLatitude(1)  # 89
        """
        
        bearing = radians(bearing)
        lat = radians(self.lat)
        lat_max = acos( fabs( sin(bearing)*cos(lat) ) )
        return degrees(lat_max)
        
    def crossingParallels(point1, point2, latitude):
        """
         Return the pair of meridians at which a great circle defined by two points crosses the given latitude. 
         If the great circle doesn't reach the given latitude, None is returned.
         
         Arguments:
            point1 -- {LatLon} -- First point defining great circle.
            point2 -- {LatLon} -- Second point defining great circle.
            latitude -- { float | int} -- Latitude crossings are to be determined for.
        Return:
            {dictionary | None} -- Dictionary containing (lon1, lon2) or None if given latitude not reached.
            
        Example:
            > parallels = LatLon.crossingParallels(LatLon(0,0), LatLon(60,30), 30)
            > parallels_1 = LatLon(30, parallels["lon1"])
            > parallels_2 = LatLon(30, parallels["lon2"])
        """
        
        lat = radians(latitude)
        lat1 = radians(point1.lat)
        lon1 = radians(point1.lon)
        lat2 = radians(point2.lat)
        lon2 = radians(point2.lon)
        
        delta_lon = lon2 - lon1
        
        x = sin(lat1) * cos(lat2) * cos(lat) * sin(delta_lon)
        y = sin(lat1) * cos(lat2) * cos(lat) * cos (delta_lon) - cos(lat1) * sin(lat2) * cos(lat)
        z = cos(lat1) * cos(lat2) * sin(lat) * sin(delta_lon)

        if (z**2 > x**2 +y**2):
            return None     #  great circle doesn't reach latitude
        
        # longitude at max latitude
        lon_max = atan2(-y, x)      
        
        # Δλ from λm to intersection points
        delta_lon_i = acos(z / sqrt(x**2 + y**2))
        
        lon_i1 = lon1 + lon_max - delta_lon_i
        lon_i2 = lon1 + lon_max + delta_lon_i
        
        return {
            "lon1": (degrees(lon_i1)+540)%360-180,    # Normalise to -180..+180
            "lon2": (degrees(lon_i2)+540)%360-180
        }
    
    
    def rhumbDistanceTo(self, point, radius=None):
        """
        Return the distance travelling from ‘self’ point to destination point along a rhumb line.
        
        Arguments: 
            point -- {LatLon} -- Latitude/longitude of destination point.
            radius -- {float | int} -- (Mean) radius of earth (defaults to EARTH_RADIUS in kilometres).
        Return:
            {float} -- Distance between this point and destination point (same units as radius - default is kms).
            
        Reference:
            http://williams.best.vwh.net/avform.htm#Rhumb
        
        Example: 
            > p1 = LatLon(52.205, 0.119)
            > p2 = LatLon(48.857, 2.351)
            > p1.rhumbDistanceTo(p2)    # 404.3 (kms)
        """
        
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
    
    
    def rhumbBearingTo(self, point):
        """
        Return the bearing from ‘self’ point to destination point along a rhumb line.
        
        Arguments:
            point -- {LatLon} -- Latitude/longitude of destination point.
        Return:
            {float} -- Bearing in degrees from north.
        
        Formula:
           Δψ = ln( tan(π/4 + φ2/2) / tan(π/4 + φ1/2) ) 	(‘projected’ latitude difference)
	       θ = atan2(Δλ, Δψ) 	
                where φ is latitude, λ is longitude, Δλ is taking shortest route (<180°), 
                R is the earth’s radius, ln is natural log
                
        Example:
            > p1 = LatLon(51.127, 1.338)
            > p2 = new LatLon(50.964, 1.853)    
            > b = p1.rhumbBearingTo(p2)     # 116.7°
        """
        
        if not isinstance(point, LatLon):
            raise TypeError('point is not LatLon object')
        
        lat1 = radians(self.lat)
        lat2 = radians(point.lat)

        delta_lon = radians(point.lon - self.lon)
        
        # if delta_lon over 180° take shorter rhumb line across the anti-meridian        
        if fabs(delta_lon) > pi:
            if delta_lon > 0:
                delta_lon =  -(2*pi - delta_lon)
            else:
                delta_lon = 2*pi + delta_lon
        
        delta_mercator_dist = log( tan(lat2/2 + pi/4) / tan(lat1/2 + pi/4) )
        bearing = atan2(delta_lon, delta_mercator_dist)
        
        return (degrees(bearing)+360) % 360   # Normalise 0..+360
        
        
    def rhumbDestinationPoint(self, distance, bearing, radius=None):
        """
        Return the destination point having travelled along a rhumb line from ‘self’ 
        point the given distance on the  given bearing.

        Arguments:
            distance -- {float | int} -- Distance travelled, in same units as earth radius (default: kilometres).
            bearing -- {float | int} -- Bearing in degrees from north.
            radius -- {float | int} -- (Mean) radius of earth (defaults to EARTH_RADIUS in kilometres).
        Return:
            {LatLon} -- Destination point.

        Example:
            > p = LatLon(51.127, 1.338)
            > distance = 40.31    # In kilometres
            > bearing = 116.7     # In degrees
            > p.rhumbDestinationPoint(distance, bearing)    # 50.9641°N, 1.8540°E
        """

        if radius is None:
            radius = EARTH_RADIUS
        else:
            radius = float(radius)

        lat1 = radians(self.lat)
        lon1 = radians(self.lon)

        angular_distance = float(distance) / radius
        bearing = radians(bearing)

        delta_lat = angular_distance * cos(bearing)
        lat2 = lat1 + delta_lat

        # check for some daft bugger going past the pole, normalise latitude if so
        if fabs(lat2) > pi/2:
            if lat2 > 0:
                lat2 = pi-lat2
            else:
                lat2 = -pi-lat2

        delta_mercator_distance = log( tan(lat2/2 + pi/4) / tan(lat1/2 + pi/4) ) 
        # E-W course becomes ill-conditioned with 0/0
        if fabs(delta_mercator_distance > 10e-12):
            q = delta_lat / delta_mercator_distance
        else:
            q = cos(lat1)

        delta_lon = angular_distance * sin(bearing) / q
        lon2 = lon1 + delta_lon

        return LatLon(degrees(lat2), (degrees(lon2)+540)%360-180)   # normalise to -180..+180°

    
    def rhumbMidpointTo(self, point):
        """
        Return the loxodromic midpoint (along a rhumb line) between ‘self’ point and second point.
        
        Arguments:
            point -- {LatLon} -- Latitude/longitude of second point.
        Return:
            {LatLon} -- Midpoint between this point and second point.
        
        Example:
            > p1 = LatLon(51.127, 1.338)
            > p2 = LatLon(50.964, 1.853)
            > pMid = p1.rhumbMidpointTo(p2)     # 51.0455°N, 001.5957°E
        """
        
        if not isinstance(point, LatLon):
            raise TypeError('point is not LatLon object')
            
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(point.lat)
        lon2 = radians(point.lon)
        
        if fabs(lon2-lon1) > pi:
            lon1 += 2*pi   # crossing anti-meridian
        
        delta_lon = lon2 - lon1
        
        lat3 = (lat1+lat2) / 2
        
        f1 = tan(pi/4 + lat1/2)
        f2 = tan(pi/4 + lat2/2)
        f3 = tan(pi/4 + lat3/2)            
        lon3 = (  delta_lon*log(f3) + lon1*log(f2) - lon2*log(f1) ) / log(f2/f1)
        
        # parallel of latitude
        if isfinite(lon3):
            lon3 = (lon1+lon2)/2
            
        return LatLon(degrees(lat3), (degrees(lon3)+540)%360-180)   # normalise to −180..+180°
        