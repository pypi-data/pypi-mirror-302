import streamlit as st
import os
import SpectralRes.Data as Dt
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO



def Recons(folder_path, file, data_list, mt_wvph, mt_phwv):
    # Fonction pour charger les données (par exemple des images ou matrices)
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
        for i in range(len(file['Photons'])):
            newfile['Photons'][str(i)] = {}
            for key in file['Photons'][str(i)].keys():
                
                
                
                for j in range(len(file['Photons'][str(i)][key])):
           
                    if len(file['Photons'][str(i)][key][j]) !=0 :
                            newfile['Photons'][str(i)][key] = []
                            newfile['Photons'][str(i)][key].append(file['Photons'][str(i)][key])
        
        # print(newfile['Photons']['0'])
                    

                        
                        
        data_list = []
        for t in np.linspace(0, obs_time-1, obs_time, dtype=int):
            im = np.zeros(shape = (pix_nb,pix_nb))

            for i in range(pix_nb):
                for j in range(pix_nb):
                    if str(i)+'_'+str(j) in newfile['Photons'][str(t)]:
                        im[i,j] = len(newfile['Photons'][str(t)][str(i)+'_'+str(j)][0])
            data_list.append(im)

        return data_list, newfile

    # Changement de la taille des time bins
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
                
                nfile['Photons'][str(i)] = []
        

        # Grouping all photon according to tiem bin size
        for g in range(len(nfile['Photons'])):

            dict_ph = {}
            dict_s = {}
            dict_pix = {}
            for i in range(length[g]):
                
                for key in file['Photons'][str(g*time + i)].keys():
                    dict_pix[key] = []
                    if key in dict_ph:
                        dict_ph[key] = np.concatenate((dict_ph[key], file['Photons'][str(g*time+i)][key][0][1]), axis = None)
                        dict_s[key] = np.concatenate((dict_s[key], file['Photons'][str(g*time+i)][key][0][0]), axis = None)
                    else:
                        dict_ph[key] = file['Photons'][str(g*time + i)][key][0][1]
                        dict_s[key] = file['Photons'][str(g*time +i)][key][0][0]
                    
                    for ph in range(len(dict_ph[key])):
                        dict_pix[key].append([dict_s[key][ph], dict_ph[key][ph]])
            nfile['Photons'][str(g)] = dict_pix
        

        return(nfile)
    
    # Titre de l'interface
    

    # Demande du chemin du dossier
    

    # folder_path = None
    # Vérification que le chemin est valide
    if folder_path != None:
        data_list, file = load_data_from_folder(folder_path)
     
        pix_nb = file['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']
        # Charger les données du dossier
        if len(data_list) >1:
                time_bins = st.number_input(label = 'Time Bins', min_value=1, max_value=len(data_list) - 1, step = 1, value = 1,key = 'time_bins_reonstruction')
                nfile = new_file(file = file, time = time_bins)
                data_list = []
                # print(nfile['Photons']['1'])
                for t in np.linspace(0, len(nfile['Photons'])-1, len(nfile['Photons']), dtype=int):
                    
                    im = np.zeros(shape = (pix_nb,pix_nb))

                    for i in range(pix_nb):
                        for j in range(pix_nb):
                            if str(i)+'_'+str(j) in nfile['Photons'][str(t)]:
                                im[i,j] = len(nfile['Photons'][str(t)][str(i)+'_'+str(j)])
                               
                
                    data_list.append(im)
                
                idx = st.slider(label ="Time (s)", min_value = 0, max_value = len(data_list) - 1, value = 0, step = 1)
        else: 
            idx = 0
            nfile = file

        col1, col2 = st.columns([1,1])
        
        with col1:
            
            x = st.number_input(label = 'x', min_value=0, max_value=len(data_list[idx]) - 1, step = 1, value = 0,key = 'x_reconstruction')
            y = st.number_input(label = 'y', min_value=0, max_value=len(data_list[idx]) - 1, step = 1, value = 0,key = 'y_reconstruction')


        with col2:
            bins = st.number_input(label = 'Bins', min_value=1, max_value=180, step = 1, value = 50, key = 'phase_bins_recons')
            option = st.selectbox('Data type',('Wavelength (µm)', 'Phase (°)'), key = 'recons_choice')
           

        
            # ph = file['Photons'][idx][str(x)+'_'+str(y)]
            # fig3 = plt.hist(ph)
        plt.rc('font', size = 10)
        fig, (ax,ax3) = plt.subplots(1, 2, layout = 'constrained', figsize = (14,6.5))
        ax.set_ylim([0, len(data_list[idx])-1])
        ax.set_xlim([0, len(data_list[idx])-1])
        
        cax = ax.imshow(data_list[idx].T, cmap='viridis', origin = 'lower')
        fig.colorbar(cax)
        ax.set_aspect('equal', 'box')
        # ax2 = ax.twiny().twinx()
        # ax2.set_ylim([0, len(data_list[idx])-1])
        # ax2.set_xlim([0, len(data_list[idx])-1])
        # ax2.set_aspect('equal', 'datalim')

        ax.plot([x-0.5,x-0.5],[y-0.5,y+1-0.5], c='r')
        ax.plot([x+1-0.5,x+1-0.5],[y+1-0.5,y-0.5], c='r')
        ax.plot([x-0.5,x+1-0.5],[y+1-0.5,y+1-0.5], c='r')
        ax.plot([x+1-0.5,x-0.5],[y-0.5,y-0.5], c='r')
        

    

        list_phase = []
        if str(y)+'_'+str(x) in file['Photons'][str(idx)]:
                for i in range(len(nfile['Photons'][str(idx)][str(y)+'_'+str(x)])):
                    if option == 'Phase (°)':
                        list_phase.append(nfile['Photons'][str(idx)][str(y)+'_'+str(x)][i][1])
                    elif option =='Wavelength (µm)':
                        list_phase.append(mt_phwv[y,x](nfile['Photons'][str(idx)][str(y)+'_'+str(x)][i][1]))
        
        if option == 'Phase (°)':
            ax3.hist(list_phase, bins=bins, range = [0,180])
            ax3.set_xlabel('Phase (°)')
        elif option == 'Wavelength (µm)':
            ax3.hist(list_phase, bins=bins, range = mt_phwv[y,x]([180,0]))
            ax3.set_xlabel('Wavelength (µm)')

        # else:
        #         a = []
        #         ax3.hist(a)

        
        ax3.set_ylabel('Count')
        # ax3.set_xlim([30,120])
        col1, col2, col3 = st.columns([0.1,1,0.1])
        buf = BytesIO()
        fig.savefig(buf, format = 'png')
        with col2:
            st.image(buf)
    
            

