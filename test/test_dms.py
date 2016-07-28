import unittest
import dms

class DmsTestCase(unittest.TestCase):
    """
    Unit tests for dms module.
    """
    
    def test_parsedms_decimal_float(self):
        d = dms.parseDMS(48.857000) # Paris latitude (48°51'25.2"N)
        self.assertEqual(d, 48.857000)        
        
    def test_parsedms_decimal_string_negative(self):
        d = dms.parseDMS("-48.857000") 
        self.assertEqual(d, -48.857000)        
        
    def test_parsedms_dms(self):
        d = dms.parseDMS("48°51'25.2'N") 
        self.assertEqual(d, 48.857000)
        
    def test_parsedms_dms_without_seconds(self):
        d = dms.parseDMS("48°51'") 
        self.assertEqual(d, 48.85)
    
    def test_parsedms_dms_without_minutes(self):
        d = dms.parseDMS("48°") 
        self.assertEqual(d, 48.0)
        
    def test_parsedms_dms_south(self):
        d = dms.parseDMS("48°51'25.2'S") 
        self.assertEqual(d, -48.857000)
        
    def test_parsedms_dms_negative(self):
        d = dms.parseDMS("-48°51'25.2'") 
        self.assertEqual(d, -48.857000)
        
    def test_todms(self):
        dms_result = dms.toDMS(-48.857000) 
        self.assertEqual(dms_result, "48°51'25.2\"")
        
    def test_todms_dm(self):
        dms_result = dms.toDMS(48.857000, "dm") 
        self.assertEqual(dms_result, "48°51.42'")
    
    def test_todms_dm_precision1(self):
        dms_result = dms.toDMS(48.857000, "dm", 1) 
        self.assertEqual(dms_result, "48°51.4'")
    
    def test_todms_d(self):
        dms_result = dms.toDMS(48.857000, "d") 
        self.assertEqual(dms_result, "48.8569°")
    
    def test_todms_d_precision2(self):
        dms_result = dms.toDMS(48.857000, "d", 2) 
        self.assertEqual(dms_result, "48.85°")

    def test_tolat(self):
        lat = dms.toLat(48.857000)
        self. assertEqual(lat, "48°51'25.2\"N")
        
    def test_tolat_south(self):
        lat = dms.toLat(-48.857000)
        self. assertEqual(lat, "48°51'25.2\"S")
        
    def test_tolon(self):
        lon = dms.toLon(0.138833)
        self. assertEqual(lon, "0°08'19.8\"E")
        
    def test_tolon_west(self):
        lon = dms.toLon(-0.138833)
        self. assertEqual(lon, "0°08'19.8\"W")
        
    def test_tobearing(self):
        b = dms.toBearing(-0.138833, "dm", 1)
        self. assertEqual(b, "359°51.7'")
        
    def test_compass_point_precision1(self):
        p = dms.compassPoint(30, 1)
        self. assertEqual(p, "N")

    def test_compass_point_precision2(self):
        p = dms.compassPoint(30, 2)
        self. assertEqual(p, "NE")
    
    def test_compass_point_precision3(self):
        # Default precision is 3
        p = dms.compassPoint(30)
        self. assertEqual(p, "NNE")
    
    def test_compass_point_precision4_error(self):        
        try:
            p = dms.compassPoint(30, 4)
        except ValueError:
            self. assertTrue(True)
            return
        self.assertTrue(False)