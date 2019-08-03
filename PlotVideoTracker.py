import VideoUtils as vu
import struct
import sys
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from shapely import geometry
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox
import pandas as pd


def arrow_key_control(event):
  global current_frame
  if event.key == 'left':
    current_frame -= 1 if current_frame > 1 else 0
  if event.key == 'right':
    current_frame += 1 if current_frame < len(x_pix) else len(x_pix)

  l1.set_color('r')
  l1.set_xdata(x_pix[current_frame:current_frame+100])
  l1.set_ydata(y_pix[current_frame:current_frame+100])

  l2.set_color('g')
  l2.set_xdata(pvdx[current_frame:current_frame+100])
  l2.set_ydata(pvdy[current_frame:current_frame+100])
     
  print(int(current_frame))
  fig.canvas.draw_idle()   


current_frame = 1     
videofile = './RawData/VT1.Nvt'
pvdfile = './RawData/maze_dnTout.pvd'
 
x, y, ts  = vu.getTrackerXY_Points(videofile)
x = x[79000:]
y = y[79000:]


x_pix = np.round(x/(np.max(x)/640))
y_pix = np.round(y/(np.max(y)/480))

pvdts, pvdx, pvdy = vu.readPVDfile(pvdfile)
fig, ax = plt.subplots()

l1, = plt.plot(x_pix,y_pix,'.', markersize=5, color='#FFE4C4')
l2, = plt.plot(pvdx, pvdy,'.', markersize=5, color='g')

cid = fig.canvas.mpl_connect('key_press_event', arrow_key_control)

plt.show()
