import streamlit as st
# import spiakid_DRS.SpectralRes.Data as Dt
import pandas as pd
# import SpectralRes.Data as Dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from astropy.io import fits
import os
import sys
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_constellation,ICRS,FK5
from astropy.time import Time
from astropy.timeseries import TimeSeries
import astropy.units as u

def new_file(file,time):
        t = len(file['Photons'])
        nfile ={}
        nfile['Photons'] = {}
        nbgroup = int(t/time)
        length = np.ones(shape=nbgroup, dtype=list) * time
        # We create lists in new file
        if t/time - nbgroup > 0:
            r = t - nbgroup*time
            length = np.concatenate((length,r), axis = None)
            
            for i in range(nbgroup+1):
                nfile['Photons'][str(i)] = [] 
        else:
            for i in range(nbgroup):
                r = t - nbgroup*time
                length = np.concatenate((length,r), axis = None)
                length = length[:-1]
                # st.write(length)
                nfile['Photons'][str(i)] = []
        

        # Grouping all photon according to tiem bin size
        for g in range(len(nfile['Photons'])):

            dict_ph = {}
            dict_s = {}
            dict_pix = {}
            for i in range(length[g]):
                
                for key in file['Photons'][str(g*time + i)].keys():
                    dict_pix[key] = []

                    if len(file['Photons'][str(g*time + i)][key][0])>0:
                        # st.write(type(file['Photons'][str(g*time + i)][key][0]))
                        if key in dict_ph:
                            
                            if len(np.shape(file['Photons'][str(g*time + i)][key][0])) == 1:
                                dict_ph[key] = np.concatenate((dict_ph[key], file['Photons'][str(g*time+i)][key][1]), axis = None)
                                
                                dict_s[key] = np.concatenate((dict_s[key], file['Photons'][str(g*time+i)][key][0]), axis = None)
                            else:
                                dict_ph[key] = np.concatenate((dict_ph[key], file['Photons'][str(g*time+i)][key][0][1]), axis = None)
                                dict_s[key] = np.concatenate((dict_s[key], file['Photons'][str(g*time+i)][key][0][0]), axis = None)
                        else:
                            # print(len(np.shape(file['Photons'][str(g*time + i)][key][0])))
                            # st.write(file['Photons'][str(g*time + i)][key])
                            if len(np.shape(file['Photons'][str(g*time + i)][key][0])) == 1:
                            
                                dict_ph[key] = file['Photons'][str(g*time + i)][key][1]
                                dict_s[key] = file['Photons'][str(g*time +i)][key][0]
                            else:
                                dict_ph[key] = file['Photons'][str(g*time + i)][key][0][1]
                                dict_s[key] = file['Photons'][str(g*time +i)][key][0][0]
                        # print(file['Photons'][str(g*time+i)][key][1])
                        for ph in range(len(dict_ph[key])):
                            dict_pix[key].append([dict_s[key][ph], dict_ph[key][ph]])
            nfile['Photons'][str(g)] = dict_pix
    

        return(nfile, length)
    

def ImCreation(nfile, pix_nb,bands, mt_phwv):
    imlist=[]

    for t in np.linspace(0, len(nfile['Photons'])-1, len(nfile['Photons']), dtype=int):
            
            im = np.zeros(shape = (pix_nb,pix_nb, len(bands)), dtype=int)
         
            for i in range(pix_nb):
                for j in range(pix_nb):
            
                    
                    if str(i)+'_'+str(j) in nfile['Photons'][str(t)]:
              
                        if len(nfile['Photons'][str(t)][str(i)+'_'+str(j)])>0:
                            
                            for ph in range(len(nfile['Photons'][str(t)][str(i)+'_'+str(j)])):
                                val = float(str(mt_phwv[i,j](nfile['Photons'][str(t)][str(i)+'_'+str(j)][ph][1])))
                                bandinter =np.copy(bands)
             
                                bandinter = np.append(bandinter, val)
                                bandinter.sort()
                               
                  
                                inx = abs(val - bandinter).argmin()
                                try:
                                    im[i,j,inx] +=1
                                except:
                                    print(val, bandinter, len(bands)) 
                                    sys.exit()

            
            imlist.append(im.astype(np.int16)) 

    
    
    return(imlist)

# def header_creation(config, nb):
#     header = None
    

#     return(header.to_header())


