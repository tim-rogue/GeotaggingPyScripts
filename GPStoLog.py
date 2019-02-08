import serial
import io
import os
import datetime
import GGA_sentence_generator
connected = False
testing = True

if(testing == True):
    num_lines = 20
    for line in range(num_lines):
        sentence = GGA_sentence_generator.make_GGA()
        GPS_log = open("/Users/timrogerson/Desktop/ODROID_progs/GPS_logs/2016-11-24.log", 'a')
        GPS_log.write(sentence)
        GPS_log.close()
        
    
    

else:
    locations = ['/dev/ttyACM0']
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    folder = "/Users/Odroid/Documents/GPS_logs/"
    filename = date+'.log'

    for device in locations:
        try:
            print("Trying..." + device)
            #creates serial object
            #with device=/dev/ttyACMO, at 9600 baud, timeout units are seconds
            ser=serial.Serial(device,9600,timeout=2)
            #TextIOWrapper takes a read/write stream (in this case the serial port)
            #and specifies an End-of-line character for the readlin() method
            serial_in=io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),  
                                   newline = '\n',
                                   line_buffering = True)
            print("connected")
            break
        except:
            print("Failed to connect to "+device)

    if(not os.path.isdir(folder+date)):
        path = folder+date
        os.makedirs(path)
    


    #while not connected:
    #    line = serial_in.readln()
    #    connected = True

    while(1):
    
        #try:
            #GPS_log = open('GPS.log', 'a')
            #break
        #except:
            #print('Can not open file'+GPS.log)
        GPS_log = open(path+filename, 'a')
        line=serial_in.readline()    
        print(line)
        GPS_log.write(line)
        #forces the buffered data into the operating systems buffers
        GPS_log.flush()
        #ensure the operating systems buffers are written to disk
        #makes sure if power is cut to system the data isn't lost
        os.fsync
        GPS_log.close()
        #print(line)

