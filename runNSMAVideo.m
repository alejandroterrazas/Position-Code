addpath('/home/alext/NSMA-Matlab-Code/Packages/Video_Processing/')
addpath('./')
y = extractvidposwm('./RawData/maze_dwPout.ascii', './RawData/maze_dwPout.pvd', 10,20,0,1)
y = extractvidposwm('./RawData/maze_dnTout.ascii', './RawData/maze_dnTout.pvd', 10,20,0,1)
y = extractvidposwm('./RawData/sleep_dwPout.ascii', './RawData/sleep_dwPout.pvd', 10,20,0,1)
y = extractvidposwm('./RawData/sleep_dnTout.ascii', './RawData/sleep_dnTout.pvd', 10,20,0,1)

quit
