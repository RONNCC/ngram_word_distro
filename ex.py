import string
import matplotlib
matplotlib.use('WX')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from itertools import izip,chain


f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,sharex='col',sharey='row')

ax1.plot(range(10),2*np.arange(10))
ax2.plot(range(10),range(10))
ax3.plot(range(5),np.arange(5)*1000)
#pyplot.yscale('log')
#ax2.set_autoscaley_on(False)
#ax2.set_ylim([0,10])


plt.show()
