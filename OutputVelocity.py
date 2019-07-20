import numpy as np
from matplotlib import pyplot as plt
import sys


'''
OutputVelocity.py
Program to turn  ascii pvd (position, velocity, direction) file into epochs
for speed vs theta analysis.  

The program outputs a single file with timestamps and velocities
files a PVD (position velocity direction).  Note, the PVD file created
with NSMA matlab code does not output velocity. 

The program accepts two command line inputs: 

1-the PVD file to process and
2-the duration (nominaly 3 secs).

Note: the PVD file is created in the view_video.sh script that either downloads
the PVD file or creates it fresh depending on flags supplied to view_video.sh
'''

pvdfile = sys.argv[1]

data = open(pvdfile, "r")

PVD = []

for line in data:
   PVD.append(line.split())

PVD = np.squeeze(np.array([PVD]))

ts = PVD[:,0].astype(int)
x  = PVD[:,1].astype(int)
y = PVD[:,2].astype(int)

##for video, every 60 samples = one second



print((ts[-1] - ts[0])/60)

starts = ts[0:-1:180]
stops = ts[180:-1:180]
print((stops-starts[:-1])/1000000.)

window_size = 500

xdiff = np.abs(np.diff(np.convolve(x,  np.ones(window_size, 
                       dtype=np.int), 'valid')))

ydiff = np.abs(np.diff(np.convolve(y, np.ones(window_size,
                                   dtype=np.int), 'valid')))
nsecs = 3
samples_sec = 60
block_size = nsecs*samples_sec

totdist = xdiff+ydiff
endrec = int(block_size*(np.floor(len(totdist)/block_size)))
print(endrec)


by_samples = np.reshape(totdist[:endrec], (block_size, -1))
velocities = np.sum(by_samples, axis = 1)

print(velocities)

#outfile = pvdfile.replace('.pvd', '_speeds')

