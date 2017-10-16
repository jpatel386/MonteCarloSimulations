import random
import math
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import urllib
from pathlib import Path
import time

futuredays = 10
predictions = 2


my_file = Path("Users/JezzBhai/PycharmProjects/MonteCarloSimulations/final.file")

if not my_file.is_file():
    urllib.urlretrieve('ftp://ja15a1l:8And4x0-h[c9z)a9X@81.19.186.141/final.file', 'final.file')

f = open('/Users/JezzBhai/PycharmProjects/MonteCarloSimulations/final.file', "r")
lines = f.readlines()

priceopenbef = []
pricehighbef = []
pricelowbef = []
priceclosebef = []

for x in lines:
    priceopenbef.append(x.split(' ')[4])
    pricehighbef.append(x.split(' ')[6])
    pricelowbef.append(x.split(' ')[7])
    priceclosebef.append(x.split(' ')[5].strip("\n"))
f.close()
priceopen = [round(float(i), 0) for i in priceopenbef]
pricehigh = [round(float(i), 0) for i in pricehighbef]
pricelow = [round(float(i), 0) for i in pricelowbef]
priceclose = [round(float(i), 0) for i in priceclosebef]

longlist = [priceopen, pricehigh, pricelow, priceclose]
avgprice = [round(((w+x+y+z)/4), 2) for w, x, y, z in zip(*longlist)]
avgprice.reverse()
rvar = []
avgdriftlist = []


def genran():
    randnum = random.uniform(0, 1)
    return randnum


def drift():
    for b in range(len(avgprice)):
        if b+1 >= len(avgprice):
            break
        else:
            r1 = math.log(avgprice[b+1]/avgprice[b], math.e)
            rvar.append(r1)
    varr1 = np.var(rvar)
    for a in rvar:
        avgdrift = a-(varr1/2)
        avgdriftlist.append(avgdrift)
    return float(sum(avgdriftlist)/len(avgdriftlist))


def stoch():
    randperc = genran()
    zscore = stats.norm.ppf(randperc)

    return zscore


def varr():
    for a in range(len(avgprice)):
        if a + 1 >= len(avgprice):
            break
        else:
            r = math.log(avgprice[a + 1] / avgprice[a], math.e)
            rvar.append(r)
    return np.var(rvar)


def col():
    return '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# tomp = avgprice[-1]*math.exp(drift() + np.sqrt(varr()) * stoch())

fut = [[] for x in range(predictions)]

i = 0
while i < predictions:

    for x in range(futuredays):
        if x == 0:
            fut[i].append(avgprice[-1] * math.exp(drift() + np.sqrt(varr()) * stoch()))
        else:
            fut[i].append(fut[i][-1] * math.exp(drift() + np.sqrt(varr()) * stoch()))

    i += 1
for x in range(predictions):
    fut[x][:0] = avgprice

plt.xlabel('Date (Days)')
plt.ylabel('Index')
plt.title('FTSE 100 Index', loc='right')

numconfdays = range(-len(priceclose) - futuredays + 1, -futuredays + 1, 1)
numtotdays = range(-len(fut[0]) + 1, 1)
xaxisprev = [x + futuredays for x in numconfdays]
xaxispred = [x + futuredays for x in numtotdays]

for x in range(len(fut)):
    plt.plot(xaxispred, fut[x], c=col())

plt.plot(xaxisprev, avgprice, 'black', label='Previous')

plt.plot(xaxisprev[-1], avgprice[-1], 'ro')

plt.axes().xaxis.set_minor_locator(MultipleLocator(1))
timestr = time.strftime("%Y%m%d-%H%M%S")

fname = "PREDVERSION" + timestr
plt.savefig(fname, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)

print "Script has run successfully. Happy gambling. T's & C's Apply. I am not responsible for any loss of money " \
      "based on information provided from my graphs."
