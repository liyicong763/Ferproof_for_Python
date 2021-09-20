# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Scatter_plot(x, y) :
    plt.figure(figsize= (15, 15))
    plt.plot(x, y, 'o')
    plt.grid(ls = '--')
    plt.show()

def Scatter_plots(x, y, y1, z, tp11, tp12, tp21, tp22) :
    plt.figure(figsize= (15, 15))
    plt.plot(x, y, 'o', color='#f3938c')
    plt.plot(x, y1, 'o', color='#f34a3e')
    plt.plot(x, z, 'o', color='#9c27b0')
    plt.plot(x, tp11, 'o', color='#03a9f4')
    plt.plot(x, tp12, 'o', color='#81aec3')
    plt.plot(x, tp21, 'o', color='#237b26')
    plt.plot(x, tp22, 'o', color='#78ad7a')
    plt.grid(ls = '--')
    plt.show()