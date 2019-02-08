
import datetime
import random
lat_dir_list = ["N","S"]
lon_dir_list = ["E","W"]

def make_GGA():

    sentence_type = "GPGGA"
    UTC = str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)+"."+str(datetime.datetime.now().microsecond)

    #get a random float between -9000,00 and 9000.00
    rand = round(random.uniform(-9000.0, 9000.0),3)
    # choose a latitiude direction
    if rand < 0:
        lat_dir =  lat_dir_list[1]
    else:
        lat_dir = lat_dir_list[0]
    
    lat = str(rand)
    
    rand = round(random.uniform(-18000.0, 18000.0),3)
    # choose a latitiude direction
    if rand < 0:
        lon_dir =  lon_dir_list[1]
    else:
        lon_dir = lon_dir_list[0]
    
    lon = str(rand)

    fix_quality = "0"
    num_sats="8"
    dop=str(round(random.uniform(0.0,20.0),1))
    alt=str(round(random.uniform(0.0,1000.0),1))
    alt_units="M"
    MSL = str(round(random.uniform(0.0,100.0),1))
    MSL_units="M"

    gps_string = sentence_type+","+UTC+","+lat+","+lat_dir+","+lon+","+lon_dir+","+fix_quality+","+num_sats+","+dop+","+alt+","+alt_units+","+MSL+","+MSL_units+","+","   
    #print(gps_string)

    check_sum = 0
    for char in gps_string:
        check_sum ^= ord(char)
    
    check_sum_string = hex(check_sum)
    gga = "$"+gps_string+"*"+check_sum_string[2:]+"\n"
    #print("$"+gps_string+"*"+check_sum_string[2:])
    return gga
        