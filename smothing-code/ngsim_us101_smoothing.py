# -*- coding: utf-8 -*-

# //$URL:: https://github.com/Rim-El-Ballouli/NGSIM-dataset-smoothing/tree/master/smothing-code
# //$Author:: Rim El Ballouli
# //$Date:: 31/12/2019

"""
This code
    1. smoothes out the noise in the local x and local y values in the NGSIM Dataset
    2. recomputes the velocites and accelerations
    3. saves smoothed dataset to three separate csv files
"""
import pandas as pd
import copy
from scipy import signal
from math import hypot



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

def get_file_name(index):
    if(index == 0):
        return file_name1.text.split('.', 1)[0]
    elif(index == 1):
        return file_name2.text.split('.', 1)[0]
    else :
        return file_name3.text.split('.', 1)[0]

def smooth_local_x_y(dataset, vehicle, window):
    """
    this function modifies the local x and local y column for a given vehicle ID
    in the dataset provided. The function replaces the original values
    with a smoothed value computed using the filter
    :param dataset:  data frame representing the dataset to smooth it's local X and Y
    :param vehicle: an integer value indicating the vehicle ID
                    the smoothing is restricted to trajectory values of this car
    :param window: a smoothing window must be an odd integer value
                    if it set to 11 this means points are smoothed with 1 second interval
                    if it set to 21 this means points are smoothed with 2 second interval
    """
    smoothed_x_values = signal.savgol_filter(dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_X'],
                                             window,  # window size used for filtering
                                             3)  # order of fitted polynomial
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_X'] = [x for x in smoothed_x_values]

    smoothed_y_values = signal.savgol_filter(dataset.loc[dataset['Vehicle_ID'] == vehicle,
                                             'Local_Y'], window, 3)
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'Local_Y'] = [x for x in smoothed_y_values]

def recompute_vel_acc(dataset, vehicle):
    """
    This function recomputes the velocity and acceleration for a given vehicle ID in a given dataset
    and replaces the values in the given dataset with the new computed values
    :param dataset: data frame representing the dataset to recompute its velocities and accelerations
    :param vehicle: an integer value indicating the vehicle ID
                    the velocities and accelerations of this vehicle is recomputed and replaced
    """
    # indexes of x, y and time columns in the dataset
    x_column = 4
    y_column = 5
    time_column = 3

    # maintain a list of smoothed velocities and acceleration
    # the first velocity and acceleration values can't be recomputed
    # therefore they are used as the first elements composing the lists
    smoothed_velocities = [dataset.loc[dataset['Vehicle_ID'] == vehicle].iloc[0, 11]]
    smoothed_accelaration = [dataset.loc[dataset['Vehicle_ID'] == vehicle].iloc[0, 12]]

    # a sub dataframe containing all trajectory data for a given vehicle ID
    ds = dataset[dataset['Vehicle_ID'] == vehicle]

    # iterate over the sub dataframe as a 2D array values
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

    # replace existing velocities and accelerations with recomputed values
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'v_Vel'] = [x for x in smoothed_velocities]
    dataset.loc[dataset['Vehicle_ID'] == vehicle, 'v_Acc'] = [x for x in smoothed_accelaration]

def print_to_file(dataset, file_name):
    """
    This functions saves a dataframe as a CSV file
    :param dataset: a dataframe representing the dataset
    :param file_name: name of the file to be saved
    """
    if (not path.exists(path_to_smoothed_dataset)):
        os.mkdir(path_to_smoothed_dataset)
        dataset.to_csv( path_to_smoothed_dataset + file_name + '_smoothed_' +
                                  str(smoothing_window) + '_.csv', index=False)

def recompute_all_vel_acc():
    """
    This functions iterates over the list of data frames representing the three dataset
    for the different time lines and recomputes the velocities and acceleration for each Vehicle in
    each dataset and prints the final output to a file in CSV format
    """
    for i in range(3):
        print(bcolors.OKGREEN + ' ######################### recomputing velocities for train data ' + str(i))
        for vehicle in train_smoothed[i]['Vehicle_ID'].unique():
            recompute_vel_acc(train_smoothed[i], vehicle)

        file_name = get_file_name(i)
        print_to_file(train_smoothed[i],file_name)



def smooth_dataset(window):
    """
     This functions iterates over the list of data frames representing the three dataset
    for the different time lines and smoothes the local x  and y values for each vehicle ID
    The local x & y values are replaced with the new ones

    smothing is done separately for each vehicle as the smoothed value of a target point
    is dependent on only on the x and y values for a specific vehicle.
    :param: window
    """
    global train_smoothed
    train_smoothed = copy.deepcopy(train[0:]) # copy of the train dataset
    for i in range(3):
        print(bcolors.OKBLUE + ' ######################### smoothing x y values in train data ' + str(i))

        for vehicle in train_smoothed[i]['Vehicle_ID'].unique():
            smooth_local_x_y(train_smoothed[i], vehicle, window)

    recompute_all_vel_acc()

if __name__ == '__main__':
    # smooth window must be an odd value
    smoothing_window = 21

    # specify the path to the input NGSIM dataset and the path to the output smoothed dataset
    path_to_dataset = 'C:/Users/relballouli/PycharmProjects/helloworld/trajectory/dataset/'
    path_to_smoothed_dataset = 'C:/Users/relballouli/PycharmProjects/helloworld/trajectory/dataset/smoothed/'

    # change the file names as needed
    file_name1 = '0750_0805_us101.csv'
    file_name2 = '0805_0820_us101.csv'
    file_name3 = '0820_0835_us101.csv'

    # load the NGSIM data from the CSV files
    train1 = pd.read_csv(path_to_dataset + file_name1, sep=',', encoding='latin-1')
    train2 = pd.read_csv(path_to_dataset + file_name2, sep=',', encoding='latin-1')
    train3 = pd.read_csv(path_to_dataset + file_name3, sep=',', encoding='latin-1')

    train = [train1, train2, train3]

    print('Smoothing window is set to ' + str(smoothing_window))
    smooth_dataset(smoothing_window)
