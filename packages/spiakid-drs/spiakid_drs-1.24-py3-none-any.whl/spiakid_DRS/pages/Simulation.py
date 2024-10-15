import streamlit as st
import numpy as np
import os

import pages.Sim_func.WvConv as WC
import pages.Sim_func.Test as RI
import pages.Sim_func.Sim_creation as SC
import pages.Sim_func.Fits_write as FW
import SpectralRes.Data as Dt
import pages.Sim_func.FITS_read as FR

@st.cache_data
def load_data_from_folder(folder_path):
        # Simuler le chargement des fichiers (ici un ensemble de matrices aléatoires pour l'exemple)
        file = Dt.read_hdf5(folder_path)
        obs_time = file['Config']['Photon_Generation']['telescope']['exposition_time']
        pix_nb = file['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']

        # for i in range(len(file['Photons'])):
        #     for key in file['Photons'][str(i)].keys():
        #         if file['Photons'][str(i)][key] == []:
        #             del file['Photons'][str(i)][key]
        newfile = {}
        newfile['Photons'] = {}
        newfile['Config'] = file['Config']
        newfile['Calib'] = file['Calib']
        for i in range(len(file['Photons'])):
            newfile['Photons'][str(i)] = {}
            for key in file['Photons'][str(i)].keys():
                for j in range(len(file['Photons'][str(i)][key])):
           
                    if len(file['Photons'][str(i)][key][j]) !=0 :
                            newfile['Photons'][str(i)][key] = []
                            newfile['Photons'][str(i)][key].append(file['Photons'][str(i)][key])

        data_list = []
        for t in np.linspace(0, obs_time-1, obs_time, dtype=int):
            im = np.zeros(shape = (pix_nb,pix_nb))

            for i in range(pix_nb):
                for j in range(pix_nb):
                    if str(i)+'_'+str(j) in newfile['Photons'][str(t)]:
                        im[i,j] = len(newfile['Photons'][str(t)][str(i)+'_'+str(j)][0])
            data_list.append(im)

        return data_list, newfile

@st.cache_data
def WvConv(file):
    CalibFile = file['Calib']
   
    pxnbr = file['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']
    mt_wvph, mt_phwv = WC.conv(CalibFile, pxnbr)
    
    return(mt_wvph, mt_phwv)


st.set_page_config(page_title='Simulation',layout = 'wide')

tab1, tab2,tab3, tab4 = st.tabs(['Simulation Interface','Reconstruction', 'FITS Writing', 'FITS Reading'])

folder_path = None
file = None
data_list = None
mt_phwv = None
mt_wvph = None

with tab1:
    SC.Sim()
with tab2:
    st.title("Simulation Visualization")
    if folder_path == None:
        folder_path = st.text_input(label = "Entrez le chemin du dossier contenant les données:", value = None, key = 'Init_first_tab')
    if folder_path != None:
        data_list, file = load_data_from_folder(folder_path)
        mt_wvph, mt_phwv = WvConv(file)
    
with tab3:
    st.title("Write FITS data")
 
    if folder_path == None:
        folder_path = st.text_input(label = "Entrez le chemin du dossier contenant les données", value = None, key = 'Init_second_tab')
    if folder_path != None:
        data_list, file = load_data_from_folder(folder_path)

        mt_wvph, mt_phwv = WvConv(file)

        
with tab2:
    RI.Recons(folder_path, file, data_list, mt_wvph, mt_phwv)
with tab3:
    FW.Write(folder_path=folder_path, file=file, data_list=data_list, mt_phwv=mt_phwv, mt_wvph=mt_wvph)

with tab4:
    st.title('Read FITS data')
    # option = st.selectbox('FITS Visualization',('General FITS', 'Wavelength FITS'))
    # if option == 'General FITS':
    #     folder_path = st.text_input(label = "Enter FITS file path", value = None, key = 'Init_third_tab')
    # elif option == 'Multiple FITS':
    
    f_path = st.text_input(label = "Enter FITS folder path", value = None, key = 'Init_third_tab')
    if f_path != None:
        l = os.listdir(f_path)
        files = []
        for i in range(len(l)):
                if 'fits' not in l[i] :
                    files.append(l[i])
                    # files.append(l[i][:-5].split(sep='_'))
        files.sort(key = lambda f: int(''.join(filter(str.isdigit,f))))
        files.insert(0, 'General')
        option = st.selectbox(label = 'Files',options = files)
        FR.fread(folder_path=f_path, option = option)


