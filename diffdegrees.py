'''This program simulates Different degrees model described in "Mathematical modeling of 
	allegiance to political parties", Iacopo Poli, 2015
	
    Copyright (C) 2015 - Iacopo Poli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
    
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from paperlib import randomic
plt.ion()

N = 1000 # population sample
density = 35.5 # density per squared km of population
influence_area= 100 # squared kilometer of efficacy

#defining random constants

#fidelity rates
a1 = randomic(N, density, influence_area)
a2 = randomic(N, density, influence_area)
#rates of return
b1 = randomic(N, density, influence_area)
b2 = randomic(N, density, influence_area)
#rates of exchange
s1 = randomic(N, density, influence_area)
s2 = randomic(N, density, influence_area)
#rates of extremism
c1 = randomic(N, density, influence_area)
c2 = randomic(N, density, influence_area)
#rate of moderation
d1 = randomic(N, density, influence_area)
d2 = randomic(N, density, influence_area)

print 'a1:', a1
print 'a2:', a2
print 'b1:', b1
print 'b2:', b2
print 's1:', s1
print 's2:', s2
print 'c1:', c1
print 'c2:', c2
print 'd1:', d1
print 'd2:', d2

#defining system of equations
def f(y, t):
        S = y[0]
        ML1 = y[1]
        ML2 = y[2]
        WL1 = y[3]
        WL2 = y[4]
        
        # the model equations
        f0 = -a1*ML1*S-a2*ML2*S+b1*ML1*S+b2*ML2*S                        
        f1 = a1*ML1*S-b1*ML1*S+s1*ML1*ML2-s2*ML1*ML2+c1*ML1*WL1-d1*ML1*WL1
        f2 = a2*S*ML2-b2*ML2*S-s1*ML1*ML2+s2*ML1*ML2+c2*ML2*WL2-d2*ML2*WL2
        f3 = -c1*ML1*WL1+d1*ML1*WL1
        f4 = -c2*ML2*WL2+d2*ML2*WL2              
        return [f0, f1, f2, f3, f4]

# initial conditions
S = N-4               # initial population
ML1 = 1                 
ML2 = 1                 
WL1 = 1
WL2 = 1
y0 = [S, ML1, ML2, WL1, WL2]       # initial condition vector
t  = np.linspace(0, 3., 100)   # time grid in months

# solve the ODEs
soln = odeint(f, y0, t)
S = soln[:, 0]
ML1 = soln[:, 1]
ML2 = soln[:, 2]
WL1 = soln[:, 3]
WL2 = soln[:, 4]

# plot results
plt.figure()
plt.plot(t, S, label='Susceptibles')
plt.plot(t, ML1, label='Mildly Loyal 1')
plt.plot(t, ML2, label='Mildly Loyal 2')
plt.plot(t, WL1, label='Wildly Loyal 1')
plt.plot(t, WL2, label='Wildly Loyal 2')
plt.xlabel('Months from start of the campaign')
plt.ylabel('Population')
plt.title('Campaign - No Init. Pop. of Loyals')
plt.legend(loc=0)
plt.pause(120)

