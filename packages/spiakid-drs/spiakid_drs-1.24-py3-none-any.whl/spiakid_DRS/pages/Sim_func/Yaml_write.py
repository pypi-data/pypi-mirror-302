import numpy as np
import streamlit as st
import pathlib


def Yaml_wr():
    
    data = dict()
    data['process_nb'] = st.number_input(label='Process number',format = '%i',value = 1)
    data['5-Output'] = dict()
    path = pathlib.Path().resolve()
        
    data['sim_file'] = st.text_input(label='Data location', value = str(path)+'/Sim.hdf5')
    Ph_gen = True

    if Ph_gen:
        
        col1, col2, col3, col4 = st.columns(4)
        data['1-Photon_Generation'] = dict()
        data['1-Photon_Generation']['telescope'] = dict()
        tel = data['1-Photon_Generation']['telescope']
        
        with col1:
            st.write('Telescope caracteristics')
            tel['exposition_time'] = st.number_input(label='Exposition Time (s)',format = '%i',value = 1)
            tel['diameter'] = st.number_input(label='Diameter (m)',format = '%f',value = 3.5)
            tel['obscuration'] = st.number_input(label = 'Obscuration',format = '%f',value = 1.)
            tel['latitude'] = st.number_input(label = 'Telescope latitude', min_value=-90.,max_value=90., format='%f', value = -29.25892)
            tel['transmittance'] = st.text_input(label = 'Transmittance', placeholder="Absolute path")
            st.write('Detector')
            tel['detector'] = dict()
            col1_1,col1_2 = st.columns(2)
            with col1_1:
                tel['detector']['pix_nbr'] = st.number_input(label='Pix number', format='%i', value = 5)
            with col1_2:
                tel['detector']['pix_size'] = st.number_input(label='Pix size', format='%f', value = 0.5)
            
        data['1-Photon_Generation']['star'] = dict()
        star = data['1-Photon_Generation']['star']

        with col2:
            st.write('Star caracteristics')
            star['number'] = st.number_input(label = 'Star number', format = '%i', value = 5)
            star['distance'] = dict()
            st.write('Distance (pc)')
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                star['distance']['min'] = st.number_input(label = 'min', format='%f', value = 5.)
            with col2_2:
                star['distance']['max'] = st.number_input(label = 'max', format='%f', value = 10.)
            st.write('Wavelength range (µm)')
            star['wavelength_array'] = dict()
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                star['wavelength_array']['min'] = st.number_input(label = 'min', format = '%f', value = 0.4)
            with col2_2:
                star['wavelength_array']['max'] = st.number_input(label = 'max', format = '%f', value = 0.8)
            with col2_3:
                star['wavelength_array']['nbr'] = st.number_input(label = 'number of value', format = '%i', value = 40)
            star['spectrum_folder'] = st.text_input(label = 'Spectrum Folder', placeholder="Absolute path")

        data['1-Photon_Generation']['sky'] = dict()
        sky = data['1-Photon_Generation']['sky']

        with col3:
            st.write('Sky caracteristics')
            sky['method'] = 'Simulation'
            sky['contamination'] = False
            sky['rotation'] = True
            sky['fov_method'] = 'fix'
            sky['guide'] = dict()
            st.write('Guiding star coordinates (degree)')
            col3_1, col3_2 = st.columns(2)
            with col3_1:
                sky['guide']['alt'] = st.number_input(label = 'altitude', format = '%f', min_value = 0., max_value = 90., value = 45.)
            with col3_2:
                sky['guide']['az'] = st.number_input(label = 'azimut', format = '%f', min_value = 0., max_value = 360., value = 45.)
            
        data['1-Photon_Generation']['PSF'] = dict()
        psf = data['1-Photon_Generation']['PSF']
        
        with col4:
            choice=st.radio(label = "PSF Creation Method", options = ("Creation","Download"))
            if choice == 'Creation':
                psf['method'] = 'turbulence'
                psf['pix_nbr'] = st.number_input(label = 'pix number', format = '%i', value = 1000)
                psf['size'] = st.number_input(label = 'pix size (arcsec)', format = '%f', value = 2.)
                psf['seeing'] = st.number_input(label = 'seeing', format = '%f', value = 0.5)
                psf['wind'] = st.number_input(label = 'wind', value = 10)
                psf['L0'] = st.number_input(label = 'L0', format = '%f', value = 30.)
                save = st.checkbox("Save the PSF ?")
                if save:
                    psf['file'] = st.text_input(label = 'PSF Saving Path', placeholder='Absolute path')
                

            elif choice == 'Download':
                psf['method'] = 'Download'
                psf['file'] = st.text_input(label = 'PSF location',placeholder='Absolute path')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write('Timeline')
        data['2-Timeline'] = dict()
        data['2-Timeline']['point_nb'] = st.number_input(label = 'Point number per sec',format = '%i', value = 1_000_000)
    
    with col2:
        phase = st.checkbox("Phase ?")
        if phase:
            data['3-Phase'] = dict()
            ph = data['3-Phase']
            ph['Calib_File'] = st.text_input(label = 'Wavelength/Phase Calibration', placeholder='Absolute path')
            ph['Phase_Noise'] = st.number_input(label = 'Phase Noise', format = '%f',value = 10.)
            ph['Decay'] = st.number_input(label = 'Dead Time Decay', format = '%f', min_value = 0., value = 33000.)
            ph['Readout_Noise'] = dict()

            ph['Readout_Noise']['scale'] = st.number_input(label = 'Readout Noise sigma', format='%f', value =0.5)
            ph['Readout_Noise']['type'] = 'Gaussian'
            
            ph['Phase'] = True

    with col3:
        elec = st.checkbox('Electronics ?')
        if elec and phase:
            data['4-Electronic'] = dict()
            electronic = data['4-Electronic'] 
            electronic['nperseg'] = st.number_input(label = 'Template Points Number', format = '%i', value = 4000)
            electronic['template_time'] = electronic['nperseg'] / data['2-Timeline']['point_nb']
            electronic['trigerinx'] = st.number_input(label = 'Pulse Point Position', format = '%i', max_value = electronic['nperseg'], value = 1000)
            electronic['point_nb'] = electronic['nperseg'] 
    
    with col4:
        
        saving = st.checkbox('Save Simulation ?')

        if saving:
            
            result = st.radio(label = "Result type", options = ("Simulated Data","Photon List"))
            if result == 'Simulated Data':
                data['5-Output']['save'] = 'Simulation'
            
            else:
                if elec and phase:
                    data['5-Output']['save'] = 'photon_list'
                else:
                    st.write('Require phase and electronics to simulate photons on detector')
    
    return(data)



