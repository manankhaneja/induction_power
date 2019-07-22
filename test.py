import sympy as syp
x = syp.Symbol('x')
E = lambda x: syp.elliptic_e(pi/2,x)
I = integrate(E,x)
print(I)
