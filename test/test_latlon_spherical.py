import unittest
from latlon_spherical import LatLon

class GeodesicsTestCase(unittest.TestCase):
    def setUp(self):
        self.cambg = LatLon(52.205, 0.119)
        self.paris = LatLon(48.857, 2.351);
        
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
    
    def test_rhumb_distance(self):
        d = self.cambg.rhumbDistanceTo(self.paris)
        self.assertEqual(("{:.1f}".format(d)), "404.3")
    
if __name__ == '__main__':
    unittest.main()