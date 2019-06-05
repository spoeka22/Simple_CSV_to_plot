"""
Created on May 2019

@author: Anna

Simple script to import ISS/XPS data from .avg format as you get it when using DataSpace_BatchDump.exe


"""
import numpy as np
import pandas as pd
from collections import OrderedDict

#DATA IMPORT PARAMETERS
#example data structure below - script that returns both folder list and filnames dictionary for a given folder path
#is available (ask Anna to upload)

folder_path = r'C:\Users\annawi\Desktop\Projects\Propene oxidation\Experiments\201905_PdAufoams\XPS + ISS\ISS - before_after echem'
folders = [
    'ISS_as_prep',
               ]
filenames =OrderedDict([
    ('ISS_as_prep',[

        # 'Au foam large_as_prep.avg',
        # 'Au foam 004 after EC_as_prep.avg',
        # 'AuPd  foam 1090 002_as_prep.avg',
        # 'AuPd foam 1090 001 post EC_as_prep.avg',
        # 'AuPd foam 9010 002_as_prep.avg',
        # 'AuPd foam 9010 003 post EC_as_prep.avg',
        'Pd foam large_as_prep.avg'
    ]),
])

def import_avg(folder_path, filenames, folders, energy_step=1):
    """
    importing of ISS data in avg format as produced by DataSpace_BatchDump.exe
    :param folder_path, filenames, folders
    energy step: as avg file contains only a list of values the x data is generated using and energy step size of 1 (by default).
    when measuring at higher energy resolution this needs to be adjusted. (I think it's actually stated somewhere in the header,
    could be nice to modify this to automatically read it from the header)
    :return: data (list of dictionary for each file containing the actual data as numpy array
    """
    data = []
    column_header = ["Kinetic energy / eV", "Intensity / CPS"]
    for folder, files in filenames.items():
        for filename in files:
            if folder in folders:
                datapath = folder_path + "/" + folder + "/" + filename #this might actually only work on Windows, refactoring to use os recommended
                print("now working on " + filename)
                with open(datapath) as f:
                    timestamp = [] #doesnt work for now
                    file_data = {}
                    file_data_frame = pd.read_csv(f, sep=",", skiprows=85, names=["0", "2", "3", "4"]) #assumes that header is always 85 lines
                    file_data_frame[["5", "6", "1"]] =file_data_frame["0"].str.split("\\s+", expand = True, )
                    file_data_frame = file_data_frame.drop(["0", "5", "6"], axis=1)
                    file_data_frame = file_data_frame.reindex(sorted(file_data_frame.columns), axis=1)
                    for column in file_data_frame.columns:
                        file_data_frame[column] = pd.to_numeric(file_data_frame[column], errors='coerce')
                    intensity_list =[]
                    for line in file_data_frame.values:
                        # print(line)
                        intensity_list = intensity_list + line[:].tolist()
                    energy_list = np.arange(len(intensity_list), step=energy_step)
                    # print(intensity_list)
                    # print(energy_list)
                    file_data_raw = np.array([energy_list, intensity_list])
                    # print(file_data_raw)
                    file_data[column_header[0]], file_data[column_header[1]] = file_data_raw
                    data.append({"filename": filename, "timestamp": timestamp, "data": file_data})

    return data