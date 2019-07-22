import sympy as syp
#from sympy import Symbol
#from scipy.special import ellipk, ellipe, ellipkm1
from numpy import pi, sqrt, linspace
from pylab import plot, xlabel, ylabel, suptitle, legend, show

uo = 4E-7*pi     # Permeability constant - units of H/m
x = syp.Symbol('x')
Bo = lambda i, a, u=uo: i*u/(2*a)    # Central field = f(current, loop radius, perm. constant)
al = lambda r, a: r/a               # Alpha = f(radius of measurement point, radius of loop)
be = lambda x, a: x/a               # Beta = f(axial distance to meas. point, radius of loop)
ga = lambda x, r: x/r               # Gamma = f(axial distance, radius to meas. point)
Q = lambda r, x, a: (1 + al(r,a))**2 + be(x,a)**2   # Q = f(radius, distance to meas. point, loop radius)
k = lambda r, x, a: syp.sqrt(4*al(r,a)/Q(r,x,a))       # k = f(radius, distance to meas. point, loop radius)
K = lambda k: syp.elliptic_f(pi/2,k**2.0)          # Elliptic integral, first kind, as a function of k
E = lambda k: syp.elliptic_e(pi/2,k**2.0)          # Elliptic integral, second kind, as a function of k

N = 10;
lc = 0.065;
# Axial field component by a solenoid
def BxSol(i, a, r):
    pitch = lc/N;
    fBx = 0;
    for j in range(int(N)):
        Bxtemp = (Bo(i,a)*\
        (E(k(r,x-j*pitch,a))*((1.0-al(r,a)**2-be(x-j*pitch,a)**2)/(Q(r,x-j*pitch,a)-4*al(r,a))) + K(k(r,x-j*pitch,a))))\
        /pi/syp.sqrt(Q(r,x-j*pitch,a));

        fBx = fBx + Bxtemp;
    return fBx

# Axial field component = f(current and radius of loop, r and x of meas. point)
def Bx(i, a, r):
    if r == 0:
        return Baxial(i,a)         # axial field
    else:                          # axial component, any location
        return Bo(i,a)*\
            (E(k(r,x,a))*((1.0-al(r,a)**2-be(x,a)**2)/(Q(r,x,a)-4*al(r,a))) + K(k(r,x,a)))\
            /pi/syp.sqrt(Q(r,x,a))

# Radial field component = f(current and radius of loop, r and x of meas. point)
def Br(i, a, r):
    if r == 0:
        return 0                   # no radial component on axis!
    else:                          # radial component, any location other than axis.
        return Bo(i,a)*ga(x,r)*\
            (E(k(r,x,a))*((1.0+al(r,a)**2+be(x,a)**2)/(Q(r,x,a)-4*al(r,a))) - K(k(r,x,a)))\
            /pi/sqrt(Q(r,x,a))
