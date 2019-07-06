from __future__ import division

import struct
import matplotlib.pyplot as plt
import numpy as np
import os
import array
import sys
       
def getVideodata(data):

  nrecords = int(len(data)/1828)
  print("Number of Records: {}".format(nrecords))
  #nrecs=3000
  xloc=np.zeros(nrecords, dtype=np.uint8)
  yloc=np.zeros(nrecords, dtype=np.uint8)
  hdir=np.zeros(nrecords, dtype=np.uint8)
  ts= np.zeros(nrecords, dtype=np.uint64)
 # dwPoints = np.zeros([nrecords,400])
  dwPoints = []
  dnTargets = []
  recsize=1828
  
  for record in range(nrecords):
    # print(record)
     recoffset = recsize*record
     swstx = int(struct.unpack('H',data[recoffset:recoffset+2])[0])
#     print("swstx: {}".format(swstx))
     swid = int(struct.unpack('H',data[recoffset+2:recoffset+4])[0])
#     print("swid: {}".format(swid))
     swdata_size = int(struct.unpack('H',data[recoffset+4:recoffset+6])[0])
#     print("swdata_size: {}".format(swdata_size)) 
     ts[record] = int(struct.unpack('Q',data[recoffset+6:recoffset+14])[0])
     dwP = struct.unpack('400I',data[recoffset+14:recoffset+1614])
#     print(len(dwP)
     dwPoints.append(tuple(p for p in dwP if int(p) != 0))
     sncrc = int(struct.unpack('H', data[recoffset+1614:recoffset+1616])[0])
     xloc[record] = int(struct.unpack('i', data[recoffset+1616:recoffset+1620])[0])
     yloc[record] = int(struct.unpack('i', data[recoffset+1620:recoffset+1624])[0])
     hdir[record] = int(struct.unpack('i', data[recoffset+1624:recoffset+1628])[0]) 
 
     dnT = struct.unpack('50i',data[recoffset+1628:recoffset+1828])
     #newone = struct.unpack('H', data[recoffset+1828:recoffset+1830])[0]
     #print("new one {}".format(newone))

     dnTargets.append(tuple(t for t in dnT if int(t) != 0))
  return ts, xloc, yloc, dwPoints, dnTargets

xlim = [int(sys.argv[1]), int(sys.argv[2])]
ylim = [int(sys.argv[3]), int(sys.argv[4])]
print(xlim)
print(ylim)

sleep = int(sys.argv[5])

vidfile = './RawData/VT1.Nvt'

with open(vidfile, 'rb') as f:
    videodata = f.read()[16384:]
    f.close()

npzfile = np.load('./RawData/EPOCHS.npz')
start = npzfile['arr_0'].astype(int)
stop = npzfile['arr_1'].astype(int)


#data = videodata[10000:20000]

timestamps, xpt, ypt, dwP, dnT = getVideodata(videodata)
img=np.zeros([640, 480], dtype=np.uint8)


print(start)
print(stop)

if sleep == 1:
  timestamps = list(timestamps[:start]) + list(timestamps[stop:])
  xpt = list(xpt[:start]) + list(xpt[stop:])
  ypt = list(ypt[:start]) + list(ypt[stop:])
  dwP = list(dwP[:start]) + list(dwP[stop:])
  dnT = list(dnT[:start]) + list(dnT[stop:])
else:
  timestamps = list(timestamps[start:stop])
  xpt = list(xpt[start:stop])
  ypt = list(ypt[start:stop])
  dwP = list(dwP[start:stop])
  dnT = list(dnT[start:stop])


outfile = './RawData/dnTout.ascii'
f = open(outfile, "w")

for ii,targets in enumerate(dnT):
  for t in targets:
    line = format(t,'032b')
    pure = line[0:4]
    y = int(line[4:16], 2)   
    raw = line[16:20]
    x = int(line[20:], 2)
      
    outstr=str(timestamps[ii]) + ' ' \
         + str(raw[0]) + ' ' + str(raw[1]) + ' ' + str(raw[2]) + ' ' + str(raw[3]) + ' ' \
         + str(pure[1]) + ' ' + str(pure[2]) + ' ' + str(pure[3]) + ' ' \
         + str(x) + ' ' + str(y) + '\n'
    if (ylim[0] < y < ylim[1]) and (xlim[0] < x < xlim[1]):
      f.write(outstr)
      img[x,y] += 1
      #print(outstr)
plt.subplot(2,2,1)
plt.plot(ypt,xpt,'b.')

plt.subplot(2,2,2)
plt.imshow(img)
#plt.show()

f.close()

outfile = './RawData/dwPout.ascii'

f = open(outfile, "w")

img=np.zeros([640, 480], dtype=np.uint8)
for ii,p in enumerate(dwP):
  for pt in p:
    line = format(pt,'032b')
    pure = line[0:4]
  
    y = int(line[4:16], 2)
    raw = line[16:20]
    x = int(line[20:], 2)
    
    outstr=str(timestamps[ii]) + ' ' \
         + str(raw[0]) + ' ' + str(raw[1]) + ' ' + str(raw[2]) + ' ' + str(raw[3]) + ' ' \
         + str(pure[1]) + ' ' + str(pure[2]) + ' ' + str(pure[3]) + ' ' \
         + str(x) + ' ' + str(y) + '\n'
 
    if (ylim[0] < y < ylim[1]) and (xlim[0] < x < xlim[1]):
      f.write(outstr)
      img[x,y] += 1
      #print(outstr)

plt.subplot(2,2,3)
 
plt.imshow(img)
plt.show()

f.close()


"""lopt
Information about file formats for Cheetah video

UInt16 swstx Value indicating the beginning of a record. Always 0x800 (2048).
UInt16 swid ID for the originating system of this record.
UInt16 swdata_size Size of a VideoRec in bytes.
UInt64 qwTimeStamp Cheetah timestamp for this record. This value is in microseconds.
14 + 1600 2 4 4 4 200
UInt32[] dwPoints Points with the color bitfield values for this record. This is a 400
element array. See Video Tracker Bitfield Information below.

Int16 sncrc Unused*

Int32 dnextracted_x Extracted X location of the target being tracked.
Int32 dnextracted_y Extracted Y location of the target being tracked.
Int32 dnextracted_angle The calculated head angle in degrees clockwise from the positive Y
axis. Zero will be assigned if angle tracking is disabled.**

Int32[] dntargets Colored targets using the samebitfield format used by the dwPoints
array. Instead of transitions, the bitfield indicates the colors that make
up each particular target and the center point of that target. This is a
50 element array sorted by size from largest (index 0) to smallest
(index 49). A target value of 0 means that no target is present in that
index location. See Video Tracker Bitfield Information below.

Video Tracker Bitfield Information:
The pixel data consists of four hundred 32 bit values (one 32 bit value per pixel). The target data
consists of fifty 32 bit values. These data have the same bit-field format which means that the 32 bit
value is broken up into sub data to describe the X location (pixel number in the line), Y location (line
number  of the frame) and the tracker colors which were above and below threshold.

The X and Y values are allocated 12 bits each, but their maximum value is determined by the resolution
that is used when tracking. See the header of your file for information about the resolution used when
your file was recorded. The other bits indicate which of the color values were above (1) or below (0)
their respective threshold setting. The layout of these bit fields can be visualized by the following:
"""
 
    
    
