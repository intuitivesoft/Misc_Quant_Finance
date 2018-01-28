''' Leisen-Reimer american option valuation and greeks '''
''' First version: 27/12/17 RG'''

import utils
import math

#Returns Leisen-Reimer American option value and delta
# r is the ctsly compounded interest rate to t
# n is the number of steps: odd number chosen for better convergence
def lropt(cp, F, S, K, t, sig, r, n = 101):

    dt = t / float(n)
    cumfac = math.log(F/S) / n
    cumfac = math.exp(cumfac)

    vt = sig * math.sqrt(t)
    d1 = (math.log(F / K) + 0.5 * (vt**2)) / vt
    d2 = d1 - vt
    pdm = pz(n, d2)
    pdp = pz(n, d1)

    u = cumfac * pdp / pdm
    D = (cumfac - pdm * u) / (1 - pdm)
    p = pdm

    f = [[0 for x in range(n+1)] for y in range(n+1)]
    for j in range(n+1):
        f[n][j] = max(cp * (-K + S *(u ** j) *(D ** (n - j))), 0)

    for i in range(n-1, -1, -1):
        for j in range(i+1):
            f[i][j] = math.exp(-r * dt) * (p * f[i + 1][j + 1] + (1 - p) * f[i + 1][j])
            f[i][j] = max(f[i][j], cp * (-K + S * (u ** j) * (D ** (i - j))))

    value = f[0][0]
    delta = ((f[1][1] - f[1][0]) / (S * (u - D)))
    return (value, delta)

#Returns Leisen-Reimer European option value and delta
def lropt_eur(cp, F, S, K, t, sig, r, n = 101):

    dt = t / float(n)
    cumfac = math.log(F/S) / n
    cumfac = math.exp(cumfac)

    vt = sig * math.sqrt(t)
    d1 = (math.log(F / K) + 0.5 * (vt**2)) / vt
    d2 = d1 - vt
    pdm = pz(n, d2)
    pdp = pz(n, d1)

    u = cumfac * pdp / pdm
    D = (cumfac - pdm * u) / (1 - pdm)
    p = pdm

    f = [[0 for x in range(n+1)] for y in range(n+1)]
    for j in range(n+1):
        f[n][j] = max(cp * (-K + S *(u ** j) *(D ** (n - j))), 0)

    for i in range(n-1, -1, -1):
        for j in range(i+1):
            f[i][j] = math.exp(-r * dt) * (p * f[i + 1][j + 1] + (1 - p) * f[i + 1][j])
            #f[i][j] = max(f[i][j], cp * (-K + S * (u ** j) * (D ** (i - j))))

    value = f[0][0]
    delta = ((f[1][1] - f[1][0]) / (S * (u - D)))
    return (value, delta)

# Gamma: returns discounted value
#take central difference: blip is in bps
#
def lropt_gamma(cp, f, s, x, t, v, r, n = 101, blip_BPS = 10.0):

    #derivative wrt spot
    blip = 0.5 * blip_BPS * s / 10000.0

    #delta up and down
    b = lropt(cp, f, s, x, t, v, r, n)[0]
    b_up = lropt(cp, f, s + blip, x, t, v, r, n)[0]
    b_dn = lropt(cp, f, s - blip, x, t, v, r, n)[0]

    #gamma
    bg = (b_up - 2.0 * b + b_dn) / (blip ** 2)
    bg *= (s / 100.0)

    return bg

# Vega: returns discounted value
#take central difference: blip is in bps
#
def lropt_vega(cp, f, s, x, t, v, r, n = 101, blip_BPS = 100.0):

    #derivative wrt spot
    blip = 0.5 * blip_BPS / 10000.0

    b = lropt(cp, f, s, x, t, v, r, n)[0]
    b_up = lropt(cp, f, s, x, t, v + blip, r, n)[0]
    b_dn = lropt(cp, f, s, x, t, v - blip, r, n)[0]

    #vega
    vega = (b_up - b_dn)

    ##volgamma
    #bg = (b_up - 2.0 * b + b_dn) / (blip ** 2);

    return vega

# Theta in forward space: returns undiscounted value
# takes days to expiry, not yearfrac
# returns decay (i.e. negative)
def lropt_theta(cp, f, s, x, dte, v, r, n = 101, blip_BPS = 100.0):

    t = float(dte) / 365.25
    b = lropt(cp, f, s, x, t, v, r, n)[0]

    t1 = (float(dte) - 1.0)/365.25
    b1 = lropt(cp, f, s, x, t1, v, r, n)[0]

    #theta
    theta = (b1 - b)

    return theta

#helper for Leisen Reimer
def pz(n, z):
    expterm = (z / (n + 1 / 3)) ** 2
    expterm = math.exp(-expterm * (n + 1 / 6))
    nxtterm = 0.5 + utils.sign(z) * 0.5 * math.sqrt(1 - expterm)
    return nxtterm
