
#!/bin/bash

# view_video.sh: script to process Cheetah video tracking files.
# This script is for processing raw Neuralynx Cheetah files including
# creating epochs (sleep1, maze, sleep2).  It is tailored for the NARP
# project but is a good starting point for other rat video tracking uses.
# The script will create PVD (position, velocity, direction files) or will
# dowload the existing PVD files, if the PVD option is selected.

# To run this script enter:
#  1-the name of the directory (e.g 10607/2019-6-26_7-26-49_10607)
#  2-optional flags, (PVD to create a PVD file, skipping the creation of epochs
#  If the position directory exists in the main directory, 
#    you must delete it manually if you wish to start from scratch; otherwise, 

# This script will check the input directory to see if the POSITION directory
# has been created.  
# use PVD option to bypass making epochs 
# If the PVD option is included, the script will run the matlab script 
# runNSMAVideo.m but will bypass the creating of epochs with ViderSliderPlot.py

rm -r ./RawData/

echo $1
filenames=$(aws s3 ls s3://narp-alext/$1/POSITION/ --human-readable | wc -l)
echo $filenames
if [ "$filenames" -lt 1 ]
then
   echo "POSITION directory does not exist; create it here"
   aws s3 cp s3://narp-alext/$1/ ./RawData/ --exclude '*' --include 'VT1.Nvt' --recursive
  
   python VideoSliderPlot.py 1 
   echo Enter Start of Behavior:
   read start
   echo start >> ./RawData/EPOCHS.dat
   python VideoSliderPlot.py -1
   echo Enter Stop of Behavior
   read stop
   
   python epochs.py $start $stop
   python ProcessRawVideo.py
   matlab -nodisplay -nodesktop -nosplash -r "run ./runNSMAVideo.m"

   #upload position data 
   aws s3 cp ./RawData/ s3://narp-alext/$1/POSITION/ --exclude '*' --include 'EPOCHS.npz' --include '*.pvd' --include '*.npz'  --recursive

else
   echo "DOWNLOADING exising position data"
   aws s3 cp s3://narp-alext/$1/POSITION/ ./RawData/ --exclude '*' --include '*.pvd' --include '*.npz' --recursive
 
   if [ "$2" == "VT1" ]
   then
     aws s3 cp s3://narp-alext/$1/ ./RawData/ --exclude '*' --include 'VT1.Nvt' --recursive
   fi
   if [ "$2" == "PVD" ]
   then
    aws s3 cp s3://narp-alext/$1/ ./RawDatat/ --exclude '*' --include 'VT1.Nvt' --recursive 
    python ProcessRawVideo.py
    matlab -nodisplay -nodesktop -nosplash -r "run ./runNSMAVideo.m"
    aws s3 cp ./RawData/ s3://narp-alext/$1/POSiITION --exclude '*' --include '*.pvd' --include '*.npz' --recursive
   fi
fi