def Write_FITS(data, path, config, bands, length):
        pbands = []
        # obs_time = config['Photon_Generation']['telescope']['exposition_time']
        

        nbPix = config['Photon_Generation']['telescope']['detector']['pix_nbr']
        pixelSize = config['Photon_Generation']['telescope']['detector']['pix_size']
        obs_time = config['Photon_Generation']['telescope']['exposition_time']
        AltGuide, AzGuide = config['Photon_Generation']['sky']['guide']['alt']*np.pi/180, config['Photon_Generation']['sky']['guide']['az']*np.pi/180
        date_obs='2024-05-20T12:06:05'
        observatory = EarthLocation.of_site('lasilla')
        # lat = observatory.lat.rad
        obs_start_time = Time(date_obs,scale='utc',format='isot',location=observatory)
        fovCenterXY = [int(nbPix/2), int(nbPix/2)]
        observatory = EarthLocation.of_site('lasilla')
        delta_time = np.linspace(0, obs_time, len(data))*u.second
        obs_times=obs_start_time+delta_time
        frame_night = AltAz(obstime=obs_times,location=observatory)
        time = Time(date_obs)
        altaz = AltAz(obstime = time, location = observatory)
        coord = SkyCoord(alt = AltGuide*u.rad, az = AzGuide*u.rad, frame = altaz)
        radec = coord.transform_to('icrs')
        RA = radec.ra.rad
        DEC = radec.dec.rad

        fovCenterICRS=SkyCoord(RA* u.rad , DEC * u.rad, frame=ICRS)
        fk5=FK5(equinox=obs_start_time)
        fovCenterAltAz=fovCenterICRS.transform_to(frame_night)
        fovCenterFK5=fovCenterICRS.transform_to(fk5)

        # time_inter= Time(length, format = 'cxcsec', scale = 'utc')
        ts = [0,]
        for j in range(1, len(length)):
            ts.append(ts[-1]+length[j])
        # time_start = Time(date_obs)
        time_stp = time + ts *u.s
        # st.write(time_stp)

        

        t = np.linspace(0,len(data)-1,len(data))
        a=fovCenterAltAz.az.radian-np.pi
        z=np.pi/2-fovCenterAltAz.alt.radian
        H=obs_times.sidereal_time('mean').radian - fovCenterFK5.ra.radian

        # H_time_series = TimeSeries(time_start='2020-01-01 20:00:00',time_delta = 1*u.s,n_samples =len(t))
        H_time_series = TimeSeries(time = time_stp)
        cosS=np.cos(a)*np.cos(H)+np.sin(a)*np.sin(H)*np.sin(observatory.lat.radian)
        if z[0] > np.pi*0.01:
            sinS=np.cos(observatory.lat.radian)*np.sin(H)/np.sin(z)
        else:
            sinS=np.cos(observatory.lat.radian)*np.sin(a)/np.cos(fovCenterFK5.dec.radian)

        S=np.arctan2(sinS,cosS)
        cdelt1=pixelSize/3600
        cdelt2=pixelSize/3600
        
        


        # header = header_creation(config, len(data))
        for p in range(len(bands) -1):
                pbands.append(round((bands[p]+bands[p+1])/2,3))
        for t in range(len(data)):
            fitsname = 'fits_'+str(int(t*obs_time/len(data)))
          
            datat = data[t]

            header = WCS(naxis = 2)

            rota=S[t]
            cd11=-cdelt1*np.cos(rota)
            cd12=cdelt2*np.sin(rota)
            cd21=cdelt1*np.sin(rota)
            cd22=cdelt2*np.cos(rota)
            
            header.wcs.ctype = ['RA---TAN', 'DEC--TAN']
            # header.wcs.cdelt = [cdelt1, cdelt2]
            header.wcs.crval = [fovCenterICRS.ra.degree, fovCenterICRS.dec.degree]
            header.wcs.crpix = fovCenterXY
            header.wcs.cunit = ['deg','deg']
            header.wcs.cd=[[cd11,cd12],[cd21,cd22]]
            header.wcs.mjdobs=obs_start_time.mjd
            
            h = header.to_header()
            h['DATE-OBS'] = H_time_series[t][0].value
            h['EXPTIME'] = length[t]
            h['PHOTZP'] = 25
            h['CDELT1'] = 0.5
            h['CDELT2'] = 0.5
            # h['EXPTIME'] = obs_time / (tbins-1)
            im = datat[:,:,0]
            for wv in range(1,len(bands)-1):
                 im += datat[:,:,wv]
            # header = fits.Header()
            # for j in range(len(headerdata.loc[:])):
            #     try: np.float16(headerdata.loc[j]['Header'])
            #     except: header[headerdata.loc[j]['NAME']] = headerdata.loc[j]['Header']
            #     else: header[headerdata.loc[j]['NAME']] = np.float16(headerdata.loc[j]['Header'])
                


            primary_hdu = fits.PrimaryHDU(im,header=h)
            hdul = fits.HDUList([primary_hdu])

            hdul.writeto(path+fitsname+'.fits', overwrite=True)
 
            for wv in range(1,len(bands)-1):
                h['WAVELEN'] = '%.3f' % pbands[wv]
                h['WAVEMIN'] = bands[wv]
                h['WAVEMAX'] = bands[wv+1]
                
                primary_hdu = fits.PrimaryHDU(datat[:,:,wv].astype(np.int16), header = h)
                hdul = fits.HDUList([primary_hdu])
                try: os.mkdir(path+'%.3f' % pbands[wv]+'µm')
                except: pass
                hdul.writeto(path+'%.3f' % pbands[wv]+'µm/'+fitsname+'.fits', overwrite=True)

        



