'''Functions used in other programs for non linear dynamics simulation 
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

import random as rnd

#randomic takes population, density of population per squared kilometer and area of influence in squared kilometers
#and returns a coefficient of conversion per unit time

def randomic(pop, avg, area):

    deviation = float(rnd.randint(1,10))/100 #average deviation in elections
    
    rand_a = (avg*area/float(pop))*deviation
    return rand_a