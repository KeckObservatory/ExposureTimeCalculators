#!/usr/bin/env python
# coding: utf-8

# In[1]:


## this is a python script to calculate NIRES S/N 
import numpy as np
import scipy.constants as sc
from astropy.io import ascii
import math


def do_calc(mag_src, #source magnitude 
            exp_time, #exposure time in seconds   
            coadds, #coadds
            dither, #dither pattern, ABBA or AB, num_dith = 4 or 2 
            dith_repeats, # repeats of dithering pattern
            obs_wave, #observation wavelength in um
            seeing, # in arcsec
            num_reads, #number of reads, 2 (CDS) or 16 (MCDS) 
            airmass, # 1.0, 1.5, 2.0
            water_vap_col # 1.0, 1.6, 3.0, 5.0
            ):




## etc web input parameters 

# mag_src = 18.2
# exp_time = 3600 #sec
# coadds = 1
# dither = "AB"
# dith_repeats = 1
# obs_wave = 2.2 #um
#obs_band = 'J'
# seeing = 0.8 #arcsec
# num_reads = 16 
# airmass = [1.0, 1.5, 2.0]
# water_vap_col = [1.0, 1.6, 3.0, 5.0]

## fixed instrument parameters
slit_width = 0.55 #arcsec
slit_lenth = 18.0 #arcsec
#mag_zero = {'J':25.0, 'H':25.0, 'K':25.0} #in vega, temporarily setting them to be the same

#read_noise = {'CDS':15, 'MCDS':5} #e-
dark_current = 0.01 #e-/s
throughput = ascii.read('/Users/syeh/Dropbox/keck/etc/nires/nires_throughput_18.dat')
tpt_wave = throughput[0][:]
tpt_val = throughput[1][:]
tpt_val_interp = np.interp(obs_wave, tpt_wave, tpt_val)
gain = 3.8 #e-/ADU
pix_size = 0.123 #arcsec/pix
collect_area = 76*1e4 # 76 m^2 = 76e4 cm^2
del_lmbd = obs_wave/2700/1e4 # cm
spatial_cov = (0.55*seeing)/(math.pi*seeing**2)
#num_pix = math.pi*(seeing/2)**2 / pix_size**2
num_pix_slt = 18*0.55/pix_size**2
num_pix_src = 0.55*seeing

## mauna kea IR sky bkg
IR_sky = ascii.read('/Users/syeh/Dropbox/keck/etc/IRsky/mk_skybg_zm_10_10_ph.dat')
sky_wave = IR_sky[0][:]/1000 # um
sky_bkg  = 1000*IR_sky[1][:] #photon/s/arcsec^2/cm/cm^2
sky_bkg_interp = np.interp(obs_wave, sky_wave, sky_bkg)

print(sky_bkg_interp)
print(tpt_val_interp)


# In[2]:


flux_src = np.power(10,-0.4*mag_src)/1e8 #input source flux in erg/s/cm^2/cm

photon_energy = sc.h*1e7*(sc.c*1e2)/(obs_wave*1e4) #single photon energy in erg

flux_src_phot = flux_src/photon_energy #source flux in photon/s/cm^2/cm

sig_src = flux_src_phot*collect_area*tpt_val_interp*del_lmbd*spatial_cov # source signal in e-/s 


if num_reads == 2:
    read_noise = 15 #CDS
elif num_reads == 16:
    read_noise = 5 #MCDS

#if dither == "AB":
#    num_dith = 2
#elif dither == "ABBA":
#     num_dith = 4
        
    
sig_src_int = sig_src*exp_time #source flux integrated over time, single frame
noise_int = (sig_src*exp_time + num_pix_slt*dark_current*exp_time + (num_pix_slt-num_pix_src)*sky_bkg_interp*exp_time + num_pix_slt*read_noise**2*exp_time)**(1/2) #noise, single frame

s2n = sig_src_int / noise_int # s/n, single frame

print("src flux", flux_src)
print("photon energy=", photon_energy)    
print("signal =", sig_src_int)     
print("noise =", noise_int)
print("S/N =", s2n)

#return final data dictionary result
 result = {}
 result['s2n'] = s2n
 return result

#This code below will only run if this module is run from the command line
# #example: python etc_nires.py
 if __name__ == "__main__":
 
#     #test
     def do_calc(mag_src, #source magnitude 
                 exp_time, #exposure time in seconds   
                 coadds, #coadds
                 dither, #dither pattern, ABBA or AB, num_dith = 4 or 2 
                 dith_repeats, # repeats of dithering pattern
                 obs_wave, #observation wavelength in um
                 seeing, # in arcsec
                 num_reads, #number of reads, 2 (CDS) or 16 (MCDS) 
                 airmass, # 1.0, 1.5, 2.0
                 water_vap_col # 1.0, 1.6, 3.0, 5.0
                 ):
     print ('result = ', data)
  


# 
# def do_calc(mag_src, #source magnitude 
#             exp_time, #exposure time in seconds   
#             coadds, #coadds
#             dither, #dither pattern, ABBA or AB, num_dith = 4 or 2 
#             dith_repeats, # repeats of dithering pattern
#             num_reads, #number of reads, 2 (CDS) or 16 (MCDS) 
#             obs_wave, # wavelenght of interest, useful for emission line obs
#             seeing #in arcsec, to calculate number of pixels on detector
#             ):
# 

# print("S/N =",s2n)
# 
# #return final data dictionary result
# result = {}
# result['s2n'] = s2n
# 
# #This code below will only run if this module is run from the command line
# #example: python etc_nires.py
# if __name__ == "__main__":
# 
#     #test
#     data = do_calc( mag_src = 15
#                     exp_time = 3600 
#                     coadds = 1
#                     dither = "AB"
#                     dith_repeats = 1
#                     num_reads = 16
#                     obs_wave = 'J'
#                     seeing = 0.8
#                     )
#     print ('result = ', data)
# 