def Write(folder_path, file, data_list, mt_wvph, mt_phwv):

    # If Folder path already exist
    if folder_path != None :

        # option = st.selectbox('Data type to write',('Wavelength (µm)', 'Phase (°)'), key = 'choice')
        st.write('Simulation Path')
        st.write(folder_path)
        obs_time = file['Config']['Photon_Generation']['telescope']['exposition_time']
        pix_nb = file['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']
        pxsize = file['Config']['Photon_Generation']['telescope']['detector']['pix_size']
        

        # lim1, lim2 = st.select_slider(
        #      'Filter Band',
        #      options=np.linspace(0.3, 1.2,91),
        #      value = (0.3,1.2)
        # )
      
        col1, col2 = st.columns([1,1])
        
        

        with col1:
            # Writing FITS code
            save_path = st.text_input(label='Saving Path', key = 'Save_path')
            
            time_bins = st.number_input(label = 'Time Bins', min_value=1, max_value=len(data_list) - 1, step = 1, value = 1, key = 'time_bins_fits')
            bins = st.number_input(label = 'Wv band', min_value=3, max_value=10, step = 1, value = 5, key = 'Wv band')
            lim1 = float(st.text_input(label = 'Wv Min (µm)', key ='lim1', value='0.2'))
            lim2 = float(st.text_input(label = 'Wv Max (µm)', key ='lim2', value='1.2'))
            bands = []
            for i in range(bins + 1):
                bands.append(lim1 + i*(lim2-lim1)/(bins))
            # bands = np.array(bands)
    
            if st.checkbox(label='Show Wavelength'):
                st.write(bands)

            
            arcsec2deg = 1/3600
            # File decomposition with indicated time bins
            nfile, length  = new_file(file=file, time=time_bins)
            
            # d = str(date.today()).split(sep = '-')
            # today = d[2] +'/'+ d[1] +'/'+ d[0][2:]
            # Setting headers in Data_Frame
            

            # with col2:
            #         st.write('Enter FITS Headers (Automated already displayed, wv bands are in)')
            #         edited_data = st.data_editor(headers_data, num_rows = 'dynamic', width = 1000, height=500, hide_index=True)
                  



            # Writing button
            col11, col12 = st.columns([5.75,1])
            with col11:
                if st.button(label = 'Write Fits'):

                    if save_path[-1] != '/': save_path= save_path + '/'
                    data = ImCreation(nfile, pix_nb, bands, mt_phwv)
        
                    
                    Write_FITS(data, save_path,file['Config'], bands, length)
            #         Write_FITS_color(data_r, data_g, data_b, save_path, edited_data)
                    st.write('DONE')


def WriteTerm(file, tbins, bands, mt_phwv, FITSPath):
     
    obs_time = file['Config']['Photon_Generation']['telescope']['exposition_time']
    pix_nb = file['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']
    pxsize = file['Config']['Photon_Generation']['telescope']['detector']['pix_size']

    nfile, length  = new_file(file=file, time=tbins)
    if FITSPath[-1] != '/': FITSPath= FITSPath + '/'
    data = ImCreation(nfile, pix_nb, bands, mt_phwv)
    Write_FITS(data, FITSPath,file['Config'], bands, length)
