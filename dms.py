from math import isfinite, isnan, floor, fabs
import re

# note Unicode Degree = U+00B0. Prime = U+2032, Double prime = U+2033
DEGREE_CHAR = '°'
MINUTE_CHAR = "'"
SECONDE_CHAR = '"'
SEPARATOR = ''
NONE_VALUE_CHAR = "–"


def parseDMS(dmsStr):
    """
    Parse string representing degrees/minutes/seconds (aka DMS) into numeric degrees.
    Return a float representing decimal degrees.
    
    Arguments :
    dmsStr {string | float} -- Decimal degrees or deg/min/sec in variety of formats.
    
    Allow signed decimal degrees (eg: -0.13) or deg-min-sec optionally suffixed by compass direction (NSEW).
    A variety of separators are accepted (eg 3° 37' 09"W).
    Seconds and minutes may be omitted.  
    
    Example :
        > dms.parseDMS("48°51'25.2'N")         
        > 48.857000
    """
    
    # check for signed decimal degrees without NSEW compass direction, if so return it directly
    if isinstance(dmsStr, float) and isfinite(dmsStr):
            return float(dmsStr)

    tmpStr = str(dmsStr).strip()
    # Strip off any sign at the beginning of the string
    tmpStr = tmpStr.replace('^-', '')
    # Strip off any compass direction at the end of the string
    tmpStr = tmpStr.replace('[NSEW]$]', '', re.IGNORECASE)
    # Split out separate d/m/s (degree / minute / second)
    dms = re.split('[^0-9.]+', tmpStr)
    
    # Remove first list element if it contains empty string (positive or negative sign)
    if dms[0] == '':
        dms = dms[1:]
        
    # Remove last list element if it contains empty string (compass direction)
    if dms[len(dms)-1] == '':
        dms = dms[:len(dms)-1]
    
    if (dms == ''):
        return None; 
    
    # Convert to decimal degrees
    dms_length = len(dms)
    if dms_length == 3: # 3-part result d/m/s
        deg = float(dms[0])/1 + float(dms[1])/60 + float(dms[2])/3600
    elif dms_length == 2: # 2-part result d/m
        deg = float(dms[0])/1 + float(dms[1])/60
    elif dms_length == 1: # Only d (degrees)
        deg = float(dms[0])
    else:
        return None
    
    m = re.match('^-.*|.*[WS]$', dmsStr.strip(), re.IGNORECASE)
    if m is not None:
        deg = -deg
        
    return float(deg)


def toDMS(deg, dms_format=None, precision=None):
    """
    Converts decimal degrees to deg/min/sec format.
    Return a deg/min/sec string.
    
    Degree, prime and double-prime symbols are added.
    But sign (+|-) is discarded, though no compass direction (NESW) is added.

    Arguments :
    deg -- {float | int} -- Degrees to be formatted as specified.
    dms_format -- {string} -- Return value format as 'd', 'dm', 'dms' for deg, deg+min, deg+min+sec (default=dms)
    precision -- {int} -- Number of decimal to use (default: 1 for dms, 2 for dm, 4 for d).
    
    Example :
    > dms.toDMS(-48.857000)
    > 48°51'25.2''
    > dms.toDMS(48.857000, "d", 2)
    > 48.86°''
    """
    
    if isnan(deg):
        return None

    # Define default format, if needed
    if dms_format is None:
        dms_format = "dms"

    if precision is None:
        if dms_format in ["d", "deg"]:
            precision = 4
        elif dms_format in ["dm", "deg+min"]:
            precision = 2         
        elif dms_format in ["dms", "deg+min+sec"]:
            precision = 1
        else:
            dms_format = "dms"
            precision = 1

    # unsigned result ready for appending compass direction
    deg = fabs(deg)
    
    # decimal pattern used to format float at a fixed precision
    digits_count = precision + 3
    decimal_pattern = "{:0" + str(digits_count) + "." + str(precision) + "f}"
    
    if dms_format in ["d", "deg"]:        
        # round degrees
        d = float(decimal_pattern.format(deg))
        dms = str(d) + DEGREE_CHAR
    elif dms_format in ["dm", "deg+min"]:
        # convert degrees to minutes & round            
        mn = deg*60
        # get component deg/min
        d = floor(mn/60)
        # pad with trailing zeros
        m = float(decimal_pattern.format(mn % 60))            
        dms = str(d) + '°'+  SEPARATOR + str(m).zfill(2) + MINUTE_CHAR
    elif dms_format in ["dms", "deg+min+sec"]:
        # convert degrees to seconds & round
        sec = deg * 3600    
        # get component deg/min/sec
        d = floor(sec / 3600)
        m = floor(sec / 60) % 60        
        s = float(decimal_pattern.format(sec % 60))
        dms = str(d) + '°' + SEPARATOR +  str(m).zfill(2) + MINUTE_CHAR +  SEPARATOR + str(s).zfill(2) + SECONDE_CHAR
    return dms

