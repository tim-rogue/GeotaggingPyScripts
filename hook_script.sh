#!/bin/bash

# a directory with the days date. This line used in production
#FOLDER="/Users/Odroid/Documents/$(date +%F)"

# a directory with the days date. This line used in testing
FOLDER="/Users/timrogerson/Desktop/ODROID_progs/test_images/$(date +%F)"


#create a directory with the days date if one doesn't already exist
if [ ! -d "$FOLDER" ]; then
  # Control will enter here if $FOLDER doesn't exist.
  mkdir $FOLDER
fi


case "$ACTION" in
        init)
                # Called just after gphoto2 starts
                # Return non-zero exit code to abort
                ;;

        start)
                # Called just before gphoto2 executes requested commands
                ;;

        stop)
                # Called just before gphoto2 ends
                ;;

        download)
                # Called just after a file has been downloaded to the computer
                # move the newest picture to a folder with todays date
        TIMESTAMP="$(date +%s_%3N).jpg"
		mv "$ARGUMENT" "$FOLDER"
		#change directory into the folder with the current date
		cd "$FOLDER"
		#rename the new image file ($ARGUMENT) with the current unix timestamp formated to seconds from JAn-1-1970
		#with a milliseconf suffix e.g 1480635656_545.jpg
		mv "$ARGUMENT" "$TIMESTAMP"
		#change directory to the previous folder where the geotag.py script is 
		cd -
		
                 
                ./geotag.py "$TIMESTAMP" "$FOLDER"
                ;;
esac







