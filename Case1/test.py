from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
money = [1.5, 2.5, 5.5, 2.0]


#def millions(x, pos):
    #'The two args are the value and tick position'
    #return '$%1.1fM' % (x * 1e-6)


#formatter = FuncFormatter(millions)

fig, ax = plt.subplots()
#ax.yaxis.set_major_formatter(formatter)
plt.bar(x, money)
plt.xticks(x, ('Bill', 'Fred', 'Mary', 'Sue'))
plt.show()
