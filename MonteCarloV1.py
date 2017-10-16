import random
import math
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import subprocess

futuredays = 40
predictions = 3


process1 = subprocess.call("/Users/JezzBhai/PycharmProjects/MonteCarloSimulations/ftseprices.sh")

f = open('/users/JezzBhai/PycharmProjects/MonteCarloSimulations/final.file', "r")
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


count = 0

while count < futuredays:
    avgprice.append(avgprice[-1] * math.exp(drift() + np.sqrt(varr()) * stoch()))
    count += 1

process2 = subprocess.call("/Users/JezzBhai/PycharmProjects/MonteCarloSimulations/ftsedel.sh")


numconfdays = range(-len(priceclose)-futuredays+1, -futuredays+1, 1)
numtotdays = range(-len(avgprice)+1, 1)
plt.xlabel('Date (Days)')
plt.ylabel('Index')
plt.title('FTSE 100 Index', loc='right')
plt.plot(numtotdays, avgprice, 'r', label='Future')
plt.plot(numconfdays, avgprice[0:64], 'black', label='Previous')
plt.legend()
plt.show()
