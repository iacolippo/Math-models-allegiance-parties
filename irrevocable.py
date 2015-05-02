'''Irrevocable supporters model - non linear dynamics simulation 
    Copyright (C) 2015  Iacopo Poli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from paperlib import randomic
plt.ion()

N = 1000 # population sample
density = 35.5 # density per squared km of population
influence_area= 100 # squared kilometer of efficacy

# defining and printing random constants
a1 = randomic(N, density, influence_area)
a2 = randomic(N, density, influence_area)

print 'a1=', a1
print 'a2=', a2

# defining system of equations
def f(y, t):
        S = y[0]
        L1 = y[1]
        L2 = y[2]
        # model equations
        f0 = -a1*S*L1-a2*S*L2           
        f1 = a1*S*L1                         
        f2 = a2*S*L2                         
        return [f0, f1, f2]

# initial conditions
S = N-2               # initial population of susceptibles
L1 = 1                  # initial loyal to party 1 population
L2 = 1                  # initial loyal to party 2 population
y0 = [S, L1, L2]       # initial condition vector
t  = np.linspace(0, 3., 100)   # time grid in months

# solve the ODEs
soln = odeint(f, y0, t)
S = soln[:, 0]
L1 = soln[:, 1]
L2 = soln[:, 2]

# plot results
plt.figure()
plt.plot(t, S/N, label='Susceptibles')
plt.plot(t, L1/N, label='Loyal 1')
plt.plot(t, L2/N, label='Loyal 2')
plt.xlabel('Months from start of the campaign')
plt.ylabel('Population')
plt.title('Campaign - No Init. Pop. of Loyals')
plt.legend(loc=0)
plt.autoscale(enable=True, axis='both', tight=None)
plt.pause(120)
