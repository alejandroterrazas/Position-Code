from __future__ import division

import struct
import matplotlib.pyplot as plt
import numpy as np
import os
import array
import sys
from matplotlib.widgets import Cursor
import matplotlib.path as mpath

"""
Program to mask raw video before using matlab to create PVD file.
Run VideoSliderPlot.py first to output the start and stop of the maze period
"""
       
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
     dnTargets.append(tuple(t for t in dnT if int(t) != 0))
  return ts, xloc, yloc, dwPoints, dnTargets

def maskData(data, outfile):
  global imgdata, ts
  f = open(outfile, "w")

  for ii,targets in enumerate(data):
    for t in targets:
      line = format(t,'032b')
      pure = line[0:4]
      y = int(line[4:16], 2)
      raw = line[16:20]
      x = int(line[20:], 2)
      if (0 < y < 640)  and (0 < x < 480): 
        if imgdata[x,y] != 0:
          outstr=str(ts[ii]) + ' ' \
          + str(raw[0]) + ' ' + str(raw[1]) + ' ' + str(raw[2]) + ' ' + str(raw[3]) + ' ' \
          + str(pure[1]) + ' ' + str(pure[2]) + ' ' + str(pure[3]) + ' ' \
          + str(x) + ' ' + str(y) + '\n'
          f.write(outstr)

  f.close()

def cleanMask(event):
   """erases points from imdata based on cursor movement"""
   global imgdata, img
   if event.ydata != None and event.xdata !=None:
     y = int(event.ydata)
     x = int(event.xdata)
     imgdata[y-10:y+10,x-10:x+10] = 0

   img.set_data(imgdata)
   fig.canvas.draw()

def plotData(data): 
  """read the targets and store counts in imgdata"""
  global imgdata, img
  imgdata = np.zeros([640,480])

  for ii,targets in enumerate(data):
    for t in targets:
      line = format(t,'032b')
      pure = line[0:4]
      y = int(line[4:16], 2)
      raw = line[16:20]
      x = int(line[20:], 2)
  
      if (0 < y < 480) and (0 < x < 640):
        imgdata[x,y] += 1

  img = plt.imshow(imgdata, clim=[0,1]) 
  plt.show()


sys.setrecursionlimit(100000)

vidfile = './RawData/VT1.Nvt'

with open(vidfile, 'rb') as f:
    videodata = f.read()[16384:]
    f.close()

npzfile = np.load('./RawData/EPOCHS.npz')
start = npzfile['arr_0'].astype(int)
stop = npzfile['arr_1'].astype(int)

ts, xpt, ypt, dwP, dnT = getVideodata(videodata)

#print(start)
#print(stop)

#clean and output sleep 1
P = list(dwP[:start])
T = list(dnT[:start])

fig, ax = plt.subplots()
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
cid_motion = fig.canvas.mpl_connect('motion_notify_event', cleanMask)
plotData(P)
maskData(P, './RawData/dwPsleep1.ascii')
maskData(T, './RawData/dnTsleep1.ascii')

#clean and output maze data
P = list(dwP[start:stop])
T = list(dnT[start:stop])

fig, ax = plt.subplots()
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
cid_motion = fig.canvas.mpl_connect('motion_notify_event', cleanMask)
plotData(P)
maskData(P, './RawData/dwPmaze.ascii')
maskData(T, './RawData/dnTmaze.ascii')

#clean and output sleep2 data
P = list(dwP[stop:])
T = list(dnT[stop:])

fig, ax = plt.subplots()
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
cid_motion = fig.canvas.mpl_connect('motion_notify_event', cleanMask)
plotData(P)
maskData(P, './RawData/dwPsleep2.ascii')
maskData(T, './RawData/dnTsleep2.ascii')
    
