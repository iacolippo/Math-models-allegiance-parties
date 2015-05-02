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
from networkx.algorithms.approximation import clique

n = 250
x = (math.log(n))
l = int(round(math.log(x), 0)) 			#scalefree are ultra-smallworld network with L prop to loglogN
p = 0.1
k = 3

q1=0.65 #green threshold party1
q2=0.75 #red threshold party2
#susceptibles = blue

def init():
	global g, positions
    
	g = nx.connected_watts_strogatz_graph(n, l, p, tries=100, seed=None) #WS connected graph generator
	#g = nx.barabasi_albert_graph(n, l, seed=None)						 #BA graph generator (can be non-connected)
	critical = nx.betweenness_centrality(g)
	keynodes = critical.values()
	flag = 0
	for nd in g.nodes_iter():
		if keynodes[nd]>0.43: 							#average value of ten highest bc over repeated iterations for WS
		#if keynodes[nd]<0.0001: 						#average value of ten highest bc over repeated iterations for BA
			g.node[nd]['state'] = rnd.choice([1, 2])
		else:
			g.node[nd]['state'] = 0 
	
	positions = nx.circular_layout(g)       #for WS networks
	#positions = nx.spectral_layout(g)      #for BA networks

def draw():
    PL.cla()
    nx.draw(g, with_labels = False, pos = positions,
            node_color = [g.node[n]['state'] for n in g.nodes_iter()],
            vmin = 0, vmax = k - 1, cmap = PL.cm.jet)
				
def mystep():
	global g
	for n in g.nodes_iter():
		listener = g.nodes()[n]
		neighbourhood = g.neighbors(listener)
		if neighbourhood != []:
			flag_party1 = 0
			flag_party2 = 0
			for nd in neighbourhood:
				if g.node[nd]['state'] == 1:
					flag_party1 = flag_party1+1
				if g.node[nd]['state'] == 2:
					flag_party2 = flag_party2+1
			if flag_party1+flag_party2 != 0:
				if flag_party1/float(flag_party1+flag_party2) > q1:
					g.node[listener]['state'] = 1
				if flag_party2/float(flag_party1+flag_party2) > q2:
					g.node[listener]['state'] = 2	
    
import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,mystep])