def toLat(deg, dms_format=None, precision=None):
    """
    Converts numeric degrees to deg/min/sec latitude (2-digit degrees, suffixed with N/S).
    Return a string representing degrees formatted as deg/min/secs according to specified format.
    
    Arguments :
        deg -- {float | int} -- Degrees to be formatted as specified.
        dms_format -- {string} -- Return value format as 'd', 'dm', 'dms' for deg, deg+min, deg+min+sec (default=dms)
        precision -- {int} -- Number of decimal to use (default: 1 for dms, 2 for dm, 4 for d).
    
    Example : 
        > dms.toLat(48.857000)
        > 48°51'25.2"N
        > dms.toLat(-48.857000)
        > 48°51'25.2"S
    """
    
    lat = toDMS(deg, dms_format, precision)
    if lat is None:
        return NONE_VALUE_CHAR
    compass_direction = 'S' if deg<0 else 'N'    
    return lat + SEPARATOR + compass_direction  

def toLon(deg, dms_format=None, precision=None):
    """
    Convert numeric degrees to deg/min/sec longitude (3-digit degrees, suffixed with E/W).
    Return a string representing degrees formatted as deg/min/secs according to specified format.
    
    Arguments:
        deg -- {float | int} -- Degrees to be formatted as specified.
        dms_format -- {string} -- Return value format as 'd', 'dm', 'dms' for deg, deg+min, deg+min+sec (default=dms)
        precision -- {int} -- Number of decimal to use (default: 1 for dms, 2 for dm, 4 for d).
    
     Example : 
        > dms.toLon(0.138833)
        > 0°08'19.8"E
        > dms.toLon(-0.138833)
        > 0°08'19.8"W
    """
    
    lon = toDMS(deg, dms_format, precision)
    if lon is None:
        return NONE_VALUE_CHAR
    compass_direction = 'W' if (deg < 0) else 'E'
    return lon + SEPARATOR + compass_direction


def toBearing(deg, dms_format=None, precision=None):
    """
    Converts numeric degrees to deg/min/sec as a bearing (0°..360°).
    Return a string representing degrees formatted as deg/min/secs according to specified format.
    
    Arguments:
        deg -- {float | int} -- Degrees to be formatted as specified.
        dms_format -- {string} -- Return value format as 'd', 'dm', 'dms' for deg, deg+min, deg+min+sec (default=dms)
        precision -- {int} -- Number of decimal to use (default: 1 for dms, 2 for dm, 4 for d).
    
     Example : 
        > dms.toBearing(-0.138833, "dm", 1)
        > 359°51.7
    """
    
    # normalise negative values to 180°..360°
    deg = float(deg+360)%360
    b = toDMS(deg, dms_format, precision)
    if b is None:
        return NONE_VALUE_CHAR
    else:
        # just in case rounding took us up to 360°
        return b.replace('360', '0')

def compassPoint(bearing, precision=3):
    """
    Return compass point (to given precision) for supplied bearing.
    
    Arguments:
        bearing -- {float | int} -- Bearing in degrees from north.
        precision -- {float | int} -- Precision (1:cardinal / 2:intercardinal / 3:secondary-intercardinal).
                                                    (default: 3)

     Example : 
            > dms.compatPoint(30)
            > NNE
            > dms.compassPoint(30, 2)
            > NE
            > dms.compassPoint(30, 1)
            > N
    """
    
    if precision not in [1, 2, 3]:
        raise ValueError('Precision must be between 1 and 3')
    
    # Normalise to 0..360
    bearing = ((bearing%360)+360)%360; 

    compass_4points = {
        0: 'N',
        1: 'E',
        2: 'S',
        3: 'W'
    }
    
    compass_8points = {
        0: 'N',
        1: 'NE',
        2: 'E',
        3: 'SE',
        4: 'S',
        5: 'SW',
        6: 'W',
        7: 'NW'
    }
    
    compass_16points = {
        0: 'N',
        1: 'NNE',
        2: 'NE',
        3: 'ENE',
        4: 'E',
        5: 'ESE',
        6: 'SE',
        7: 'SSE',
        8: 'S',
        9: 'SSW',
        10: 'SW',
        11:'WSW',
        12: 'W',
        13: 'WNW',
        14: 'NW',
        15: 'NNW',
    }
    
    compass_precisions = {
        1: compass_4points.get(round(bearing*4/360) % 4, NONE_VALUE_CHAR),
        2: compass_8points.get(round(bearing*8/360) % 8, NONE_VALUE_CHAR),
        3: compass_16points.get(round(bearing*16/360) % 16, NONE_VALUE_CHAR),
    }
    
    return compass_precisions.get(precision)
