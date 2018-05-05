import numpy as np
import pylab 
x = np.linspace(0, 20, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

pylab.plot(x, y1, 'r-o', label='SMT Sorted Relative')
pylab.plot(x, y2, 'b-o', label='SMT Sorted Rigid')
pylab.plot(x, y2, 'g-o', label='SMT No Condensing')
pylab.legend(loc='upper left')
pylab.ylim(-1.5, 2.0)
pylab.show()


pylab.plot(x, y1, 'r-o', label='SMT Sorted Relative')
pylab.plot(x, y2, 'b-o', label='SMT Sorted Rigid')
pylab.legend(loc='upper left')
pylab.ylim(-1.5, 2.0)
pylab.show()


import numpy as np
import pylab 
x = np.linspace(0, 20, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

pylab.plot(x, y1, 'r-o', label='Brute Force')
pylab.plot(x, y2, 'b-o', label='SMT Solver')
pylab.plot(x, y2, 'g-o', label='Dynamic Algorithm')
pylab.legend(loc='upper left')
pylab.ylim(-1.5, 2.0)
pylab.show()



pylab.plot(x, y2, 'b-o', label='SMT Solver')
pylab.plot(x, y2, 'g-o', label='Dynamic Algorithm')
pylab.legend(loc='upper left')
pylab.ylim(-1.5, 2.0)
pylab.show()



pylab.plot(x, y2, 'b-o', label='SMT Solver')
pylab.legend(loc='upper left')
pylab.ylim(-1.5, 2.0)
pylab.show()