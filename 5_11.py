import cryptocompare as cc
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


if __name__ == "__main__":


    # --------------------------------Bitcoin 2020--------------------------------------

    a = cc.get_historical_price_day('BTC', 'EUR',
    limit=365, exchange='CCCAGG', toTs=datetime.datetime(2021,1,1))

    """
    The function cryptocompare.get_historical_price_day(), depending on the parameter limit, returns 
    a list of 'limit+1' dictionaries. 
    
    Each dictionary contains 9 key-value pairs
    'time', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'close', 'conversionType', 'conversionSymbol'
    
    :parameter limit: (number of instances+1) that you want to return before the 'toTs' date.
            **for example, if you select limit=1, and toTs=datetime.datetime(2019,6,6), the function will return
            the values of the coin the dates (2019,6,4) and (2019,6,5).
            
    Exercise 5.11 requested a graph of all the values of BitCoin ('BTC'), during 2020. The year 2020 was a leap year,
    meaning that it had 366 days. Therefore, the limit selected was 365.
    
    To plot the graph in matplotlib, I used for Bitcoin the 'high','low' and 'close' values for each of the 366 days.
    """

    btc_high = []
    btc_low = []
    btc_close = []
    days = [i for i in range(366)]

    for i in range(len(a)):
        btc_high.append(a[i].get('high'))
        btc_low.append(a[i].get('low'))
        btc_close.append(a[i].get('close'))

    plt.plot(days, btc_high, color='green', label = "high")
    plt.plot(days, btc_low, color='red', label = "low")
    plt.plot(days, btc_close, color='orange', label = "close_value")

    plt.xlabel('days of 2020')
    plt.ylabel('Bitcoin price in EUR')
    plt.title('Bitcoin price in EUR from 1/1/2020- 31/12/2020')
    plt.legend()
    #plt.show()


    #--------------------------------Ethereum 2020-----------------------------

    b = cc.get_historical_price_day('ETH', 'EUR',
    limit=365, exchange='CCCAGG', toTs=datetime.datetime(2021, 1, 1))

    coin_list = cc.get_coin_list()
    coins = sorted(list(coin_list.keys()))

    """
    For the second part of the exercise, I repeated the process using np arrays instead of lists, and also
    the Cryptocurrency used in this case was Ethereum ('ETH').
    Prices refer to the period between 1/1/2020 - 31/12/2020.
    
    """
    eth_days = np.arange(366)
    eth_high = np.zeros(366)
    eth_low = np.zeros(366)
    eth_close = np.zeros(366)

    for i in range(len(b)):
        eth_high[i] = b[i].get('high')
        eth_low[i] = b[i].get('low')
        eth_close[i] = b[i].get('close')

    plt.plot(eth_days, eth_high, color='green', label="high")
    plt.plot(eth_days, eth_low, color='red', label="low")
    plt.plot(eth_days, eth_close, color='orange', label="close_value")

    plt.xlabel('days of 2020')
    plt.ylabel('Ethereum price in EUR')
    plt.title('Ethereum price in EUR from 1/1/2020- 31/12/2020')
    plt.legend()
    plt.show()



