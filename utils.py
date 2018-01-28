''' Miscellaneous (static) utility functions '''
''' Second version: 17/12/17 RG'''

import math
from datetime import datetime, timedelta

# reads a textfile with 2 columns (stks, vols)
#returns tuple (stks, vols), components are lists
def readvols(filename):
    with open(filename) as textFile:
        lines = [line.split() for line in textFile]
    stks = [i[0] for i in lines]
    vols = [i[1] for i in lines]
    return stks, vols

#returns the #days between 2 dates
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#add n days to
def add_days(d, n):
    d = datetime.strptime(d, "%Y-%m-%d")
    d = d + timedelta(days = n)
    return d

#returns yearfrac between 2 dates
#refdate = 0 => today
def voltenor(voldate, refdate = 0):
    vd = datetime.strptime(voldate, "%Y-%m-%d")
    rd = 0
    if(refdate == 0): #current date
        rd = datetime.today()
        rd = rd.replace(hour=0, minute=0, second=0, microsecond= 0)
    else:
        rd = datetime.strptime(refdate, "%Y-%m-%d")
    return abs((vd - rd).days)/365.25

def sign(x):
    return math.copysign(1, x)
