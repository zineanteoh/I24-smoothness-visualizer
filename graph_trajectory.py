# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 11:15:36 2022

@author: teohz

@brief: graphs a trajectory file 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_derivative(function, time):
    '''
    Parameters
    ----------
    function : list of N points at time t
    time : list of N points corresponding to function at time t

    Returns
    -------
    f_prime : list of df/dt at time t, the midpoint of two adjacent points
                in the original function
    t_prime : list of (N - 1) points corresponding to f_prime at time t
    '''
    f_prime = np.diff(function)/np.diff(time)
    t_prime = []
    for i in range(len(f_prime)):
        t_temp = (time[i + 1] + time[i]) / 2
        t_prime = np.append(t_prime, t_temp)
    return f_prime, t_prime

def plot_figure(x_list, y_list, color, label, xlabel, ylabel):
    plt.figure()
    plt.plot(x_list, y_list, color + "x", label=label, markersize=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

if __name__ == "__main__":
    # read file
    main_folder = r"C:\Users\teohz\Desktop\smoothness-visualizer"
    gt_path = main_folder + "\TM_10000_GT.csv"
    df = pd.read_csv(gt_path)
    
    # get one specific car
    df = df[df['ID'] == 5]
    x = df['x'].reset_index(drop=True)
    time_x = df['Timestamp'].reset_index(drop=True)
    
    # position
    plot_figure(time_x, x, "b", "Position", "time (seconds)", "position, x")
    
    # velocity
    v, time_v = get_derivative(x, time_x)
    plot_figure(time_v, v, "g", "Velocity", "time (seconds)", "velocity, dx/dt")
    
    # acceleration
    a, time_a = get_derivative(v, time_v)
    plot_figure(time_a, a, "m", "Acceleration", "time (seconds)", "acceleration, dv/dt")
    
    # jerk
    j, time_j = get_derivative(a, time_a)
    plot_figure(time_j, j, "y", "Jerk", "time (seconds)", "jerk, da/dt")

    