#!/usr/local/bin/python

import pynmea2
import subprocess
import datetime
import os
import sys
import gpsToExif


testing = True
date = datetime.datetime.now().strftime('%Y-%m-%d')
file_extension=".log"

if(testing):
    print("script generated log file name: ")
    test_log_name = "2016-11-24.log"
    print(test_log_name)

#this line will be uncommented for use on the ODROID
#log_file = "/Users/Odroid/Documents/GPS_logs/"+date+file_extension


#this line will be uncommented for testing my mac
log_file = "/Users/timrogerson/Desktop/ODROID_progs/GPS_logs/"+test_log_name

#This the the file that this script will write errors to. 
geotag_log = "/Users/timrogerson/Desktop/ODROID_progs/geotag_Log_"+date+".log"

#this is the path to the gphoto error log. 
#Only written to in this script to to make for easier human reading of the file
gphoto_error_log = "/Users/timrogerson/Desktop/ODROID_progs/gphoto_error.txt"


#check to see if a destination for the image to be geotagged is given, if not exit the script
try:
    print("The destination for the downloaded image is ")
    print(sys.argv[2])
    print("THe image file name is ")
    print(sys.argv[1])
except:
    with open(geotag_log,'a') as error_log:
        curr_datetime = str(datetime.datetime.now())
        error_log.write("\n\n")
        error_log.write(curr_datetime+"\n")
        error_log.write("The destination folder for the image to be geotagged either doesn't exist or was not passed to this script.")
        error_log.close()
    sys.exit()

#save the path to the image that wil be geotagged
image_path = sys.argv[2]
image_file_name=sys.argv[1]

#open log file (if log file can't be open for some reason write that error to the error log)
try:
    with open(log_file,'rb') as log:
        #loop through the entire file
        for line in log:
            pass
        #get the last line of the file i.e th most recent NMEA string
        last_line = line
        log.close()
except:
    with open(geotag_log,'a') as error_log:
        curr_datetime = str(datetime.datetime.now())
        error_log.write("\n\n")
        error_log.write(curr_datetime+"\n")
        error_log.write("Could not open the GPS logfile. File may not exist yet, or this script\nmay have the wrong path.")
        error_log.close()

#parse the last line of the GPS log file 
#If line can't be parsed write that error to the error log
try:
    #parse the last line of the GPS log file
    gps_data = pynmea2.parse(last_line)
    print(gps_data.lat)
    print(gps_data.lon)
    print(gps_data.timestamp)
    
except:
    with open(geotag_log,'a') as error_log:
        curr_datetime = str(datetime.datetime.now())
        error_log.write("\n\n")
        error_log.write(curr_datetime+"\n")
        error_log.write("Couldn't parse the most recent NMEA sentence in  "+log_file)
        error_log.close()
        sys.exit()


##Need to write lines that convert lat,lon,timestamp into format recognized by 
## EXif data
exif_lat = gpsToExif.latLonToExif(gps_data.lat)
exif_lon = gpsToExif.latLonToExif(gps_data.lon)
exif_time = gpsToExif.gpsTimeToExif(gps_data.timestamp)




try:
    #call exiftool to edit image meta data
    subprocess.call(["exiftool","-GPSLongitudeRef="+gps_data.lon_dir,\
                                "-GPSLongitude="+exif_lon,\
                                "-GPSLatitudeRef="+gps_data.lat_dir,\
                                "-GPSLatitude="+exif_lat,\
                                "-GPSTimeStamp="+exif_time,\
                                "-GPSAltitudeRef="+"Above Sea Level",\
                                "-GPSAltitude="+str(gps_data.altitude),\
                                image_path+"/"+image_file_name])
    
    
    #when exiftool edits image file data it save the unedited orginal file as "file_name.jpg_original"
    # this line deletes that original file and only keeps the new edited file
    subprocess.call(["rm", image_path+"/"+image_file_name+"_original"])                             
                                
    '''subprocess.call(["exiftool","-GPSLongitudeRef="+gps_data.lon_dir,\
                                "-GPSLongitude="+gps_data.lon,\
                                "-GPSLatitudeRef="+gps_data.lat_dir,\
                                "-GPSLatitude="+gps_data.lat,\
                                "-GPSTimeStamp="+exif_time,\
                                "-GPSAltitudeRef="+"Above Sea Level",\
                                "-GPSAltitude="+str(gps_data.altitude),\
                                image_path+image_file_name])'''
except:
    with open(geotag_log,'a') as error_log:
        curr_datetime = str(datetime.datetime.now())
        error_log.write("\n\n")
        error_log.write(curr_datetime+"\n")
        error_log.write("Exiftool could not edit the meta data of the provided image.\n")
        error_log.close()
        sys.exit()
    sys.exit()
    
#write the successfully changed data to the geotag log file
with open(geotag_log,'a') as error_log:
    curr_datetime = str(datetime.datetime.now())
    error_log.write("\n\n")
    error_log.write(curr_datetime+"\n")
    error_log.write("Image: "+image_file_name+"\n")
    error_log.write("Image meta-data succesfully changed.\n\n")
    error_log.write("    GPSLongitudeRef="+gps_data.lon_dir+"\n")
    error_log.write("    GPSLongitude="+exif_lon+"\n")
    error_log.write("    GPSLatitudeRef="+gps_data.lat_dir+"\n")
    error_log.write("    GPSLatitude="+exif_lat+"\n")
    error_log.write("    GPSTimeStamp="+exif_time+"\n")
    error_log.write("    GPSAltitudeRef="+"Above Sea Level"+"\n")
    error_log.write("    GPSAltitude="+str(gps_data.altitude)+"\n")
    error_log.close()
    
with open(gphoto_error_log,'a') as gphoto_log:
    curr_datetime = str(datetime.datetime.now())
    gphoto_log.write("\n\n")
    gphoto_log.write("------------------ "+curr_datetime+" ------------------------")
    gphoto_log.close()
       
#for testing, print out the meta data of the image
subprocess.call(["exiftool","-GPSLongitudeRef","-GPSLongitude","-GPSLatitudeRef","-GPSLatitude","-GPSTimeStamp","-GPSAltitudeRef","-GPSAltitude",image_path+"/"+image_file_name])


