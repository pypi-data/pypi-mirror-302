import numpy as np
from yaml.loader import SafeLoader
import yaml
import pydantic
from pydantic import TypeAdapter, ValidationError
from pydantic.dataclasses import dataclass
import h5py
import spiakid_DRS.pages.Sim_func.WvConv as WC
import spiakid_DRS.SpectralRes.Data as Dt
import spiakid_DRS.pages.Sim_func.Fits_write as FW

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


def FITSdataCheck(file: str)->dict: 
    config = read_yaml(file)

    @dataclass
    class FITSFile:
        SimFolder: str
        FITSfolder: str
        WVbands: list
        TimeBinsDuration: int
    ta = TypeAdapter(FITSFile)
    try: 
        ta.validate_python(config)
        return(config)
    except pydantic.ValidationError as e:
        print(e)
 

def WriteFits(file):
    yml = FITSdataCheck(file)
    sim = Dt.read_hdf5(yml['SimFolder'])
    px_nbr = sim['Config']['Photon_Generation']['telescope']['detector']['pix_nbr']
    mt_wvph, mt_phwv = WC.conv(sim['Calib'], px_nbr)
    FW.WriteTerm(sim, yml['TimeBinsDuration'], yml['WVbands'], mt_phwv, yml['FITSfolder'])
    print('Done')



    return()