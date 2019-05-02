import pandas as pd
import matplotlib.pyplot as plt
from util import get_data
import numpy as np


def author(self):
    return 'akapoor64'


# Indicator - Simple moving average
def simple_moving_average_over_window(values, window):
    return values.rolling(window).mean()


def simple_moving_std_over_window(values, window):
    return values.rolling(window).std()


def calculate_bb_value(values, window):
    # Return Bollinger Value
    BB = (values - simple_moving_average_over_window(values, window)) / (
            2 * simple_moving_std_over_window(values, window))
    return BB


# Indicator - Bollinger bands
def calculate_bollinger_bands(rm, rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def calculate_momentum_over_window(values, window):
    # Return Momentum Value
    return (values / values.shift(window)) - 1


def main():
    # Define input parameters
    start_date = '2008-1-1'
    end_date = '2009-12-31'
    dates = pd.date_range(start_date, end_date)
    symbols = 'JPM'
    window = 30  # rolling window of 30 Days

    df = get_data([symbols], dates, False)
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    df = df / df.ix[0,]
    df.sort_index(axis=0)

    simple_moving_average = simple_moving_average_over_window(df[symbols], window)
    simple_moving_std = simple_moving_std_over_window(df[symbols], window)

    upper_bb, lower_bb = calculate_bollinger_bands(simple_moving_average, simple_moving_std)
    bb_value = calculate_bb_value(df[symbols], window)
    momentum = calculate_momentum_over_window(df[symbols], window)

    plt.close('all')
    chart_1 = df.join(simple_moving_average, lsuffix='_Normalized Price', rsuffix='_SMA')

    chart_1.columns = ['Normalized Price', "Simple Moving Average"]
    chart_1_axes = chart_1.plot(title="Normalized Price & Simple Moving Average", fontsize=12, lw=0.7)
    chart_1_axes.set_xlabel("Date")
    chart_1_axes.set_ylabel("Normalized Price")

    plt.savefig("Normalized Price & Simple Moving Average")

    plt.close('all')
    chart_2 = df.join(simple_moving_average, lsuffix='_Normalized Price', rsuffix='_SMA') \
        .join(upper_bb, lsuffix='_', rsuffix='_upperband') \
        .join(lower_bb, lsuffix='_', rsuffix='_lowerband')

    chart_2.columns = ['Normalized Price', 'Simple Moving Average', 'Upper Band', 'Lower Band']
    chart_2_axes = chart_2.plot(title="Normalized Price & Bollinger bands", fontsize=12, lw=0.7)
    chart_2_axes.set_xlabel("Date")
    chart_2_axes.set_ylabel("Normalized Price")

    plt.savefig("Normalized Price & Bollinger bands")

    plt.close('all')

    chart_3 = df.join(momentum, lsuffix='_Normalized Price', rsuffix='_Momentum')
    chart_3.columns = ['Normalized Price', 'Momentum']
    chart_3_axes = chart_3.plot(title="Normalized Price & Momentum", fontsize=12, lw=0.7)
    chart_3_axes.set_xlabel("Date")
    chart_3_axes.set_ylabel("Normalized Price")

    plt.savefig("Normalized Price & Momentum")
    print("Graphs created : Normalized Price & Bollinger bands.png , Normalized Price & Momentum.png, Normalized Price & Simple Moving Average.png")


if __name__ == "__main__":
    main()
