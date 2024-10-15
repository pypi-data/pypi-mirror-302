import numpy as np
import streamlit as st
import pages.Sim_func.Yaml_write as wr
import yaml
from yaml.loader import SafeLoader
import pathlib
import os
import importlib.metadata 

def Sim():

    st.title('Simulation Creation')

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    select = st.radio('YAML with data to create the simulation',options = ['Import','Create'])
    


    if select == 'Import':
        yaml_path = st.text_input(label='Yaml file',placeholder="Absolute path", value =pathlib.Path().resolve())
        if st.button('Launch'):
            data = read_yaml(yaml_path)
            st.write(data)

    elif select == 'Create':
        st.write('Enter informations for the simulation, the package will be download after the launch')
        data = wr.Yaml_wr()
        data_file = st.text_input(label='Path and Name of data file',value =pathlib.Path().resolve())
        if data_file[-4:] == 'yaml' or data_file[:-4] == 'Yaml':
            pass
        else: data_file = data_file + '.yaml'
        if st.button('Download'):
            st.write('Saved')
            with open(data_file,'w') as yml:
                yaml.dump(data,yml,default_flow_style=False)
        if st.button('Launch'):
            
            # print(sys.modules)
            installed_packages_map = {dist.metadata['Name'] for dist in importlib.metadata.distributions()}
            if 'spiakid-simulation' not in installed_packages_map:
                st.write('Intsallation')
                os.system('pip install spiakid-simulation')
            st.write('Launched')
            with open(data_file,'w') as yml:
                yaml.dump(data,yml,default_flow_style=False)

            os.system('python -m spiakid_simulation.Simulation --sim '+ str(data_file))

            st.write('Done')
            
          
    


def read_yaml(FilePath):
        r""""
        Read yaml file and store all information in data

        Parameter
        ---------

        FilePath: string
            Position and name of the yaml file

        Attributes
        ----------

        Data: Dictionnary
            Contains all information that contains the yaml file correctly ordered
        """
        with open(FilePath) as f:
            data = yaml.load(f, Loader=SafeLoader)
        return data

