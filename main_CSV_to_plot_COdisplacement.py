"""
Created on Thu Sep  27 15:08 2018

@author: Anna

Simple script to import CSV data as DataFrame according to absolute data path, possible data treatment, and plotting
using matplotlib.

Specifically written for importing FT-IR data exported as csv using software spectragryph.

"""

from pandas import DataFrame
import pandas as pd
import itertools
import json
from collections import OrderedDict
import matplotlib
matplotlib.use('qt4agg')
import matplotlib.pyplot as plt
import numpy as np
import re


#DATA IMPORT PARAMETERS
folder_path = r'\\dtu-storage\annawi\Desktop\Projects\Propene oxidation\IR_experiments\Spectra'
folders =[
            # '092418 - smoothPdfilm',
            # '092518',
            '092618 - rough Pd film'
          ]
filenames =OrderedDict([
            ('092418 - smoothPdfilm', ['092418_Pd_Phosbuff_450mV_prop_0001(6).csv',
                                                                              ]),

])


#IMPORTING FUNCTIONS

#info about datastructure of the FT-IR data:
#first line contains timestamp -> important to sync with EC data
#2nd line is column header, from then on data
#comma separated


def import_csv(folder_path, filenames, folders):
    """
    importing of data as csv - tailored to FTIR data for now
    :param folder_path, filenames, folders
    :return: data
    """
    data = []

    for folder, files in filenames.items():
        for filename in files:
            if folder in folders:
                datapath = folder_path + "/" + folder + "/" + filename
                with open(datapath) as f:
                    timestamp = f.readline()[5:-2]
                    file_data = pd.read_table(f, delimiter=',')

                data.append({"filename": filename, "timestamp": timestamp, "data": file_data})
    
    return data

def makelabel(file, settings = "time"):
    """Creates label from filename or timestamp
    settings can bei "time" or "name"
    """
    if settings == "time":
        plot_label = file['timestamp']

    elif settings == "name":
        plot_label = file['filename']

    else:
        plot_label = "none"
        print("Warning, wrong label settings")

    return plot_label

#TREATMENT FUNCTIONS


#PLOTTING
def make_plot(datalist, x_data_col = "Wavenumbers [1/cm]", y_data_col = "Absorbance"):
    """

    :param datalist:
    :return:
    """

    # prepare for figure with 2 x-axes
    print('Preparing a figure with 2 x-axes for plotting.')
    fig = plt.figure(figsize=(16,9))  # figsize=(3.999,2.1)
    ax1 = fig.add_subplot(111)

    #settings for data lines
    linestyle_list = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    color_list = ['b', 'g', 'k', 'orange', 'magenta', 'teal', 'purple', 'gold', '#5a7d9a']
    marker_list = []
    label_choice = "time" #alternative: "name"

    #plot data
    for (each_file, color, linestyle, marker) in itertools.zip_longest(datalist, color_list, linestyle_list, marker_list):
        try:
            ax1.plot(each_file['data'][x_data_col].values.tolist()[:-3],
                     each_file['data'][y_data_col].values.tolist()[:-3], color=color,
                     linestyle=linestyle, marker=marker, label=makelabel(each_file, label_choice))
        except TypeError:
            if len(datalist) < len(color_list) or len(datalist) < len(linestyle_list) or len(datalist) < len(marker_list):
                continue
            else:
                print("Problem plotting datalist...")


    # axis details
    ax1.set_xlabel(x_data_col, size=16)
    ax1.set_ylabel(y_data_col, size=16)
    ax1.tick_params(axis="both", labelsize=14, pad=8, direction="in", which="both",
                    width=1.5)
    ax1.set_xlim(4050, 500)
    ax1.set_ylim(0.0, 0.06)

    ax1.legend(fontsize=8, loc=(0, 1.05), ncol=2)

    # defines size of padding, important for legend on top, possibility to change space between subplots once implemented
    lpad = 0.15
    rpad = 0.15
    tpad = 0.10
    bpad = 0.15
    fig.subplots_adjust(left=lpad, right=1 - rpad, top=1 - tpad, bottom=bpad)

    plt.show()

def main():
    #read in the data
    datalist = import_csv(folder_path, filenames, folders)
    # print(datalist)
    # print(datalist[0]['data'])

    #make the plot
    make_plot(datalist)


if __name__ == "__main__":
    main()