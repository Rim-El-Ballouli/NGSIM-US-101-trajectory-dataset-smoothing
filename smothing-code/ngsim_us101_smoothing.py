# -*- coding: utf-8 -*-

# Copyright (c) 2019 Altran Prototypes Automobiles (APA), Velizy-Villacoublay, France. All rights reserved.
# //$URL:: https://github.com/Rim-El-Ballouli/NGSIM-dataset-smoothing/tree/master/smothing-code
# //$Author:: Rim El Ballouli
# //$Date:: 31/12/2019

"""
This code aims at smoothing out the noise in the local x and local y values in the NGSIM Dataset

"""
import pandas as pd
from scipy import signal
from math import hypot
import copy
import os.path
from os import path

# A class defining color variables used to beautify console printing of the smoothing progress
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# smooth window must be an odd value
# if it set to 11 this means points are smoothed with 1 second interval
# if it set to 21 this means points are smoothed with 2 second interval
smoothing_window = 21

# specify the path to the input NGSIM dataset and the path to the output smoothed dataset
path_to_dataset = 'C:/Users/relballouli/PycharmProjects/helloworld/trajectory/dataset/'
path_to_smoothed_dataset = 'C:/Users/relballouli/PycharmProjects/helloworld/trajectory/dataset/smoothed/'

# load the NGSIM data from the CSV files
# change the file names as needed
train1 = pd.read_csv(path_to_dataset + '0750_0805_us101.csv', sep=',', encoding='latin-1')
train2 = pd.read_csv(path_to_dataset + '0805_0820_us101.csv', sep=',', encoding='latin-1')
train3 = pd.read_csv(path_to_dataset + '0820_0835_us101.csv', sep=',', encoding='latin-1')

train = [train1, train2, train3]

def get_file_name(index):
    """
    This function
    :param index:
    :return:
    """
    if(index == 0):
        return '0750_0805_us101'
    elif(index == 1):
        return '0805_0820_us101'
    else :
        return '0820_0835_us101'

def smooth_local_x_y(dataset, vehicle, window):
    """

    :param dataset:
    :param vehicle:
    :param window:
    :return:
    """
    smoothed_x_values = signal.savgol_filter(dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_X'],
                                             window,  # window size used for filtering
                                             3)  # order of fitted polynomial
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_X'] = [x for x in smoothed_x_values]

    smoothed_y_values = signal.savgol_filter(dataset.loc[dataset['Vehicle_ID'] == vehicle,
                                             'Local_Y'], window, 3)
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_Y'] = [x for x in smoothed_y_values]

def recompute_all_vel_acc():
    for i in range(3):
        print(bcolors.OKGREEN + ' ######################### recomputing velocities for train data ' + str(i))
        for vehicle in train_smoothed[i]['Vehicle_ID'].unique():
            recompute_vel_acc(train_smoothed[i], vehicle)
            file_name = get_file_name(i)

        if (not path.exists(path_to_smoothed_dataset)):
            os.mkdir(path_to_smoothed_dataset)
        train_smoothed[i].to_csv(
            path_to_smoothed_dataset + file_name + '_smoothed_' + str(smoothing_window) + '_.csv',
            index=False)

def recompute_vel_acc(dataset, vehicle):
    # indexes of x, y and time columns
    x_column = 4
    y_column = 5
    time_column = 3

    # first velocity value cant be calculated therefore it is taken as is
    smoothed_velocities = [dataset.loc[dataset['Vehicle_ID'] == vehicle].iloc[0, 11]]
    smoothed_accelaration = [dataset.loc[dataset['Vehicle_ID'] == vehicle].iloc[0, 12]]
    ds = dataset[dataset['Vehicle_ID'] == vehicle]
    for row in range(len(ds)-1):
        curr_x_value = ds.iloc[row, x_column]
        curr_y_value = ds.iloc[row, y_column]
        curr_time_value = ds.iloc[row, time_column]

        next_x_value = ds.iloc[row+1, x_column]
        next_y_value = ds.iloc[row+1, y_column]
        next_time_value = ds.iloc[row+1, time_column]

        dist = hypot(next_x_value - curr_x_value, next_y_value - curr_y_value)
        delta_time = next_time_value - curr_time_value
        velocity = (dist / delta_time) * 1000 # convert to sec
        smoothed_velocities.append(velocity)

        acceleration = ((velocity - smoothed_velocities[row])  / delta_time )* 1000
        smoothed_accelaration.append(acceleration)
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'v_Vel'] = [x for x in smoothed_velocities]
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'v_Acc'] = [x for x in smoothed_accelaration]

def smooth_dataset(window):
    """
    smothing should happen separately for each vehicle as the smoothed value of a target point
    is dependent on the x and y values  before and after the target value.
    therefore we don't the x and y values of the last point of one vehicle to be affected by
    the trajectory of other vehicles in the dataset
    :return:
    """
    global train_smoothed
    if (path.exists(path_to_smoothed_dataset + '0750_0805_us101_smoothed_' + str(smoothing_window) + '_.csv') &
            path.exists(path_to_smoothed_dataset + '0805_0820_us101_smoothed_' + str(smoothing_window) + '_.csv') &
            path.exists(path_to_smoothed_dataset + '0820_0835_us101_smoothed_' + str(smoothing_window) + '_.csv')):

        t1 = pd.read_csv(path_to_smoothed_dataset + '0750_0805_us101_smoothed_' + str(smoothing_window) + '_.csv', sep=',',
                         encoding='latin-1')
        t2 = pd.read_csv(path_to_smoothed_dataset + '0805_0820_us101_smoothed_' + str(smoothing_window) + '_.csv', sep=',',
                         encoding='latin-1')
        t3 = pd.read_csv(path_to_smoothed_dataset + '0820_0835_us101_smoothed_' + str(smoothing_window) + '_.csv', sep=',',
                         encoding='latin-1')
        train_smoothed = [t1, t2, t3]
    else :
        train_smoothed = copy.deepcopy(train[0:]) # copy of the train dataset
        for i in range(3):
            print(bcolors.OKBLUE + ' ######################### smoothing x y values in train data ' + str(i))
            for vehicle in train_smoothed[i]['Vehicle_ID'].unique():
                smooth_local_x_y(train_smoothed[i], vehicle, window)
        recompute_all_vel_acc()

if __name__ == '__main__':
    print('Smoothing window is set to ' + str(smoothing_window))
    smooth_dataset(smoothing_window)




