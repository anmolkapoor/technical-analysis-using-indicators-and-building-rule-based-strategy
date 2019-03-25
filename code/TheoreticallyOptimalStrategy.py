#
# Provide a chart that reports:
#
# Benchmark (see definition above) normalized to 1.0 at the start: Green line
# Value of the theoretically optimal portfolio (normalized to 1.0 at the start): Red line
# You should also report in text:
#
# Cumulative return of the benchmark and portfolio
# Stdev of daily returns of benchmark and portfolio
# Mean of daily returns of benchmark and portfolio
#

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt

from util import get_data, plot_data


def compute_portfolio_stats(port_val):
    daily_ret = (port_val / port_val.shift(1)) - 1
    cummulative_returns = (port_val[-1] / port_val[0]) - 1
    average_daily_return = daily_ret.mean()
    std_daily_return = daily_ret.std()
    return cummulative_returns, average_daily_return, std_daily_return


def compute_portvals(orders_df, start_val=1000000, commission=9.95, impact=0.005):
    # orders_df = orders_df.sort_index()
    st_v = min(orders_df.index)
    ed_v = max(orders_df.index)
    dr = pd.date_range(st_v, ed_v)
    traded_symbols = ["JPM"]
    traded_symbol_data = get_data(symbols=traded_symbols, dates=dr)
    traded_symbol_data = traded_symbol_data.fillna(method="ffill")
    traded_symbol_data = traded_symbol_data.fillna(method="bfill")

    traded_symbol_data["traded_today"] = pd.Series(0.0, index=traded_symbol_data.index)
    traded_symbol_data["p_value"] = pd.Series(0.0, index=traded_symbol_data.index)
    # traded_symbol_data["t_value"] = pd.Series(0, index=traded_symbol_data.index)
    for symbol_key in traded_symbols:
        traded_symbol_data[symbol_key + "_shares"] = pd.Series(0.0, index=traded_symbol_data.index)

    for trade_date, row in orders_df.iterrows():
        symbol = "JPM"
        shares = row['orders']
        order = "BUY"
        if shares > 0:
            order = "BUY"
        # elif shares < 0:
        #     order = "SELL"
        # elif shares == 0:
        #     continue
        else:
            order = "SELL"
            shares = -1 * shares

        if trade_date not in traded_symbol_data.index:
            continue
        traded_value_on_day = traded_symbol_data.ix[trade_date, "traded_today"]
        symbol_rate_on_day = traded_symbol_data.ix[trade_date, symbol]

        if order == "BUY":
            multiplier = -1
        else:
            multiplier = 1

        trade = multiplier * symbol_rate_on_day * shares
        extras = symbol_rate_on_day * shares * impact + commission
        traded_value_on_day = traded_value_on_day + trade - extras
        traded_symbol_data.ix[trade_date, "traded_today"] = traded_value_on_day
        already_shares = traded_symbol_data.ix[trade_date, symbol + "_shares"]
        traded_symbol_data.ix[trade_date, symbol + "_shares"] = already_shares + (multiplier * (-1) * shares)

    for i in range(1, traded_symbol_data.shape[0]):
        for symbol_key in traded_symbols:
            traded_symbol_data.ix[i, symbol_key + "_shares"] = traded_symbol_data.ix[i, symbol_key + "_shares"] + \
                                                               traded_symbol_data.ix[i - 1, symbol_key + "_shares"]
    current_start_val = start_val
    for date_v, row in traded_symbol_data.iterrows():
        total_share_value = 0
        current_start_val = current_start_val + row["traded_today"]
        for symbol_key in traded_symbols:
            total_share_value = total_share_value + row[symbol_key + "_shares"] * traded_symbol_data.ix[
                date_v, symbol_key]

        traded_symbol_data.ix[date_v, "p_value"] = current_start_val + total_share_value
    return traded_symbol_data['p_value']


