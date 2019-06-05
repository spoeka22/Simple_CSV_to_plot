"""
Created on Thu Sep  27 15:08 2018

@author: Anna

Simple script to import CSV data as DataFrame according to absolute data path, possible data treatment, and plotting
using matplotlib.

Specifically written for importing FT-IR data exported as csv using software spectragryph.
 Version 24.1.2019: updates so it's optimized to plot data from one single csv with several colums into an xyz shape,
 rather than plotting single spectra

"""

from pandas import DataFrame
import pandas as pd
import itertools
import json
from collections import OrderedDict
import matplotlib
matplotlib.use('qt4agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import re
from mpl_toolkits.mplot3d import Axes3D #THIS IS ACTUALLY USED!! DONT DELETE
import os




#DATA IMPORT PARAMETERS
folder_path = r'C:\Users\annawi\Desktop\Projects\Propene oxidation\IR_experiments'
folders =[
            # r'\20181121\112118\treated spectra',
            r'\20181127\112718\treated spectra',
            # r'20181128\112818\treated spectra',

          ]
filenames =OrderedDict([
          (r'\20181121\112118\treated spectra', ['20181122_firstCO_strip_simpleBL_corrH2OvAPCORR.csv',
                                                 '20181122_propenepurge+secondCO_strip_firstspecsubtracted_simple_BLcorr_H2Ovapcorr.csv',
                                                 '20181122_thridCO_purge_BLcorr_referencespecbeforepurgesubtracted_H2Ovapsubtr.csv'
                                                  ]),
          (r'\20181127\112718\treated spectra', [#'20181127_COstrip_1_allspectra_initial400mVsubtracted_H2Ovap_subtr_simple_BL_corr.csv',
                                                  # '20181127_COstrip_2_allspectra_initial400mVsubtracted_simple_BL_corr.csv',
                                                 '20181127_COstrip_3_allspectra_initial400mVsubtracted_simple_BL_coor.csv',
                                                 # '20181127_COstrip_4_allspectra_initial400mVsubtracted_H2Ovap_subtr_simple_BL_corr.csv',
                                                 # '20181127_COstrip_5_allspectra_initial400mVsubtracted_simple_BL_corr.csv'
                                                 ]),
          (r'20181128\112818\treated spectra', ['20181128_spectra_beforefirstleakfix_COstrip1_initialsubtracted_BL_corr.csv',
                                          '20181128_spectra_beforefirstleakfix_COstrip2_initialsubtr_H2Ovapsubtr_BL_corr.csv',
                                          '20181128_spectra_afterfirstleakfix_COstrip3_initialArsubtracted_H2Ovapsubtr_BL_corr.csv',
                                          '20181128_spectra_afterfirstleakfix_COstrip4_initialsubtr_H2Ovapcorr_BL_corr.csv'
                                          ])
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
                    timestamp=[]
                    file_data = pd.read_table(f, delimiter=',')
                    file_data.rename(columns={'Unnamed: 0':'Wavenumbers [1/cm]'}, inplace=True)
                    # print(file_data)
                    columns = list(file_data)
                    # print(columns)
                    for column in columns:
                        time = re.search(r'\d{2}:\d{2}:\d{2}', column)
                        if time:
                            timestamp.append(time.group(0))
                        else:
                            timestamp.append("NaN")
                    # print(timestamp)
                    new_colum_names=dict(zip(columns, timestamp))
                    # print(new_colum_names)
                    file_data_2= file_data.rename(columns=new_colum_names, inplace=False)
                    # print(file_data_2)
                    file_data_sorted = file_data_2.sort_index(axis=1, ascending=False )
                    # print(file_data_sorted)
                    data.append({"filename": filename, "timestamp": timestamp, "data": file_data, "sorted_y_data":file_data_sorted})
    
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
def make_plot(datalist, x_data_col = "Wavenumbers [1/cm]", y_data_col="Absorbance a.u.", y_data_sorted=True, timelimit=(53469,60000)):
    """
    makes a new plot for each line of data in datalist
    :param datalist:
    :return:
    """
    for dataline in datalist:
        # print(dataline)
        # prepare for figure with 2 x-axes
        print('Preparing a figure with 2 x-axes for plotting.')

        fig = plt.figure(figsize=(16,9))  # figsize=(3.999,2.1)
        ax1 = fig.add_subplot(111, projection='3d')

        #find y colums to plot
        if y_data_sorted:
            columns = list(dataline['sorted_y_data'])
        else:
            columns = list(dataline['data'])
        no_of_lines = len(columns)
        print(columns)

        # settings for data lines
        linestyle_list = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        cmap = cm.get_cmap('viridis')
        color_list = [cmap(x/no_of_lines-0.05) for x in range(no_of_lines)]
        # color_list = ['b', 'g', 'k', 'orange', 'magenta', 'teal', 'purple', 'gold', '#5a7d9a']
        marker_list = []
        label_choice = "time"  # alternative: "name"



        # # plot data 2D
        # for (column, color, linestyle, marker) in itertools.zip_longest(columns, color_list, linestyle_list,
        #                                                                 marker_list):
        #     try:
        #         ax1.plot(dataline['data'][x_data_col].values.tolist()[1:-3],
        #                  dataline['data'][column].values.tolist()[1:-3], color=color,
        #                  linestyle=linestyle, marker=marker, )  # label=makelabel(dataline, label_choice))
        #     except TypeError:
        #         if len(datalist) < len(color_list) or len(datalist) < len(linestyle_list) or len(
        #                 datalist) < len(marker_list):
        #             continue
        #         else:
        #             print("Problem plotting datalist...")
        #

        # plot data 3D
        for (column, color, linestyle, marker) in itertools.zip_longest(columns, color_list, linestyle_list,
                                                                        marker_list):
        #     print(column)
            #find timestamp from column header - seems to be the most straightforward way to do that without adding extra loops
            if column:
                try:
                    time = re.search(r'\d{2}:\d{2}:\d{2}', column).group(0)
                    time_seconds = float(time[0:2]) * 3600 + float(time[3:5]) * 60 + float(time[6:])
                    z_coordinate = time_seconds
                except AttributeError:
                    print("no time in column name")
                    continue
            else:
                continue

            if z_coordinate <= timelimit[0] or z_coordinate >= timelimit[1]:
                print("Spectrum not within the give time limits. I continue.")
                continue



            x_list = [float(x) for x in dataline['data'][x_data_col].values.tolist()[1:-3]]
            if y_data_sorted:
                y_list = [float(y) for y in dataline["sorted_y_data"][time].values.tolist()[1:-3]]
            else:
                y_list = [float(y) for y in dataline['data'][column].values.tolist()[1:-3]]
            z_list = [z_coordinate for x in range(len(x_list))]

            try:
                ax1.plot(x_list, z_list, zs=y_list, color=color,
                        linestyle=linestyle, marker=marker )  # label=makelabel(dataline, label_choice))

            except TypeError:
                if len(datalist) < len(color_list) or len(datalist) < len(linestyle_list) or len(datalist) < len(marker_list):
                    continue
                else:
                    print("Problem plotting datalist...")

        #3D persepective
        ax1.view_init(elev=51, azim=-77)


        # axis details
        ax1.set_xlabel(x_data_col, size=16, labelpad=20)
        ax1.set_ylabel("time / s", size=16, labelpad=20)
        ax1.set_zlabel(y_data_col, size=16, labelpad=20)
        ax1.tick_params(axis="both", labelsize=14, pad=10, direction="in", which="both",
                        width=1.5)
        ax1.set_xlim(4050, 500) #wavenumber
        ax1.set_zlim(-0.005, 0.01) #absorbance
        # ax1.set_ylim(44850) #time

        ax1.legend(fontsize=8, loc=(0, 1.05), ncol=2)

        # defines size of padding, important for legend on top, possibility to change space between subplots once implemented
        lpad = 0.15
        rpad = 0.15
        tpad = 0.10
        bpad = 0.15
        fig.subplots_adjust(left=lpad, right=1 - rpad, top=1 - tpad, bottom=bpad)

        #save the plot
        if os.path.exists("output_files/" + dataline['filename'] + '.png'):
            overwrite = input("Do you want to overwrite an existing plot? (y/n)")
            if overwrite == "y" or overwrite == "yes":
                print("Overwriting file.")
            else:
                dataline['filename'] = input("Enter new filename:")

        plt.savefig("output_files/" + dataline['filename'] + '.pdf', dpi=300, bbox_inches='tight')
        plt.savefig("output_files/" + dataline['filename'] + '.png', dpi=300, bbox_inches='tight')
        print("Figure saved.")

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