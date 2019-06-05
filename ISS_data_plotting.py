"""
Created on Thu Sep  27 15:08 2018

@author: Anna

Simple script to import CSV data as DataFrame according to absolute data path, possible data treatment, and plotting
using matplotlib.

Specifically written for importing FT-IR data exported as csv using software spectragryph.
 Version 24.1.2019: updates so it's optimized to plot data from one single csv with several colums into an xyz shape,
 rather than plotting single spectra

 THIS ONE HERE modified for reading in and plotting ISS data

"""

from pandas import DataFrame
import pandas as pd
import itertools
import json
from collections import OrderedDict
import matplotlib
# matplotlib.use('qt4agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import re
from mpl_toolkits.mplot3d import Axes3D #THIS IS ACTUALLY USED!! DONT DELETE
import os




#DATA IMPORT PARAMETERS
folder_path = r'C:\Users\annawi\Desktop\Projects\Propene oxidation\Experiments\201905_PdAufoams\XPS + ISS\ISS - before_after echem'
folders = [
    'ISS_as_prep',
    # 'ISS_after5s_sputter',
    # 'ISS_after2x5s_Arsputter',
    'ISS after 3x5s Ar sputter',
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
    ('ISS_after5s_sputter', [
        # 'Au foam large_5sArsputter.avg',
        # 'Au foam 004 after EC_5sArsputter.avg',
        # 'AuPd  foam 1090 002_5sArsputter.avg',
        # 'AuPd foam 1090 001 post EC_5sArsputter.avg',
        # 'AuPd foam 9010 002_5sArsputter.avg',
        # 'AuPd foam 9010 003 post EC_5sArsputter.avg',
        'Pd foam large_5sArsputter.avg'
    ]),
    ('ISS_after2x5s_Arsputter', [
        # 'Au foam large_2x5sArsputter.avg',
        # 'Au foam 004 after EC_2x5sArsputter.avg',
        # 'AuPd  foam 1090 002_2x5sArsputter.avg',
        # 'AuPd foam 1090 001 post EC_2x5sArsputter.avg',
        # 'AuPd foam 9010 002_2x5sArsputter.avg',
        # 'AuPd foam 9010 003 post EC_2x5sArsputter.avg',
        'Pd foam large_2x5sArsputter.avg'
    ]),
    ('ISS after 3x5s Ar sputter', [
            # 'Au foam large_3x5sArsputter.avg',
    # 'Au foam 004 after EC_3x5sArsputter.avg',
    #       'AuPd  foam 1090 002_3x5sArsputter.avg',
    #     'AuPd foam 1090 001 post EC_3x5sArsputter.avg',
    #     'AuPd foam 9010 002_3x5sArsputter.avg',
    #     'AuPd foam 9010 003 post EC_3x5sArsputter.avg',
        'Pd foam large_3x5sArsputter.avg'
    ]),


])


#IMPORTING FUNCTIONS

#info about datastructure of the FT-IR data:
#first line contains timestamp -> important to sync with EC data
#2nd line is column header, from then on data
#comma separated


def import_csv(folder_path, filenames, folders):
    """
    importing of data as csv - tailored to ISS data here
    :param folder_path, filenames, folders
    :return: data
    """
    data = []
    column_header =["Kinetic energy / eV", "Intensity / CPS"]
    for folder, files in filenames.items():
        for filename in files:
            if folder in folders:
                datapath = folder_path + "/" + folder + "/" + filename
                print("now working on " + filename)
                with open(datapath) as f:
                    timestamp=[]
                    file_data={}
                    file_data_raw = np.genfromtxt(f, skip_header=20, unpack=True)
                    # print(file_data_raw)
                    # file_data.rename(columns={'':'CPS'}, inplace=True)
                    file_data[column_header[0]], file_data[column_header[1]] = file_data_raw
                    # print(file_data)

                    data.append({"filename": filename, "timestamp": timestamp, "data": file_data})

    return data


