from __future__ import division

import struct
import matplotlib.pyplot as plt
import numpy as np
import os
import array
import sys
import VideoUtils as vu
from scipy import ndimage

"""
Program to process raw video before using matlab to create PVD file.
Run VideoSliderPlot.py first to output the start and stop of the maze period

You can supply 'out of bounds' limits with arguments.  YLim is most common.
"""

def makeMaskfromTracker(xvals, yvals):
  accumulate = np.zeros([640,480])
  mask = np.zeros_like(accumulate)
  for x, y in zip(xvals,yvals):
     #print(x,y)
     if (xlim[0] < x < xlim[1]) and (ylim[0] < y < ylim[1]):
        accumulate[x,y] +=1
  mask[np.where(accumulate>5)] = 1
 # mask = ndimage.binary_erosion(mask, structure=np.ones((30,30)))
  mask = ndimage.binary_dilation(mask, structure=np.ones((10,50)))

  return mask


def makeMask(data):

  accumulate = np.zeros([640,480])
  mask  = np.zeros_like(accumulate)

  for ii,targets in enumerate(data):
    for t in targets:
      line = format(t,'032b')
      pure = line[0:4]
      y = int(line[4:16], 2)
      raw = line[16:20]
      x = int(line[20:], 2)

      if (ylim[0] < y < ylim[1]) and (xlim[0] < x < xlim[1]):
        accumulate[x,y] += 1

  mask[np.where(accumulate>10)] = 1
  #erode and dilate mask to find outline of maze
  mask = ndimage.binary_erosion(mask, structure=np.ones((30,30)))
  mask = ndimage.binary_dilation(mask, structure=np.ones((10,50)))
 
  return mask

def outputPrePVDfromTracker(outfile, xvals, yvals, ts, 
                            plotit, xlim, ylim, applymask=False):
 
  f = open(outfile, "w")
  img = np.zeros([640,480])

  for ii, (x, y) in enumerate(zip(xvals, yvals)):
    write_rec = False
    if (xlim[0] < x < xlim[1]) and (ylim[0] < y < ylim[1]):
    
      if applymask==True:
        if mask[x,y] == 1:
           write_rec = True
      if applymask==False:
         write_rec = True
   
      if write_rec == True:
         outstr= "{} {} {} {} {} {} {} {} {} {}\n".format(
                  ts[ii], 1, 0, 0, 0, 0, 0, 0, x, y)

         f.write(outstr)
         img[x,y] += 1
       
  f.close()

    
def outputPrePVD(outfile, data, ts, plotit, xlim, ylim, applymask=False): 
  f = open(outfile, "w")
  img = np.zeros([640,480])

  for ii,targets in enumerate(data):
    #if ii%100 == 0 print("Processing record # ", ii)
    for t in targets:
      write_rec = False
      line = format(t,'032b')
      pure = line[0:4]
      y = int(line[4:16], 2)
      raw = line[16:20]
      x = int(line[20:], 2)

      if (ylim[0] < y < ylim[1]) and (xlim[0] < x < xlim[1]):
        if applymask==True:
          if mask[x,y] == 1:
            write_rec = True
        if applymask==False:
          write_rec = True
   
      if write_rec == True:
         outstr= "{} {} {} {} {} {} {} {} {} {}\n".format(
                  ts[ii], 
                  raw[0], raw[1], raw[2], raw[3],
                  pure[1], pure[2], pure[3],
                  x, y)

         f.write(outstr)
         img[x,y] += 1
       
  f.close()

## check ylim

xlim = [0, 640]
ylim = [0, 480]
#ylim = [250, 480]

npzfile = np.load('./RawData/EPOCHS.npz')
start = npzfile['arr_0'].astype(int)
stop = npzfile['arr_1'].astype(int)
videofile = './RawData/VT1.Nvt'

timestamps, xpt, ypt, dwP, dnT = vu.getVideoData(videofile)

P = list(dwP[start:stop])
T = list(dnT[start:stop])
ts = list(timestamps[start:stop])

mask = makeMask(P)
np.savez("./RawData/mask", mask)

#plt.imshow(mask)
#plt.show()
outputPrePVD("./RawData/maze_dwPout.ascii", 
               P, ts, 0, xlim, ylim,applymask=True)
outputPrePVD("./RawData/maze_dnTout.ascii",
               T, ts, 0, xlim, ylim,applymask=True)


##combine sleep epochs into one big sleep session using the following

P = list(dwP[:start]) + list(dwP[stop:])
T = list(dnT[:start]) + list(dnT[stop:])

ts = list(timestamps[:start]) + list(timestamps[stop:])

outputPrePVD("./RawData/sleep_dwPout.ascii", 
             P, ts, 0, xlim, ylim)

outputPrePVD("./RawData/sleep_dnTout.ascii", 
             T, ts, 0, xlim, ylim)
 
x, y, ts = vu.getTrackerXY_Points(videofile)
print("x: ", x, "y: ", y)

x_pix = np.round(x/(np.max(x)/640)).astype(int)
y_pix = np.round(y/(np.max(y)/480)).astype(int)

print("x_pix: ", x_pix, "y_pix: ", y_pix)
x = list(x_pix[start:stop])
y = list(y_pix[start:stop])
ts = list(ts[start:stop])
mask = makeMaskfromTracker(x, y)
plt.imshow(mask)
plt.show()
np.savez("./RawData/mask", mask)

outputPrePVDfromTracker("./RawData/maze_trackerout.ascii",
                          x,y, ts, 0, xlim, ylim,applymask=True)


##combine sleep epochs into one big sleep session using the following

x = list(x[:start]) + list(x[stop:])
y = list(y[:start]) + list(y[stop:])

ts = list(ts[:start]) + list(ts[stop:])

outputPrePVDfromTracker("./RawData/sleep_trackerout.ascii", 
             x,y, ts, 0, xlim, ylim)


