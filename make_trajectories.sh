
#!/bin/bash
# make_trajectories.sh
# script to loop over PVD files and convert to .npz trajectories
# Run this script after running view_video.sh.
# To run the script type ./make_trajectories.sh
# add the flag 'plot' to get a plot of every trajectory (can be tedious)

for filename in ./RawData/*.pvd; do
   echo "$filename"
   python OutputTrajectories.py $filename $1
done 