class TheoreticallyOptimalStrategy:

    def calculate_price_going_up(self, current, future):
        return current < future

    def do_buy_trade(self, portfolio_position):
        # buy
        if portfolio_position == 0:
            return 1000
        elif portfolio_position == -1000:
            return 2000
        elif portfolio_position == 1000:
            return 0

    def do_sell_trade(self, portfolio_position):
        if portfolio_position == 0:
            return -1000
        elif portfolio_position == -1000:
            return 0
        elif portfolio_position == 1000:
            return -2000

    def testPolicy(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):

        dates = pd.date_range(sd, ed)

        df = get_data([symbol], dates)
        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')
        portfolio_position = 0
        trade_shares = []

        stock_data = df[symbol]
        for i in range(len(df.index) - 1):
            is_price_going_up = self.calculate_price_going_up(stock_data[i], stock_data[i + 1])
            if is_price_going_up:
                trade_shares.append(self.do_buy_trade(portfolio_position))
            else:
                trade_shares.append(self.do_sell_trade(portfolio_position))
            portfolio_position = portfolio_position + trade_shares[i]

        # for last day
        trade_shares.append(0)
        df_trades = pd.DataFrame(data=trade_shares, index=df.index, columns=['orders'])
        return df_trades

    def benchmark(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        dates = pd.date_range(sd, ed)
        df = get_data([symbol], dates)
        trade_shares = [1000, 0]
        trade_date = [df.index[0], df.index[len(df.index) - 1]]
        df_trades = pd.DataFrame(data=trade_shares, index=trade_date, columns=['orders'])
        return df_trades


if __name__ == '__main__':
    start_date = dt.datetime(2008, 01, 01)
    end_date = dt.datetime(2009, 12, 31)

    symbol = 'JPM'

    optimized_strategy = TheoreticallyOptimalStrategy()
    optimized_trades = optimized_strategy.testPolicy(symbol, start_date, end_date, 100000)
    optimized_port_vals = compute_portvals(orders_df=optimized_trades, start_val=100000,
                                           commission=0.00, impact=0.00)

    benchmark_trades = optimized_strategy.benchmark(symbol, start_date, end_date, 100000)
    benchmark_port_vals = compute_portvals(orders_df=benchmark_trades, start_val=100000,
                                           commission=0.00, impact=0.00)

    print "Printing stats"

    opt_cummulative_returns, opt_average_daily_return, opt_std_daily_return = compute_portfolio_stats(
        optimized_port_vals)
    bnch_cummulative_returns, bnch_average_daily_return, bnch_std_daily_return = compute_portfolio_stats(
        benchmark_port_vals)

    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Cumulative Return of Portfolio: {}".format(opt_cummulative_returns)
    print "Standard Deviation of Portfolio: {}".format(opt_std_daily_return)
    print "Average Daily Return of Portfolio: {}".format(opt_average_daily_return)
    print "Final Portfolio Value: {}".format(optimized_port_vals[-1])
    print
    print "Cumulative Return of Benchmark: {}".format(bnch_cummulative_returns)
    print "Standard Deviation of Benchmark: {}".format(bnch_std_daily_return)
    print "Average Daily Return of Benchmark: {}".format(bnch_average_daily_return)
    print "Final Benchmark Value: {}".format(benchmark_port_vals[-1])

    optimized_port_vals_normalized = (optimized_port_vals / optimized_port_vals.ix[0,]).to_frame()
    benchmark_port_vals_normalized = (benchmark_port_vals / benchmark_port_vals.ix[0,]).to_frame()

    chart_1 = benchmark_port_vals_normalized.join(optimized_port_vals_normalized, lsuffix='_benchmark',
                                                  rsuffix='_portfolio')
    chart_1.columns = ['Benchmark', 'TheoreticallyOptimalStrategy']
    chart1_axes = chart_1.plot(title="Benchmark and TheoreticallyOptimalStrategy portfolio (Normalized)", fontsize=12,
                               lw=0.7,
                               color=["green", "red"])

    chart1_axes.set_xlabel("Date")
    chart1_axes.set_ylabel("Portfolio")
    plt.savefig("TheoreticallyOptimalStrategy")
    print(
        "Graphs created : TheoreticallyOptimalStrategy.png")
