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
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import UnivariateSpline

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

def plot_figure(title, 
                plot_infos,
                xlabel, 
                ylabel, 
                alpha,
                output_file_name = "figure.png"):
    plt.figure()
    for plot_info in plot_infos:
        plt.plot(plot_info["x_list"], 
                 plot_info["y_list"], 
                 color = plot_info["color"],
                 alpha = alpha,
                 label = plot_info["label"],
                 markersize = 0.5)
    plt.ticklabel_format(useOffset=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(os.path.join(main_folder, output_file_name))

main_folder = r"C:\Users\teohz\Desktop\smoothness-visualizer"
trajectory_path = main_folder + "\TM_10000_GT.csv"

if __name__ == "__main__":
    # read file
    df_orig = pd.read_csv(trajectory_path)
    
    for car_id in range(1, 10):
        # get specific car_id (comment out if no id column in trajectory file)
        df = df_orig[df_orig['ID'] == car_id]
        df = df.reset_index(drop=True)
        
        # position
        x = df['x']
        time_x = df['Timestamp']
        # spline fit on position
        spl = InterpolatedUnivariateSpline(time_x, x)
        spl_time_x = np.linspace(min(time_x), max(time_x), 100)
        spl_x = spl(spl_time_x)
        # plot position
        plot_title = "Position: Car_id: " + str(car_id)
        plot_infos = [{"x_list": time_x, "y_list": x, "color": "tab:olive", "label": "Position"},
                      {"x_list": spl_time_x, "y_list": spl_x, "color": "tab:green", "label": "Spline Fit Position"}]
        output_file_name = "car" + str(car_id) + "_1_position.png"
        plot_figure(plot_title, plot_infos, "time (seconds)", "position, x", 1, output_file_name)
        
        # velocity
        v, time_v = get_derivative(x, time_x)
        v = -v
        spl_v, spl_time_v = get_derivative(spl_x, spl_time_x)
        spl_v = -spl_v
        # plot velocity
        plot_title = "Velocity: Car_id: " + str(car_id)
        plot_infos = [{"x_list": time_v, "y_list": v, "color": "tab:olive", "label": "Velocity"}, 
                      {"x_list": spl_time_v, "y_list": spl_v, "color": "tab:green", "label": "Spline Fit Velocity"}]
        output_file_name = "car" + str(car_id) + "_2_velocity.png"
        plot_figure(plot_title, plot_infos, "time (seconds)", "velocity, dx/dt", 0.9, output_file_name)
        
        # acceleration
        a, time_a = get_derivative(v, time_v)
        spl_a, spl_time_a = get_derivative(spl_v, spl_time_v)
        # plot acceleration
        plot_title = "Acceleration: Car_id: " + str(car_id)
        plot_infos = [{"x_list": time_a, "y_list": a, "color": "tab:olive", "label": "Accleration"},
                      {"x_list": spl_time_a, "y_list": spl_a, "color": "tab:green", "label": "Spline Fit Acceleration"}]
        output_file_name = "car" + str(car_id) + "_3_acceleration.png"
        plot_figure(plot_title, plot_infos, "time (seconds)", "acceleration, dv/dt", 0.9, output_file_name)
        
        # jerk
        j, time_j = get_derivative(a, time_a)
        spl_j, spl_time_j = get_derivative(spl_a, spl_time_a)
        # plot jerk
        plot_title = "Jerk: Car_id: " + str(car_id)
        plot_infos =  [{"x_list": time_j, "y_list": j, "color": "tab:olive", "label": "Jerk"},
                       {"x_list": spl_time_j, "y_list": spl_j, "color": "tab:green", "label": "Spline Fit Jerk"}]
        output_file_name = "car" + str(car_id) + "_4_jerk.png"
        plot_figure(plot_title, plot_infos, "time (seconds)", "jerk, da/dt", 1, output_file_name)
        
    