"""PyCX 0.31
Complex Systems Simulation Sample Code Repository

2008-2013 (c) Copyright by Hiroki Sayama
2012 (c) Copyright by Chun Wong & Hiroki Sayama
         ("pycxsimulator-old.py", "realtime-simulation-template-old.py")
2013 (c) Copyright by Przemyslaw Szufel & Bogumil Kaminski
         Extensions to GUI module, some revisions
All rights reserved.


This software is being distributed under the following Simplified BSD
(FreeBSD) license.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
"""

import matplotlib
matplotlib.use('TkAgg')

import networkx as nx
import random as rnd
import pylab as PL
import math
from paperlib import sum_vector

n = 250
x = (math.log(n))
l = int(round(math.log(x), 0)) 			#scalefree are ultra-smallworld network with L prop to loglogN
p = 0.1
k = 5

q1 = 0.10 #mildly1 light blue
q2 = 0.15 #mildly2 orange
b1 = 0.35
b2 = 0.20
s1 = 0.1
s2 = 0.3
c1 = 0.2 
d1 = 0.8 #wildly1 green
c2 = 0.1
d2 = 0.5 #wildly2 red
#susceptibles = blue

def init():
	global g, positions
    
	g = nx.connected_watts_strogatz_graph(n, l, p, tries=100, seed=None) #WS connected graph generator
	#g = nx.barabasi_albert_graph(n, l, seed=None)						 #BA graph generator (can be non-connected)
	critical = nx.betweenness_centrality(g)
	keynodes = critical.values()
	
	for nd in g.nodes_iter():
		if keynodes[nd]>0.43: 							#average value of ten highest bc over repeated iterations for WS
		#if keynodes[nd]<0.0001: 						#average value of ten highest bc over repeated iterations for BA
			g.node[nd]['state'] = rnd.choice([1, 2, 3, 4])
		else:
			g.node[nd]['state'] = 0 
	
	positions = nx.circular_layout(g)       #for WS networks
	#positions = nx.spectral_layout(g)      #for BA networks

def draw(): #draws the graph
    PL.cla()
    nx.draw(g, with_labels = False, pos = positions,
            node_color = [g.node[n]['state'] for n in g.nodes_iter()],
            vmin = 0, vmax = k - 1, cmap = PL.cm.jet)
				
def mystep():
	global g
	for n in g.nodes_iter():
	
		listener = g.nodes()[n] #for each cycle a node becomes the listener
		neighbourhood = g.neighbors(listener) #neighborhood is defined
		
		if neighbourhood != []: #checks if neighborhood isn't empty
			
			flag_mp1 = 0
			flag_mp2 = 0
			flag_wp1 = 0
			flag_wp2 = 0
			flag_s = 0
			
			check = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 	#checks for satisfied thresholds
			thresholds = [b1, b2, q1, q2, s1, s2, c1, c2, d1, d2]	#thresholds vector
		
			for nd in neighbourhood:	#checks states of neighbors
				if g.node[nd]['state'] == 0:
					flag_s = flag_s+1
				if g.node[nd]['state'] == 1:
					flag_mp1 = flag_mp1+1
				if g.node[nd]['state'] == 2:
					flag_wp1 = flag_wp1+1
				if g.node[nd]['state'] == 3:
					 flag_mp2 = flag_mp2+1
				if g.node[nd]['state'] == 4:
					flag_wp2 = flag_wp2+1
			
			if g.node[n]['state'] == 1 and flag_s/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > b1:
				g.node[n]['state'] = 0
				check[0] = 1
			elif g.node[n]['state'] == 3 and flag_s/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > b2:
				g.node[n]['state'] = 0
				check[1] = 1
			elif g.node[n]['state'] == 0 and (flag_mp1+flag_wp1)/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > q1:
				g.node[listener]['state'] = 1
				check[2] = 1
			elif g.node[n]['state'] == 0 and (flag_mp2+flag_wp2)/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > q2:
				g.node[listener]['state'] = 3
				check[3] = 1
			elif g.node[n]['state'] == 1 and (flag_mp2+flag_wp2)/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > s2:
				g.node[n]['state'] = 3
				check[4] = 1
			elif g.node[n]['state'] == 3 and (flag_mp1+flag_wp1)/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > s1:
				g.node[n]['state'] = 1
				check[5] = 1
			elif g.node[n]['state'] == 2 and flag_mp1/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > c1:
				g.node[n]['state'] = 1
				check[6] = 1
			elif g.node[n]['state'] == 4 and flag_mp2/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > c2:
				g.node[n]['state'] = 3
				check[7] = 1
			elif g.node[n]['state'] == 1 and flag_wp1/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > d1:
				g.node[n]['state'] = 2
				check[8] = 1
			elif g.node[n]['state'] == 3 and flag_wp2/float(flag_mp1+flag_mp2+flag_wp1+flag_wp2+flag_s) > d2:
				g.node[n]['state'] = 4
				check[9] = 1
			
			#if more than one threshold is satisfied, chooses the one with lowest threshold
			if sum_vector(check, len(check)) > 1:
				
				for n in range(0, len(check)):
					if check[n] == 1:
						check[n] = thresholds[n]
				
				check.sort()
				
				if check[0] == b1 or check[0] == b2:
					g.node[listener]['state'] = 0
				elif check[0] == q1 or check[0] == s1 or check[0] == c1:
					g.node[listener]['state'] = 1
				elif check[0] == q2 or check[0] == s2 or check[0] == c2:
					g.node[listener]['state'] = 3
				elif check[0] == d1:
					g.node[listener]['state'] = 2
				elif check[0] == d2:
					g.node[listener]['state'] = 4
    
import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,mystep])