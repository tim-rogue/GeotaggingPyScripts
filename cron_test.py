
test_file = "/Users/Odroid/Documents/GPS_logs/count.txt"

count = 0

while True:

    with open(test_file,'a') as test:
        test.write(str(count)+"\n")
        test.close()
        
    count+=1
    
       
    