def import_avg(folder_path, filenames, folders, energy_step=1):
    """
    importing of ISS data in avg format as produced by DataSpace_BatchDump.exe
    :param folder_path, filenames, folders
    :return: data
    """
    data = []
    column_header = ["Kinetic energy / eV", "Intensity / CPS"]
    for folder, files in filenames.items():
        for filename in files:
            if folder in folders:
                datapath = folder_path + "/" + folder + "/" + filename
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
def make_plot(datalist, x_data_col = "Kinetic energy / eV", y_data_col="Intensity / CPS", logplot= False,
              theory_lines=[886.4, 835.5, 645.1, 618.9, 396.4], save_plot = False, y_data_sorted=True, timelimit=(53469,60000), combi_plot=False):
    """
    makes a new plot for each line of data in datalist if combi_plot=False, else all in one plot (standard: separate plots)
    :param datalist:

    theory_lines=[938.1, 888.4, 699.9, 673.7, 446.7] : calculated for 1000eV and 125degrees : Au, Pd, Cl, S, O
    theory_lines=[886.4, 835.5, 645.1, 618.9, 396.4] : calculated for 950eV and 135degrees :  Au, Pd, Cl, S, O
    :return:
    """
    if combi_plot == True:
        fig = plt.figure(figsize=(16, 9))

    for dataline in datalist:
        # print(dataline)
        # prepare for figure with 2 x-axes
        print('Preparing a figure with 2 x-axes for plotting.')

        if not combi_plot:
            fig = plt.figure(figsize=(16,9))  # figsize=(3.999,2.1)

        ax1 = fig.add_subplot(111)

        # #find y colums to plot
        # if y_data_sorted:
        #     columns = list(dataline['sorted_y_data'])
        # else:
        #     columns = list(dataline['data'])
        # no_of_lines = len(columns)
        # print(columns)

        # # settings for data lines
        # linestyle_list = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        # cmap = cm.get_cmap('viridis')
        # color_list = [cmap(x/no_of_lines-0.05) for x in range(no_of_lines)]
        # # color_list = ['b', 'g', 'k', 'orange', 'magenta', 'teal', 'purple', 'gold', '#5a7d9a']
        # marker_list = []
        # label_choice = "time"  # alternative: "name"



        #plot with logaritmic y-axis for better visibility of the small Pd peaks
        if logplot == True:
            ax1.semilogy(dataline['data'][x_data_col], dataline['data'][y_data_col], label=dataline['filename'])

        else:# plot data 2D
            ax1.plot(dataline['data'][x_data_col], dataline['data'][y_data_col], label=dataline['filename'])  # label=makelabel(dataline, label_choice))




        # axis details
        ax1.set_xlabel(x_data_col, size=16, labelpad=20)
        ax1.set_ylabel(y_data_col, size=16, labelpad=20)
        ax1.tick_params(axis="both", labelsize=14, pad=10, direction="in", which="both",
                        width=1.5)

        ax1.legend(fontsize=8, loc=(0, 1.05), ncol=2)

        # defines size of padding, important for legend on top, possibility to change space between subplots once implemented
        lpad = 0.15
        rpad = 0.15
        tpad = 0.10
        bpad = 0.15
        fig.subplots_adjust(left=lpad, right=1 - rpad, top=1 - tpad, bottom=bpad)

        #add lines of reference values
        ymin, ymax = ax1.get_ylim()
        for line_value in theory_lines:
            x_data_line = [line_value for x in range(int(ymax))]
            y_data_line = [y for y in range(int(ymax))]
            ax1.plot(x_data_line,y_data_line, 'k:')


        #save the plot
        if not combi_plot:
            if save_plot == True:
                save_the_plot(dataline['filename'], logplot)

    if combi_plot:
        if save_plot == True:
            save_the_plot(dataline['filename'] + "_combi", logplot)
    plt.show()


def save_the_plot(filename, logplot):
    if logplot == True:
        if os.path.exists(folder_path + "\\" + filename + '_log.png'):
            overwrite = input("Do you want to overwrite an existing plot? (y/n)")
            if overwrite == "y" or overwrite == "yes":
                print("Overwriting file.")
            else:
                filename = input("Enter new filename:")

        plt.savefig(folder_path + "\\" + filename + '_log.pdf', dpi=300, bbox_inches='tight')
        plt.savefig(folder_path + "\\" + filename + '_log.png', dpi=300, bbox_inches='tight')
        print("Figure saved.")
    else:
        if os.path.exists(folder_path + "\\" + filename + '.png'):
            overwrite = input("Do you want to overwrite an existing plot? (y/n)")
            if overwrite == "y" or overwrite == "yes":
                print("Overwriting file.")
            else:
                filename = input("Enter new filename:")

        plt.savefig(folder_path + "\\" + filename + '.pdf', dpi=300, bbox_inches='tight')
        plt.savefig(folder_path + "\\" + filename + '.png', dpi=300, bbox_inches='tight')
        print("Figure saved.")



if __name__ == '__main__':
    #read in the data
    # datalist = import_csv(folder_path, filenames, folders) #from csv format
    datalist = import_avg(folder_path, filenames, folders) #from avg format
    # print(datalist)
    # print(datalist[0]['data'])

    #make the plot
    # make_plot(datalist)


