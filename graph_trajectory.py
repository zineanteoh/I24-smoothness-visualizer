# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 11:15:36 2022

@author: teohz

@brief: this program plots and saves trajectory graph up to 
        3rd derivative (jerk). 
        derivatives are computed using discrete-time derivatives
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

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

def plot_figure(car_id, 
                computed_plot_info, 
                actual_plot_info, 
                xlabel, 
                ylabel, 
                alpha,
                output_file_name = "figure.png"):
    plt.figure()
    # graph actual (if provided)
    if actual_plot_info != {}:
        plt.plot(actual_plot_info["x_list"], 
                 actual_plot_info["y_list"], 
                 color = actual_plot_info["color"],
                 alpha = alpha,
                 label = actual_plot_info["label"],
                 markersize = 0.5)
    # graph computed
    if computed_plot_info != {}:
        plt.plot(computed_plot_info["x_list"],
                 computed_plot_info["y_list"],
                 color = computed_plot_info["color"],
                 linestyle = "-",
                 alpha = alpha,
                 label = computed_plot_info["label"],
                 markersize = 0.5)
    plt.title("Car_id: " + str(car_id))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(os.path.join(main_folder, output_file_name))

main_folder = r"C:\Users\teohz\Desktop\smoothness-visualizer"
trajectory_path = main_folder + "\TM_10000_GT.csv"

if __name__ == "__main__":
    # read file
    df = pd.read_csv(trajectory_path)
    
    for car_id in range(1, 7):
        # get specific car_id (comment out if no id column in trajectory file)
        df = df[df['ID'] == car_id]
        df = df.reset_index(drop=True)
        x = df['x']
        time_x = df['Timestamp']
        
        # position
        output_file_name = "car" + str(car_id) + "_1_position.png"
        computed_x = {"x_list": time_x, "y_list": x, "color": "tab:olive", "label": "Actual Position"}
        plot_figure(car_id, computed_x, {}, "time (seconds)", "position, x", 1, output_file_name)
        
        # velocity
        output_file_name = "car" + str(car_id) + "_2_velocity.png"
        v, time_v = get_derivative(x, time_x)
        computed_v = {"x_list": time_v, "y_list": -v, "color": "tab:green", "label": "Computed Velocity"}
        actual_v = {"x_list": time_x, "y_list": df['speed'], "color": "tab:olive", "label": "Actual Velocity"}
        plot_figure(car_id, computed_v, actual_v, "time (seconds)", "velocity, dx/dt", 0.9, output_file_name)
        
        # acceleration
        output_file_name = "car" + str(car_id) + "_3_acceleration.png"
        a, time_a = get_derivative(v, time_v)
        computed_a = {"x_list": time_a, "y_list": -a, "color": "tab:blue", "label": "Computed Accleration"}
        actual_a = {"x_list": time_x, "y_list": df['acceleration'], "color": "tab:olive", "label": "Actual Acceleration"}
        plot_figure(car_id, computed_a, actual_a, "time (seconds)", "acceleration, dv/dt", 0.9, output_file_name)
        
        # jerk
        output_file_name = "car" + str(car_id) + "_4_jerk.png"
        j, time_j = get_derivative(a, time_a)
        computed_j =  {"x_list": time_j, "y_list": j, "color": "tab:red", "label": "Computed Jerk"}
        plot_figure(car_id, computed_j, {}, "time (seconds)", "jerk, da/dt", 1, output_file_name)

    