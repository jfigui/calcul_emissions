#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================================
calcul_emissions.py
================================================

Programma per calcular l'estalvi setmanal en emissions de CO2 aconseguit
gràcies a la participacio en el bicibus de l'entorn.

Simplificacions dels calculs:
- Nomes es computen els trajectes dels nens
- Es parteix de la base que cada nen utilitzaria un cotxe
- Tots els trajectes son calculats des de l'origen de la linia
- Emissions per cotxe calculades segons: 
  https://impactco2.fr/transport/voiturethermique

"""

# Author: fvj
# License: BSD 3 clause

import datetime
import dateutil
import argparse
import atexit

import pandas as pd
import numpy as np

import matplotlib as mpl
mpl.use('Agg')

# Increase a bit font size
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family':  "sans-serif"})

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


print(__doc__)


def main():
    """
    main
    """

    # parse the arguments
    parser = argparse.ArgumentParser(
        description="Calcul d'emissions")

    # keyword arguments
    parser.add_argument(
        '--path', type=str,
        default='/home/mdso/figuerasiventuraj/calcul_emissions/',
        help='nom del directory que conté els trajectes per linia per setmana')
        
    parser.add_argument(
        '--fname', type=str,
        default='viatges_bicibus_entorn.csv',
        help='nom del fitxer que conté els trajectes per linia per setmana')
        
    parser.add_argument(
        '--fname_out', type=str,
        default='estalvi_co2_bicibus_entorn.png',
        help='nom del fitxer que conté els trajectes per linia per setmana')

    args = parser.parse_args()

    print("====== Inici del calcul d'emissions: %s" %
          datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    atexit.register(_print_end_msg,
                    "====== fi del calcul d'emissions ")


    emissions_cotxe = 217.60  # g/km

    # distancia de cada linia a l'escola (km)
    d_mianigues = 0.8
    d_petanca = 0.9
    d_andreu = 0.8
    
    # lectura del fitxer amb les distancies recorregudes per setmana
    df = pd.read_csv(f'{args.path}{args.fname}')    

    # distancia total recorreguda
    df['emissions_setmana'] = (
        df['viatges_mianigues']*d_mianigues+df['viatges_petanca']*d_petanca
        + df['viatges_StAndreu']*d_andreu)
    df['emissions_acumulades'] = df['emissions_setmana'].cumsum()
    
    print(df)
    
    plot_timeseries(df, [f'{args.path}{args.fname_out}'])
    
    
def plot_timeseries(df, fname_list, labelx='Setmana',
                    labely='Emissions de CO2 (g)', title="Estalvi d'emissions de CO2",
                    timeformat=None, colors=None, linestyles=None,
                    markers=None, ymin=None, ymax=None, dpi=72):
    """
    plots a time series

    Parameters
    ----------
    tvec : datetime object
        time of the time series
    data_list : list of float array
        values of the time series
    fname_list : list of str
        list of names of the files where to store the plot
    labelx : str
        The label of the X axis
    labely : str
        The label of the Y axis
    labels : array of str
        The label of the legend
    title : str
        The figure title
    period : float
        measurement period in seconds used to compute accumulation. If 0 no
        accumulation is computed
    timeformat : str
        Specifies the tvec and time format on the x axis
    colors : array of str
        Specifies the colors of each line
    linestyles : array of str
        Specifies the line style of each line
    markers: array of str
        Specify the markers to be used for each line
    ymin, ymax: float
        Lower/Upper limit of y axis
    dpi : int
        dots per inch

    Returns
    -------
    fname_list : list of str
        list of names of the created plots

    History
    --------
    201?.??.?? -fvj- creation
    2017.08.21 -jgr- modified margins and grid + minor graphical updates
    2018.03.05 -jgr- added x-limit of x axis to avoid unwanted error messages

    """
    fig, ax = plt.subplots(figsize=[10, 6], dpi=dpi)

    lab = None
    col = None
    lstyle = '--'
    marker = 'o'

    
    df.plot.bar(x='setmana', y='emissions_setmana', ax=ax, rot=0)
    
    #ax2 = ax.twinx()
    
    ax.plot(
        ax.get_xticks(), df['emissions_acumulades'].values, marker='o',
        color='red', label='emissions_acumulades')        
    ax.legend()

    ax.set_title(title)
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    # ax.set_ylim(bottom=ymin, top=ymax)
    # ax.set_xlim([tvec[0], tvec[-1]])

    # Turn on the grid
    ax.grid()

    if timeformat is not None:
        ax.xaxis.set_major_formatter(mdates.DateFormatter(timeformat))

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    # fig.autofmt_xdate()

    # Make a tight layout
    fig.tight_layout()

    for fname in fname_list:
        fig.savefig(fname, dpi=dpi)
    plt.close(fig)

    return fname_list
    

def _print_end_msg(text):
    """
    prints end message

    Parameters
    ----------
    text : str
        the text to be printed

    Returns
    -------
    Nothing

    """
    print(text + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


# ---------------------------------------------------------
# Start main:
# ---------------------------------------------------------
if __name__ == "__main__":
    main()

