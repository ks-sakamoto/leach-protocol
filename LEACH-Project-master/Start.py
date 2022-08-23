# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 21:16:40 2022

@author: KIRAN
"""

import sys

sys.path.append("src")

from LEACH import LEACHSimulation
from LEACH_graphs import Energy_graph,LifeTime_graph


Leach_obj=LEACHSimulation(n=100)
Leach_obj.start()

Energy_graph(Leach_obj).plot_energy_graph()
LifeTime_graph(Leach_obj).plot_lifetime_graph()
