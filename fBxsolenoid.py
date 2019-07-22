# This is a program for finding the functional form of component of B parallel to axis at any radial distance
import fBcalc
from sympy import *
from sympy.plotting import plot

x = Symbol('x');
expr = fBcalc.BxSol(108,0.01225,0.007); #i,a,r in order where i= current, a= radius of coil, r= distance from center
print(expr)
plot(expr,(x,-0.04,0.11),xlabel ='Radial distance from the centre of coil (m)',ylabel = 'Magnetic field strength (T)',title='Axial component of magnetic field for i = 104 A, radius of coil= 1.225 cm and at a distance of 4 mm from center' )
