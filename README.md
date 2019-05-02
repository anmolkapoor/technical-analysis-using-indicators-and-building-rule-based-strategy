# Technical Analysis with Indicators and building a ML based trading strategy (Part 1 of 2)
Technical indicators are heuristic or mathematical calculations based on the price, volume, or open interest of a security or contract used by traders who follow technical analysis. By analysing historical data, technical analysts use indicators to predict future price movements. Using these predictions, analysts create strategies that they would apply to trade a security in order to make profit.

In this post, we will be discussing:
* Three examples of Technical indicators, namely Simple moving average, Momentum and Bollinger Bands®.
* Strategy and how to view them as trade orders.
* Create a Theoretically optimal strategy if we can see future stock prices.
* Create a Manual Strategy based on indicators.
* Compare and  analysis of two strategies.
  

>Since the above indicators are based on rolling window, we have taken 30 Days as the rolling window size.

  

### Simple Moving average

SMA is the moving average calculated by sum of adjusted closing price of a stock over the window and diving over size of the window.

>SMA[t] = price[t − N: t] . mean()


SMA can be used as a proxy the true value of the company stock. For large deviations from the price, we can expect the price to come back to the SMA over a period of time. This can create a BUY and SELL opportunity when optimised over a threshold.

[![SMA Chart](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Simple%20Moving%20Average.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Simple%20Moving%20Average.png)


### Momentum

Momentum refers to the rate of change in the adjusted close price of the s. It can be calculated :

>Momentum[t] = (price[t] / price[t − N])-1


The value of momentum can be used an indicator, and can be used as a intuition that future price may follow the inertia. That means that if a stock price is going up with a high momentum, we can use this as a signal for BUY opportunity as it can go up further in future.

[![Momentum Chart](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Momentum.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Momentum.png)

### Bollinger Bands®

Bollinger Bands (developed by John Bollinger) is the plot of two bands two sigma away from the simple moving average. They can be calculated as:

  
>upper_band = sma + standard_deviation * 2

>lower_band = sma - standard_deviation * 2


If we plot the Bollinger Bands with the price for a time period:

[![BB Chart](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Bollinger%20bands.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/Normalized%20Price%20%26%20Bollinger%20bands.png)

We can find trading opportunity as SELL where price is entering the upper band from outside the upper band, and BUY where price is lower than the lower band and moving towards the SMA from outside. This movement inlines with our indication that price will oscillate from SMA, but will come back to SMA and can be used as trading opportunities.

# Strategy and Trade orders
For our discussion, let us assume we are trading a stock in market over a period of time. Trading of a stock, in its simplistic form means we can either sell, buy or hold our stocks in portfolio. These commands issued are orders that let us trade the stock over the exchange. Thus, these trade orders can be of type:
* SHORT  or SELL . eg: SHORT JPM 1000
* LONG or BUY. eg; LONG JPM 1000
* HOLD. which is holding the stocks in our portfolio.

For simplicity of discussion, lets assume, we can only issue these three commands SHORT, LONG and HOLD for our stock JPM, and our portfolio can either be in these three states at a given time:
* +1000 ( We have 1000 JPM stocks in portfolio)
* 0 ( We have no JPM stocks in portfolio)
* -1000 (We have short 1000 JPM stocks and attributed them in our portfolio)
  

# Theoretically Optimal Strategy

Lets assume we can foresee the future price and our tasks is create a strategy that can make profit. A simple strategy is to sell as much as there is possibility in the portfolio ( SHORT till portfolio reaches -1000) and if price is going up in future buy as much as there is possibility in the portfolio( LONG till portfolio reaches +1000)

Pseudo code:

```

Is_price_going_up = price[today+1] - price[today]

if is_price_going_up:
    do_buy_trade
else:
    do_sell_trade

```

Results:

>Date Range: 2008-01-01 to 2009-12-31
  

||Theoretical Strategy|Benchmark|
|---|----|---|
|Cumulative return|5.7861|0.0123|
|Stdev of daily returns|0.00454782319791|0.0170043662712|
|Average of daily returns|0.00381678615086|0.000168086978191|
|Final Portfolio Value|678610.0|101230.0|
  
  

[![Theoritical Chart](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/TheoreticallyOptimalStrategy.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/TheoreticallyOptimalStrategy.png)

  

### Manual Rule-Based Trader

Now consider we did not have power to see the future value of stock (that will be the case always), can we create a strategy that will use the three indicators described to predict the future. Let's call it ManualStrategy which will be based on some rules over our indicators. We have applied the following strategy using 3 indicators : Bollinger Bands, Momentum and Volatility using Price Vs SMA.

Strategy:

````

If price_yesterday was above upper_band_yesterday and price_today is below upper_band_today:
    do_sell_trade
Else if price_yesterday was below lower_band_yesterday and price_today is above lower_band_today:
    do_buy_trade
Else if price_today > sma_today and difference(price_today, sma_today)> threshold:
    do_sell_trade
Else if price_today<sma_today and difference(sma_today,price_today) > threshold:
    do_buy_trade
Else if momentum_today > threshold_positive
    do_buy_trade
Else if momentum_today<theshold_negative
    do_sell_trade
Else No_trade

````

Results:

  

>Date Range: 2008-01-01 to 2009-12-31

  
  

||Manual Strategy|Benchmark|
|---|---|---|
|Cumulative return|0.358969602112|0.0123|\
|Stdev of daily returns|0.0129419160091|0.0170043662712|
|Average of daily returns|0.000692144738531|0.000168086978191
|Final Portfolio Value|135884.05|101230.0

[![ManualStrategy](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/ManualStrategy-Train.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/ManualStrategy-Train.png)

# Comparative Analysis

Here are the statistics comparing in-sample data:

>Date: 2008-01-01 to 2009-12-31
  
||Manual Strategy|Benchmark|
|---|---|---|
|Cumulative return|0.358969602112|0.0123|
|Stdev of daily returns|0.0129419160091|0.0170043662712|
|Average of daily returns|0.000692144738531|0.000168086978191
|Final Portfolio Value|135884.05|101230.0

For out-sample:

>Date: 2010-01-01 2011-12-31

||Manual Strategy|Benchmark
|---|---|---|
|Cumulative return|0.0111025547427|-0.0834
|Stdev of daily returns|0.00832245137396|0.0084810074988
|Average of daily returns|5.6467518872e-05|-0.000137203160195\
|Final Portfolio Value|101100.65|91660.0

#### Why there is a difference in performance:

The manual strategy works well for the train period as we were able to tweak the different thresholds like window size, buy and selling threshold for momentum and volatility. The tweaked parameters did not work very well. Our bets on a large window size was not correct and even though the price went up, the huge lag in reflection on SMA and Momentum, was not able to give correct BUY and SELL opportunity on time.

[![ManualStrategy-test](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/ManualStrategy-Test.png)](https://github.com/anmolkapoor/technical-analysis-using-indicators-and-building-rule-based-strategy/raw/master/images/ManualStrategy-Test.png)

##### Now that we have found that our rule based strategy was not very optimum, can we apply machine learning to learn optimal rules and achieve better results.
 [Read the next part of the series to create a machine learning based strategy over technical indicators and its comparative analysis over the rule based strategy]({{ site.baseurl }}{% post_url 2019-05-02-Technical-Analysis-With-Indicators-And-Building-ML-Based-Trading-Strategy-Part-2 %}).


