# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 13:47:50 2021

@author: Duela
"""

import numpy as np
from scipy.spatial.transform import Rotation as rot
import datetime
from skyfield.api import Loader, EarthSatellite
from skyfield.timelib import Time
from skyfield.api import EarthSatellite, Topos
import skyfield.api


from skyfield.timelib import Time
import matplotlib.pyplot as plt



TLE_file = "A_GNSS_2020_10_07.txt"
with open(TLE_file, "rt") as f:    # Opening Txt file
  TLE_data = f.read()              # Reading Txt file
    
TLE_data = TLE_data.split("\n")    # Spliting Txt file  
 
tle = []
for i in range(0, len(TLE_data), 3):    # Txt file has a 318 lines 
    name = {}
    tle.append({
         "satellite":EarthSatellite(TLE_data[i+1], TLE_data[i+2], TLE_data[i]), 
         "name":TLE_data[i], "1":TLE_data[i+1], "2":TLE_data[i+2],
         })
    
Time_range = skyfield.api.load.timescale()
Th = Time_range.utc(2020, 10, 6, 0, range(0, 1440, 1), 0)   # 24 hrs Time interval
                
Th = Time_range.tt_jd(Th.tt-0.125)
T = 24*(Th-Th[0])
Seconds = 1./24/3600
th = Time_range.tt_jd(Th.tt+Seconds)
my_loc = Topos('54.6872 N', '25.2797 E')      # Vilnius Coordinates
Fre = 1575.42e6                               # GNSS L1 band center frequency
C = 3e8                                       # Speed of light
name = "name"
CL = "Current Velocity"
VL = "Relative Velocity"
doppler = "Doppler Frequency"

for i in range(len(tle)):
    satellite = tle[i]['satellite']
    rel_pos = (satellite - my_loc).at(Th)     # Initial position
    rel_pos2 = (satellite - my_loc).at(th)    # Position after ine second
    
    alt, az, distance = rel_pos.altaz()
    I = np.where(alt.degrees < 0)
    D = rel_pos.position.km
    D1 = rel_pos2.position.km
    Dn = np.linalg.norm(D,axis=0)
    Dn1 = np.linalg.norm(D1,axis=0)
    Vrx = Dn-Dn1                             # Relative velocity
    Doppler = (Fre*Vrx)/C                    # To calculate Doppler shift
    
    Vrx[I] = None;
    Doppler[I] = None
    tle[i][VL] = Vrx
    tle[i][doppler] = Doppler
    
print("Orbital calculation finished")

# To Plot Doppler shift against Time

import pylab as plt
from matplotlib.transforms import Bbox
plt.figure(2, dpi = 150)
plt.clf()
for i in range(len(tle)):
  plt.plot(T, tle[i][doppler], linewidth = 0.75, linestyle = 'dashed', label = tle[i-0][name] )

current_handles, current_labels = plt.gca().get_legend_handles_labels()
reversed_handles = list(reversed(current_handles))
reversed_labels = list(reversed(current_labels))
plt.gca().legend(loc='center left', bbox_to_anchor=(0.98, 0.6))
# Create empty plot with blank marker containing the extra label

plt.xlim(0, 24)
plt.ylim(-8, 8)
plt.xlabel('Time, hours', fontsize=9)
plt.ylabel(' Doppler, (Khz)', fontsize=9)
plt.grid()

# To Relative velocity against Time
import pylab as plt
plt.figure(1, dpi = 150)
plt.clf()
oversize_policy = None     # what there is now
oversize_policy = "hide"   # what is added short term
oversize_policy = "popup"  # for the future

for i in range(len(tle)):
  plt.plot(T, tle[i][VL], linewidth = 1, label = tle[i-0][name] )

current_handles, current_labels = plt.gca().get_legend_handles_labels()
reversed_handles = list(reversed(current_handles))
reversed_labels = list(reversed(current_labels))
plt.gca().legend(loc='center left', bbox_to_anchor=(0.98, 0.6))
# Create empty plot with blank marker containing the extra label


plt.xlim(0, 24)
plt.xlabel('Time, hours', fontsize=9)
plt.ylabel(' Vr, (Km/s)', fontsize=9)
plt.grid()





