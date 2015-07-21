#!/usr/bin/env python
from obspy.core import read, Stream, UTCDateTime
import glob
import numpy as np
import matplotlib.pyplot as plt
import sys
from obspy.signal.trigger import zDetect, plotTrigger
from response_spectrum import ResponseSpectrum, NigamJennings, plot_response_spectra, plot_time_series
import sm_utils


#Need to add comments to this code

debug = True

files = glob.glob('data/*')

st = Stream()
for curfile in files:
	st+=read(curfile)

#Make everything overlap and nice
st._cleanup()
st.sort(['network','station','channel','starttime'])


pers = np.linspace(0.01, 20, 300)
for idx, tr in enumerate(st):
	tr.detrend('demean')
	tr.taper(max_percentage=0.05, type='cosine')
	tr.data = tr.data
	tr.filter('highpass',freq=1.0)
	rs = NigamJennings(tr.data,1/tr.stats.sampling_rate,pers,damping=0.5, units="m/s/s")
	spec, ts, acc, vel, dis = rs.evaluate()
	fig = plt.figure(1, figsize=(8,8))
	plt.loglog(spec["Period"],spec["Pseudo-Acceleration"]*0.1/9.81,'k',linewidth=2)
	plt.xlim([.1, 10])
	plt.xlabel('Period (s)', fontsize=18)
	plt.ylabel('Acceleration (g)', fontsize=18)
	plt.title('QCN Pseudo-Acceleration Response Spectra', fontsize=18)
	plt.tick_params(labelsize=18)
	
plt.savefig(filename='ALLPSD.jpg',format='jpeg',dpi=400)
#plt.show()
	
	



balh=plot_response_spectra(spec,filename='Spec' + tr.stats.station + tr.stats.channel + tr.stats.starttime.formatIRISWebService() + ".png")
balh=plot_time_series(ts['Acceleration'],1/tr.stats.sampling_rate,velocity=ts['Velocity'],displacement=ts['Displacement'],filename='TS' + tr.stats.station + \
    tr.stats.channel + tr.stats.starttime.formatIRISWebService() + ".png")

		






