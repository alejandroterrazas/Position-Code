
#!/bin/bash
#script to process video tracking files
#use PVD option to bypass making epochs 
#updated to include automatically running matlab PVD script

rm -r ./RawData/
echo $1
test=$(aws s3 ls s3://narp-alext/$1/POSITION/ --human-readable | wc -l)
echo $test
if [ $test -lt 1 ]
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
 
   if [ $2 -eq "VT1" ] || [ $2 -eq "PVD" ]
   then
     aws s3 cp s3://narp-alext/$1/ ./RawData/ --exclude '*' --include 'VT1.Nvt' --recursive
   fi
   if [ $2 -eq "PVD" ]
   then 
    python ProcessRawVideo.py
    matlab -nodisplay -nodesktop -nosplash -r "run ./runNSMAVideo.m"
    aws s3 cp ./RawData/ s3://narp-alext/$1/POSiITION --exclude '*' --include '*.pvd' --include '*.npz' --recursive
   fi
fi
