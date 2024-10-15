import numpy as np
import streamlit as st
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from io import BytesIO
import os

def fread(folder_path, option):
    
    if folder_path != None :
        if folder_path[-1] != '/': folder_path += '/'
        
        l = os.listdir(folder_path)
        
        files = []
        for i in range(len(l)):
            if 'fits' in l[i]:
                files.append(l[i])
                # files.append(l[i][:-5].split(sep='_'))
        files.sort(key = lambda f: int(''.join(filter(str.isdigit,f))))
        time = st.slider(label = 'Time', min_value=0, max_value=len(files)-1, value=0)
        if option == 'General':
            path = folder_path + files[time]
        else:
            path = folder_path + option + '/' + files[time]
        hdu_list = fits.open(path)
        image_data = hdu_list[0]
       
        
        image_data.scale('int16')
        # wcs = WCS(image_data.header)
        header = fits.getheader(path)
        # lim1, lim2 = header['LIM1'], header['LIM2']
        h = list(header)
        name = []
        t = []
        for i in range(len(header)):
                name.append(h[i])
                t.append(header[h[i]])
        # st.write(folder_path + files[time])
        if image_data.data.ndim == 3:
            
            col1, col2 = st.columns([1,1])
            with col1:
                x = st.number_input(label = 'x', min_value=0, max_value=len(image_data.data[:,:,0]) - 1, step = 1, value = 0,key = 'x_fread')
                y = st.number_input(label = 'y', min_value=0, max_value=len(image_data.data[:,:,0]) - 1, step = 1, value = 0,key = 'y_fread')

            with col2:
                hd= st.checkbox('Show Headers')
                if hd:
                    
                    st.data_editor(pd.DataFrame({
                        'NAME': name,
                        'HEADER': t
                    }) ,width = 1000, height=250)

        
            bands = header['BAND']
            bands = list(map(float, bands[1:-1].split(sep=',')))
            # st.write(len(bands))
            pbands = []
            for p in range(len(bands) -1):
                pbands.append((bands[p]+bands[p+1])/2)
            # st.write(pbands)
            col1, col2, col3 = st.columns([0.1,1,0.1])
            with col2:
                plt.rc('font', size = 20)
                fig, (ax1, ax2) = plt.subplots(1,2,layout = 'constrained', figsize = (14,6.5))
            #     ax1.set_ylim([0, len(image_data.data[:,:,0])-1])
            #     ax1.set_xlim([0, len(image_data.data[:,:,0])-1])
            #     if 'red' in folder_path:
            #         cax = ax1.imshow(image_data.data[:,:,0].T, cmap='Reds', origin = 'lower')
            #     elif 'green' in folder_path: 
            #         cax = ax1.imshow(image_data.data[:,:,0].T, cmap='Greens', origin = 'lower')
            #     elif 'blue' in folder_path: 
            #         cax = ax1.imshow(image_data.data[:,:,0].T, cmap='Blues', origin = 'lower')
                ndata = np.zeros(shape = (len(image_data.data), len(image_data.data)), dtype = int)
                for i in range(len(image_data.data)):
                    for j in range(len(image_data.data)):
                        ndata[i,j] = sum(image_data.data[i,j,:])
                cax = ax1.imshow(ndata.T, cmap='viridis', origin = 'lower')
                ax1.set_aspect('equal', 'box')

                ax1.plot([x-0.5,x-0.5],[y-0.5,y+1-0.5], c='r')
                ax1.plot([x+1-0.5,x+1-0.5],[y+1-0.5,y-0.5], c='r')
                ax1.plot([x-0.5,x+1-0.5],[y+1-0.5,y+1-0.5], c='r')
                ax1.plot([x+1-0.5,x-0.5],[y-0.5,y-0.5], c='r')
                fig.colorbar(cax)

                ax2.plot(pbands, image_data.data[x, y,:])
                ax2.set_xlabel('Wavelength (µm)')
                ax2.set_ylabel('Count')

                # if image_data.data[x,y,0] != 0:
                #     if 'red' in folder_path: 
                #         phase = np.linspace(start = lim2, stop = 1.3, num=len(image_data.data[x,y,1:]))
                #         ax2.set_xlabel('Wavelength (µm)')
                #     elif 'green' in folder_path: 
                #         phase = np.linspace(start = lim1, stop = lim2, num=len(image_data.data[x,y,1:]))
                #         ax2.set_xlabel('Wavelength (µm)')
                #     elif 'blue' in folder_path: 
                #         phase = np.linspace(start = 0.2, stop = lim1, num=len(image_data.data[x,y,1:]))
                #         ax2.set_xlabel('Wavelength (µm)')
                #     else:
                #         phase = np.linspace(start = 0, stop = 180, num=len(image_data.data[x,y,1:]))
                #         ax2.set_xlabel('Phase (°)')
                #     ax2.plot(phase, image_data.data[x,y,1:])
                    

                # else:
                #     l_zero = np.zeros(shape=len(image_data.data[0,0,1:]))
                #     ax2.plot(l_zero)
                #     ax2.set_xlabel('Phase (°)')

                
                # ax2.set_ylabel('Count')
                buf = BytesIO()
                fig.savefig(buf, format = 'png')
                st.image(buf)

        if image_data.data.ndim == 2:
            col1,col2,col3 = st.columns([1,1,1])
            with col1:
                fig, ax1 = plt.subplots(1,layout = 'constrained', figsize = (6.5,6.5))
                # ax1.imshow(image_data.data.T, origin = 'lower')
                cax = ax1.imshow(image_data.data.T, origin = 'lower')
                fig.colorbar(cax)
                buf = BytesIO()
                fig.savefig(buf, format = 'png')
                st.image(buf)
            with col3:

                    
                    st.data_editor(pd.DataFrame({
                        'NAME': name,
                        'HEADER': t
                    }) ,width = 1000, height=500
                    )

        # elif option == 'Multiple FITS':
        #     if '.fits' not in folder_path:
        #         if folder_path[-1] != '/' : folder_path = folder_path+'/'
                

        #         folder = folder_path + 'fits_red0.fits'
        #         hdu_listr = fits.open(folder)
        #         image_datar = hdu_listr[0]
        #         image_datar.scale('int16')

             
        #         x = st.number_input(label = 'x', min_value=0, max_value=len(image_datar.data[:,:,0]) - 1, step = 1, value = 0,key = 'x_fread')
        #         y = st.number_input(label = 'y', min_value=0, max_value=len(image_datar.data[:,:,0]) - 1, step = 1, value = 0,key = 'y_fread')

        #         header = fits.getheader(folder)
        #         # lim1, lim2 = header['LIM1'], header['LIM2']
        #         hdu_listr.close()
                
        #         folder = folder_path + 'fits_green0.fits'
        #         hdu_listg = fits.open(folder)
        #         image_datag = hdu_listg[0]
        #         image_datag.scale('int16')
        #         hdu_listg.close()
                
        #         folder = folder_path + 'fits_blue0.fits'
        #         hdu_listb = fits.open(folder)
        #         image_datab = hdu_listb[0]
        #         image_datab.scale('int16')
        #         hdu_listb.close()
        #         col1, col2, col3 = st.columns([0.1,1,0.1])
        #         if (image_datab.data == image_datar.data).all(): st.write('FUCK')
        #         with col2:
        #             plt.rc('font', size = 20)
        #             fig, axs = plt.subplots(2,3, layout = 'constrained', figsize = (14,6.5))
        #             # fig, (axb, axg, axr) = plt.subplots(1,3,layout = 'constrained', figsize = (14,6.5))
        #             axs[0,0].set_ylim([0, len(image_datab.data[:,:,0])-1])
        #             axs[0,0].set_xlim([0, len(image_datab.data[:,:,0])-1])
        #             caxb = axs[0,0].imshow(image_datab.data[:,:,0].T, cmap='Blues', origin = 'lower')
        #             axs[0,0].set_aspect('equal', 'box')
        #             axs[0,0].plot([x-0.5,x-0.5],[y-0.5,y+1-0.5], c='r')
        #             axs[0,0].plot([x+1-0.5,x+1-0.5],[y+1-0.5,y-0.5], c='r')
        #             axs[0,0].plot([x-0.5,x+1-0.5],[y+1-0.5,y+1-0.5], c='r')
        #             axs[0,0].plot([x+1-0.5,x-0.5],[y-0.5,y-0.5], c='r')
        #             fig.colorbar(caxb)

        #             axs[0,1].set_ylim([0, len(image_datag.data[:,:,0])-1])
        #             axs[0,1].set_xlim([0, len(image_datag.data[:,:,0])-1])
        #             caxg = axs[0,1].imshow(image_datag.data[:,:,0].T, cmap='Greens', origin = 'lower')
        #             axs[0,1].set_aspect('equal', 'box')

        #             axs[0,1].plot([x-0.5,x-0.5],[y-0.5,y+1-0.5], c='r')
        #             axs[0,1].plot([x+1-0.5,x+1-0.5],[y+1-0.5,y-0.5], c='r')
        #             axs[0,1].plot([x-0.5,x+1-0.5],[y+1-0.5,y+1-0.5], c='r')
        #             axs[0,1].plot([x+1-0.5,x-0.5],[y-0.5,y-0.5], c='r')
        #             fig.colorbar(caxg)

        #             axs[0,2].set_ylim([0, len(image_datar.data[:,:,0])-1])
        #             axs[0,2].set_xlim([0, len(image_datar.data[:,:,0])-1])
        #             caxr = axs[0,2].imshow(image_datar.data[:,:,0].T, cmap='Reds', origin = 'lower')
        #             axs[0,2].set_aspect('equal', 'box')

        #             axs[0,2].plot([x-0.5,x-0.5],[y-0.5,y+1-0.5], c='r')
        #             axs[0,2].plot([x+1-0.5,x+1-0.5],[y+1-0.5,y-0.5], c='r')
        #             axs[0,2].plot([x-0.5,x+1-0.5],[y+1-0.5,y+1-0.5], c='r')
        #             axs[0,2].plot([x+1-0.5,x-0.5],[y-0.5,y-0.5], c='r')
        #             fig.colorbar(caxr)

        #             if image_datar.data[x,y,0] != 0:
                    
        #                 phaser = np.linspace(start = lim2, stop = 1.3, num=len(image_datar.data[x,y,1:]))
        #                 axs[1,2].set_xlabel('Wavelength (µm)')
        #                 axs[1,2].plot(phaser, image_datar.data[x,y,1:])
        #             else:
        #                 l_zero = np.zeros(shape=len(image_datar.data[0,0,1:]))
        #                 axs[1,2].plot(l_zero)
        #                 axs[1,2].set_xlabel('Wavelength (µm)')
        #             # elif 'green' in folder_path: 
        #             if image_datag.data[x,y,0] != 0:
        #                 phaseg = np.linspace(start = lim1, stop = lim2, num=len(image_datag.data[x,y,1:]))
        #                 axs[1,1].set_xlabel('Wavelength (µm)')
        #                 axs[1,1].plot(phaseg, image_datag.data[x,y,1:])
        #             else:
        #                 l_zero = np.zeros(shape=len(image_datag.data[0,0,1:]))
        #                 axs[1,1].plot(l_zero)
        #                 axs[1,1].set_xlabel('Wavelength (µm)')
        #             # elif 'blue' in folder_path: 
        #             if image_datab.data[x,y,0] != 0:
        #                 phaseb = np.linspace(start = 0.2, stop = lim1, num=len(image_datab.data[x,y,1:]))
        #                 axs[1,0].set_xlabel('Wavelength (µm)')
        #                 axs[1,0].plot(phaseb, image_datab.data[x,y,1:])
        #             else:
        #                 l_zero = np.zeros(shape=len(image_datab.data[0,0,1:]))
        #                 axs[1,0].plot(l_zero)
        #                 axs[1,0].set_xlabel('Wavelength (µm)')
        #             axs[1,2].set_ylabel('Count')
        #             axs[1,1].set_ylabel('Count')
        #             axs[1,0].set_ylabel('Count')
        #             buf = BytesIO()
        #             fig.savefig(buf, format = 'png')
        #             st.image(buf)
                        


                    

                    
        #     else: 
        #         st.write('Select General FITS')

            