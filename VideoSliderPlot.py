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

dir = sys.argv[1]

print("Dir {}".format(dir))

def slider_on_change(val):
   if dir == "1":
      l1.set_xdata(xfilt[0:int(val)])
      l1.set_ydata(yfilt[0:int(val)])
   elif dir == "-1":
      l1.set_xdata(xfilt[int(val):-1])
      l1.set_ydata(yfilt[int(val):-1])
   if dir == "0":
      l2.set_xdata(newx[int(val):(int(val)+10000)])
      l2.set_ydata(newy[int(val):(int(val)+10000)])

   print(int(val))
   fig.canvas.draw_idle()   
     
videofile = './RawData/VT1.Nvt' 
x, y, ts  = vu.getTrackerXY_Points(videofile)

xfilt = vu.smooth(x, window_len=200)
yfilt = vu.smooth(y, window_len=200)

#plot min and max values
xmin = np.amin(xfilt)
xmax = np.amax(xfilt)
ymin = np.amin(yfilt)
ymax = np.amax(yfilt)

ylim=100
#xfilt,yfilt = vu.mask(xfilt,yfilt,0, ylim)

fig, ax = plt.subplots()

l1, = plt.plot(xfilt,yfilt,'.', markersize=5, color='#FFE4C4')

if dir == "0":
    l2, = plt.plot(newx[1:1000],newy[1:1000],'.', markersize=5, color='#0F0F0F')

#l1, = plt.plot(xfilt, yfilt, '.', markersize=5, color='#FFE4C4')

#plt.xlim([40000,np.amax(xfilt)+1000])
plt.xlim([xmin-1000, xmax+1000])
plt.ylim([ymin-1000, ymax+1000])

tslider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03])
tslider = Slider(tslider_ax, 'Time', 0.1, len(xfilt), valinit=0.1)
tslider.on_changed(slider_on_change)

#cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
