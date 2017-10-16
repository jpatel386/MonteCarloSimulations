import random
import math
from scipy import stats
import matplotlib.pyplot as plt

todp = 7250.0
yesp = 7260.0
stChange = 0
dates = []


def genran():
    randnum = random.randint(1, 100)
    return float(randnum)/100.0


def drift():
    r = math.log(todp/yesp, math.e)
    tomp = todp*math.exp(r)
    return tomp


def stoch():
    randperc = genran()
    zscore = stats.norm.ppf(randperc)
    return zscore


# tomp = todp+stoch
# print tomp

numdays = range(-20,0)
#tdays = ["t" + `i` for i in numdays]
#tdays.extend(["t","t+1","t+2","t+3","t+4"])
print numdays

priceopen = [7401.46, 7337.43, 7365.26, 7430.62, 7438.50, 7411.47, 7372.92, 7354.13, 7396.98, 7377.60,
             7413.59, 7400.69, 7379.70, 7295.39, 7215.47, 7253.28, 7275.25, 7271.95, 7263.90, 7310.64]

pricehigh = [7401.62, 7381.33, 7443.68, 7460.52, 7438.50, 7437.51, 7372.92, 7412.68, 7396.98, 7434.07,
             7435.84, 7401.30, 7390.70, 7295.39, 7257.45, 7285.67, 7289.93, 7289.16, 7320.28, 7312.45]


pricelow = [7289.20, 7337.43, 7365.01, 7430.06, 7404.05, 7369.58, 7322.42, 7348.38, 7358.42, 7377.60,
            7386.98, 7336.23, 7287.73, 7196.58, 7215.47, 7243.59, 7249.58, 7260.05, 7242.23, 7272.49]

priceclose = [7337.43, 7365.26, 7430.62, 7438.50, 7411.47, 7372.92, 7354.13, 7396.98, 7377.60, 7413.59,
              7400.69, 7379.70, 7295.39, 7215.47, 7253.28, 7275.25, 7271.95, 7263.90, 7310.64, 7301.29]

longlist = [priceopen,pricehigh,pricelow,priceclose]

avgprice = [round(((w+x+y+z)/4),2) for w,x,y,z in zip(*longlist)]

print avgprice

plt.plot(numdays,avgprice,)

plt.show()
