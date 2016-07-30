# geodesy
Chris Veness Geodesy library Python's implementation

Original Javascript library can be found here :
https://github.com/chrisveness/geodesy

---------
FEATURES:
---------
For now, only one of the module is implemented : *latlon-spherical*
This module is a library of geodesy functions for operations on a spherical earth model.

Class LatLon: Represents a point on the earth's surface at the specified latitude / longitude.
- LatLon.distanceTo: returns the distance from this point to destination point (using haversine formula).
- LatLon.bearingTo: returns the (initial) bearing from this point to destination point.
- LatLon.finalBearingTo: returns final bearing arriving at destination destination point from this point.
- LatLon.midpointTo: returns the midpoint between this point and the supplied point.
- LatLon.intermediatePointTo: returns the point at given fraction between this point and specified point.
- LatLon.destinationPoint: returns the destination point from this point having travelled the given distance on the given initial bearing.
- LatLon.intersection: returns the point of intersection of two paths defined by point and bearing.
- LatLon.crossTrackDistanceTo: returns (signed) distance from this point to great circle defined by start-point and end-point.
- LatLon.maxLatitude: returns maximum latitude reached when travelling on a great circle on given bearing from this point.
- LatLon.crossingParallels: returns the pair of meridians at which a great circle defined by two points crosses the given latitude.
- LatLon.rhumbDistanceTo: returns the distance travelling from this point to destination point along a rhumb line.
- LatLon.rhumbBearingTo: returns the bearing from this point to destination point along a rhumb line.
- LatLon.rhumbDestinationPoint: returns the destination point having travelled along a rhumb line from this point the given distance on the  given bearing.
- LatLon.rhumbMidpointTo: returns the loxodromic midpoint (along a rhumb line) between this point and second point.


-----
TODO:
-----
Implement *latlon-vincenty* module
Implement *latlon-ellipsoidal* module
Implement *latlon-vectors* module
