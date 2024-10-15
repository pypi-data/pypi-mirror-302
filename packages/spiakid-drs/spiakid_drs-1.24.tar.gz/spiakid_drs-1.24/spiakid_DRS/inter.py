from spiakid_DRS.SpectralRes import Detect as D
import spiakid_DRS.DRSterm as dr
import os
import sys
import argparse
from pathlib import Path
import pathlib

"""
Link between Terminal and pipeline
"""
def parse():
    # read in command line arguments
    parser = argparse.ArgumentParser(description='MKID Pipeline CLI')
    parser.add_argument('--init', action='store_true', help='launch the interface')
    parser.add_argument('--outp', help='output destination', dest='out_cfg', default=None)
    parser.add_argument('--inp', help='data location', dest='in_cfg' , default=None)
    parser.add_argument('--format', help='format of the plot', default='.jpg', dest='form')
    parser.add_argument('--dir', help='create input and output folder', action='store_true')
    parser.add_argument('--fits', help = 'Write FITS from a simulation', action='store_true')
    parser.add_argument('--yaml', help='Path to the Yaml with information', dest = 'yml', default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse()

    if args.init:
        # try:
        #     path = str(sorted(pathlib.Path('/').glob('**/Home.py'))[0]) #Docker version
        # except:
        #     here = os.path.dirname(sys.executable).split(sep = '/')[1:-1]
           
        #     link = '/'
        #     for i in here: link += i + '/'
            
        #     path = str(sorted(pathlib.Path(link).glob('**/Home.py'))[0])  #Terminal version
        path = '/home/sfaes/git/DRS/spiakid_DRS/Home.py'
        os.system("streamlit run "+path)
    if args.fits and args.yml:
      
        dr.WriteFits(args.yml)
    
  