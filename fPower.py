import math
import fBcalc
from sympy import *
import numpy as np
from scipy import special, integrate, linspace
import xlrd
import xlwt
import pandas as pd
from xlutils.copy import copy

def trap(y, x):
    pow_int = np.trapz(y, x);
    return pow_int

def simp(y,x):
    pow_int = integrate.simps(y,x);
    return pow_int

x = Symbol('x');
# Input variables
lc = 0.0635;
rc = 0.01225;
#dw = float(input('Enter the diameter of workpiece \n'));
#lw = float(input('Enter the length of workpiece \n'));
# f = frequency
# i = current
def power(lw,dw,i,f):

    rw = dw/2;
    Bx = fBcalc.BxSol(i,rc,rw); #i,a,r in order where i= current, a= radius of coil, r= distance from center
    rho_cg = 3.25*10**(3);
    rho_si = 3.25*10**(-8)  #Reference https://www.engineeringtoolbox.com/resistivity-conductivity-d_418.html
    # Calculation for derived variables
    rw = rw*100;
    ur = 1;
    u = ur*4*math.pi*10**(-7);
    k = math.sqrt((8*(math.pi**2)*f*ur)/rho_cg);
    #print(k*rw)
    Q = 2*(special.ber(k*rw)*special.berp(k*rw) + special.bei(k*rw)*special.beip(k*rw))\
        /(k*rw)/((special.ber(k*rw))**2 + (special.bei(k*rw))**2);
    rw = rw/100;
    print(k)
    new_k = math.sqrt(2*math.pi*u*f/rho_si)
    print(new_k)
    aw = math.pi*rw*rw;
    beta = math.pi*f*aw*Q/(u);    #beta is a constant and total power is beta times Bx**2 integrated
                                  #over the length of the workpiece

    # Bx involves ellipticl integrals of the first kind and the second kind and
    # its analytical integral is not possible using python

    # Approach: Evaluate Bx at a set number of points and implement different types of
    # numerical integration methods like simpsons, trapezoidal etc.

    # Maybe define a good criteria of how many points to take versus the computation power consumed for evaluating the numerical integrals
    # Origin redefined to the center of end coil of the solenoid

    # Defining linspace in such a way that the distance between two points in the workpiece remains fixed to an order where Bx doesn't change significantly
    # i.e. lw/(number of points) = constant -- this is not the best way because derivative of Bx is large near the end of coil and linspace is constant
    # distance between each successive x points be 0.0001 m

    num_pts = int(lw/0.0003)
    x_arr = linspace((lc-lw)/2,(lc+lw)/2,num = num_pts);
    Bx_sq_arr = np.empty(num_pts, dtype='float')

    for i in range(num_pts):
        temp = Bx.subs(x,x_arr[i]);
        Bx_sq_arr[i] = temp**2;

    P = beta* trap(Bx_sq_arr,x_arr)
    rate = P/(lw*2700*math.pi*rw*rw*910)

    return rate

def heatrate(lw,dw,i,f):
        rw = dw/2;
        rate = [0,0]
        Bx = fBcalc.BxSol(i,rc,rw); #i,a,r in order where i= current, a= radius of coil, r= distance from center
        rho_cg = 3.57*10**(3);
        rho_si = 3.57*10**(-8)  #Reference https://www.engineeringtoolbox.com/resistivity-conductivity-d_418.html
        # Calculation for derived variables
        rw = rw*100;
        ur = 1;
        u = ur*4*math.pi*10**(-7);
        k = math.sqrt((8*(math.pi**2)*f*ur)/rho_cg);
        #print(k*rw)
        Q = 2*(special.ber(k*rw)*special.berp(k*rw) + special.bei(k*rw)*special.beip(k*rw))\
            /(k*rw)/((special.ber(k*rw))**2 + (special.bei(k*rw))**2);
        rw = rw/100;
        new_k = math.sqrt(2*math.pi*u*f/rho_si)
        #print(new_k*rw)
        aw = math.pi*rw*rw;
        beta = math.pi*f*aw*Q/(u);
        rate[0] = beta*(float(Bx.subs(x,lc/2)**2))/(2695*math.pi*rw*rw*952.177)
        rate[1] = beta*(float(Bx.subs(x,(lc-lw)/2)**2 + Bx.subs(x,(lc+lw)/2)**2)/2)/(2700*math.pi*rw*rw*929)
        return rate

def iterator(data):
    total = len(data.loc[:,'Height (mm)'].values)
    for ind in range(total):
        lw = data.loc[ind][0] * 10**(-3);
        dw = data.loc[ind][1] * 10**(-3);
        rw = dw/2
        i = data.loc[ind][2]/2;
        f = data.loc[ind][3]*1000;

        rate = power(lw,dw,i,f)
        # writing the data to final table

        rb = xlrd.open_workbook('/home/manan/Desktop/final_results.xlsx')
        r_sheet = rb.sheet_by_index(0)
        r = r_sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        sheet.write(r,0,label = lw * 10**3)
        sheet.write(r,1,label = dw * 10**3)
        sheet.write(r,2,label = rate)  ##Reference- The specifiv heat of aluminium from 330 to 890K
        #sheet.write(r,3,label = rate[1])

        wb.save('/home/manan/Desktop/final_results.xlsx')


data = pd.read_excel('/home/manan/Desktop/Inductionheating.xlsx')
iterator(data)
#print('The power for diameter ' + str(dw) + ' and length ' + str(lw) + ' is ',P);
#print('dT/dt is', P/(lw*2700*math.pi*rw*rw*929));   #Reference- The specifiv heat of aluminium from 330 to 890K
