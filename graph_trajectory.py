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

def plot_figure(computed_plot_info, actual_plot_info, xlabel, ylabel, alpha = 1.0):
    plt.figure()
    # graph actual (if provided)
    if actual_plot_info != {}:
        plt.plot(actual_plot_info["x_list"], 
                 actual_plot_info["y_list"], 
                 actual_plot_info["format"],
                 alpha = alpha,
                 label = actual_plot_info["label"],
                 markersize = 0.5)
    # graph computed
    plt.plot(computed_plot_info["x_list"],
             computed_plot_info["y_list"],
             computed_plot_info["format"],
             alpha = alpha,
             label = computed_plot_info["label"],
             markersize = 0.5)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

if __name__ == "__main__":
    # read file
    main_folder = r"C:\Users\teohz\Desktop\smoothness-visualizer"
    gt_path = main_folder + "\TM_10000_GT.csv"
    df = pd.read_csv(gt_path)
    
    # get one specific car
    df = df[df['ID'] == 5].reset_index(drop=True)
    x = df['x']
    time_x = df['Timestamp']
    
    # position
    computed_x = {"x_list": time_x, "y_list": x, "format": "tab:olive", "label": "Computed Position"}
    plot_figure(computed_x, {}, "time (seconds)", "position, x")
    
    # velocity
    v, time_v = get_derivative(x, time_x)
    computed_v = {"x_list": time_v, "y_list": v, "format": "tab:green", "label": "Computed Velocity"}
    actual_v = {"x_list": time_x, "y_list": -df['speed'], "format": "tab:olive", "label": "Actual Velocity"}
    plot_figure(computed_v, actual_v, "time (seconds)", "velocity, dx/dt", 0.9)
    
    # acceleration
    a, time_a = get_derivative(v, time_v)
    computed_a = {"x_list": time_a, "y_list": a, "format": "tab:blue", "label": "Computed Accleration"}
    actual_a = {"x_list": time_x, "y_list": -df['acceleration'], "format": "tab:olive", "label": "Actual Acceleration"}
    plot_figure(computed_a, actual_a, "time (seconds)", "acceleration, dv/dt", 0.9)
    
    # jerk
    j, time_j = get_derivative(a, time_a)
    computed_j =  {"x_list": time_j, "y_list": j, "format": "tab:red", "label": "Computed Jerk"}
    plot_figure(computed_j, {}, "time (seconds)", "jerk, da/dt")

    