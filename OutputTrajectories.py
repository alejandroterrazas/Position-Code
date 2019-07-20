import numpy as np
from matplotlib import pyplot as plt
import sys


'''
OutputTrajectories.py
Program to turn  ascii pvd (position, velocity, direction) file into individual
trajectories.

The program output two numpy otuput files for each pvd file input: 

   1) _MOVING.npz
   2) _NOTMOVING.npz

These represent epochs where the rat is running on the maze or stopped.  
The main part of the program involves grouping consecutive timestamps
and smoothing over small blips of a few timestamps that are not significant
stops epochs or moving epochs.

The program accepts two command lin inputs: 
 1) the PVD file to proessing  and
 2) an optional flag "plot" that results in the program ploting
 every trajectory (good for verifying but can result in many plots 
 that must be exited each time)  

Note: the PVD file is created in the view_video.sh script that either downloads
the PVD file or creates it fresh depending on flags supplied to view_video.sh
'''

def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result

pvdfile = sys.argv[1]
plotit = sys.argv[2]

data = open(pvdfile, "r")

PVD = []

for line in data:
   PVD.append(line.split())

PVD = np.squeeze(np.array([PVD]))

ts = PVD[:,0].astype(int)
x  = PVD[:,1].astype(int)
y = PVD[:,2].astype(int)

plt.plot(x,y,'r.')
plt.ylim([0,480])
plt.xlim([0,640])
plt.show()
 

window_size = 5000
xdiff = np.abs(np.diff(np.convolve(x,  np.ones(window_size, 
                       dtype=np.int), 'valid')))

ydiff = np.abs(np.diff(np.convolve(y, np.ones(window_size,
                                   dtype=np.int), 'valid')))

totdist = xdiff+ydiff

inotmoving = np.where(totdist<20)[0]
grouped = group_consecutives(inotmoving)
starts = []
stops = []

#print(grouped)

for group in grouped:
    print("length of group: ", len(group))
    if len(group)>1000:
      starts.append(ts[group[0]])
      stops.append(ts[group[-1]])
      print(starts)
      if plotit == 'plot':
        plt.plot(x[group[0]:group[-1]], y[group[0]:group[-1]],'b.')
        print(x[group[0]:group[-1]])

        plt.ylim([0,480])
        plt.xlim([0,640])
        plt.show()


outfile = pvdfile.replace('.pvd', '_NOTMOVING')
np.savez(outfile, starts, stops)

imoving = np.where(totdist>40)[0]
grouped = group_consecutives(imoving)

starts = []
stops = []

for group in grouped:
    print("len group: ", len(group))
    if len(group)  > 1000:
      starts.append(ts[group[0]])
      stops.append(ts[group[-1]])
     # minix = x[group[0]:group[-1]]
      if plotit == 'plot':
        plt.plot(x[group[0]:group[-1]], y[group[0]:group[-1]],'b.')
        plt.ylim([0,480])
        plt.xlim([0,640])
        plt.show()


outfile = pvdfile.replace('.pvd', '_MOVING')
np.savez(outfile, starts, stops)



#outfile = './RawData/NOTMOVING.txt'
#f = open(outfile, "w")

#for start, stop in zip(starts,stops):
#  f.write(str(start))
#  f.write(',')
#  f.write(str(stop))
#  f.write('\n')

#f.close()

#print(inotmoving)
#print(totdist[inotmoving])
#notmoving = np.zeros(np.size(totdist))
#notmoving[inotmoving] = 1
#print(notmoving)

#hist, bin_edges = np.histogram(totdist,100)
#print(bin_edges)

#print(xdiff[40000:60000])


#print(x)
#print(y)

