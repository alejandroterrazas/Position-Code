import numpy as np
import sys

np.savez("./RawData/EPOCHS.npz", sys.argv[1], sys.argv[2]) 
