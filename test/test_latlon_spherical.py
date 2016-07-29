import unittest
from latlon_spherical import LatLon, EARTH_RADIUS
import dms

class GeodesicsTestCase(unittest.TestCase):
    def setUp(self):
        self.cambg = LatLon(52.205, 0.119)
        self.paris = LatLon(48.857, 2.351)
        self.london = LatLon(51.521470, -0.138833)
        self.origin = LatLon(0, 0)
        
    def test_tostring_d(self):
        p = self.london.toString('d', 6)
        self.assertEqual(p, '51.521470°N, 0.138833°W')
        
    def test_distance(self):
        d = self.cambg.distanceTo(self.paris)
        self.assertEqual("{:.1f}".format(d), "404.3")
        
    def test_distance_miles(self):
        d = self.cambg.distanceTo(self.paris, 3959)
        self.assertEqual("{:.1f}".format(d) , "251.2")
        
    def test_initial_bearing_to(self):
        b = self.cambg.bearingTo(self.paris)
        self.assertEqual("{:.1f}".format(b), "156.2")
    
    def test_final_bearing_to(self):
        b = self.cambg.finalBearingTo(self.paris)
        self.assertEqual("{:.1f}".format(b), "157.9")

    def test_midpoint_to(self):
        p = self.cambg.midpointTo(self.paris)
        self.assertEqual(p.toString('d'), '50.5363°N, 1.2746°E')
    
    def test_intermediatepoint_to(self):
        p = self.cambg.intermediatePointTo(self.paris, 0.25)
        self.assertEqual(p.toString('d'), '51.3721°N, 0.7073°E')
        
    def test_destination_point(self):
        bradwell = LatLon(51.4778, -0.0015)
        distance = 7.794
        bearing = 300.7
        p = bradwell.destinationPoint(distance, bearing)
        self.assertEqual(p.toString('d'), '51.5135°N, 0.0983°W')        
        
    def test_intersection(self):
        stn = LatLon(51.8853, 0.2545)   # Stansted airport (UK)
        cdg = LatLon(49.0034, 2.5735) # Charles de Gaulle airport (FR)
        p = LatLon.intersection(stn, 108.547, cdg, 32.435)
        self.assertEqual(p.toString('d'), '50.9078°N, 4.5084°E')        
        
    def test_crosstrack_distance(self):
        p0 = LatLon(53.2611, -0.7972)
        p1 = LatLon(53.3206, -1.7297)
        p2 = LatLon(53.1887,  0.1334)
        d = p0.crossTrackDistanceTo(p1, p2, EARTH_RADIUS*1000)        
        self.assertEqual("{:.2f}".format(d), "-307.55")
        
    def test_maxlatitude_0(self):
        lat = self.origin.maxLatitude(0)
        self.assertEqual(lat, 90)
    
    def test_maxlatitude_1(self):
        lat = self.origin.maxLatitude(1)
        self.assertEqual("{:.0f}".format(lat), '89')
        
    def test_maxlatitude_90(self):
        lat = self.origin.maxLatitude(90)
        self.assertEqual(lat, 0)
        
    def test_rhumb_distance(self):
        d = self.cambg.rhumbDistanceTo(self.paris)
        self.assertEqual(("{:.1f}".format(d)), "404.3")
    
if __name__ == '__main__':
    unittest.main()