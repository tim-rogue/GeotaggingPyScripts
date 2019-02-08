
# This function s called within the function latLonToExif. It converts a float representing a GPS latitude or longitude value
# in the degrees decimal minutes format to degrees minutes seconds format and returns the three
# values in a list.
# e.g 5258.674 is 52 degrees 58.674 minutes. This converts to 52 degrees 58 minutes 40.44 seconds.
# The returned list is [52,58,40.44]. Note seconds will be rounded to 2 decimal points. This may
# introduce error into the final result. This may have to be corrected in after testing  
def GGA_latLonToDegMinSec(latLon):
    
    decimalMinutes = round(latLon%100,3)
    #print("decimalMinutes: ")
    #print(decimalMinutes)
    degrees = int((latLon-decimalMinutes)/100)
    #print("dergees: ")
    #print(degrees)
    degDecMin= [degrees,decimalMinutes]
    #print("degDecMin: ")
    #print(degDecMin)    
    return degDecMin

# This function takes an NMEA GGA lat/lon string DDMM.m (degrees and decimal minutes)  
#  and converts it to a string that is in Exif format 'Degrees/1,Minutes/1,Seconds/100'
# e.g 5852.674 will be returned as '58/1,52/1,4044/100'
#
def latLonToExif(latLonString):
    latLon = float(latLonString)
    if(latLon < 0):
        latLon*=-1
    degDecMin = GGA_latLonToDegMinSec(latLon)
    degrees = str(degDecMin[0])
    dec_min = str(degDecMin[1]) 
    exifLatLon = degrees+","+dec_min
    #exifLatLon = degrees+' deg '+minutes+'\' '+seconds+'\'\' '
    return exifLatLon




#This function takes a datetime.time(h,m,s) object and converts it into a unix timestamp string
# of the form "hh:mm:ss". i.e datetime.time(11,34,28) -> '11:34:28' 
def gpsTimeToExif(datetime):
   
    utc_string = str(datetime.hour)+':'+str(datetime.minute)+':'+str(datetime.second)    
    return utc_string     

