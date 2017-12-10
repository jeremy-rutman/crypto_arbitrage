__author__ = 'jeremy'

import krakenex
from pykrakenapi import KrakenAPI
#pip install pykrakenapi
from bitflyer import public
#pip install bitflyer

import time
import ast
import sys
import os

# import urllib.request
# from urllib.request import Request, urlopen
#from urllib.request import  urlopen
#import urllib2

import pandas
from random import choice

# import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


url='https://www.bit2c.co.il/'

import numpy as np

import requests, json

def bitflyer_ticker():
    ticker = public.Public().getticker()
    #returns eg
#    {'volume': 216014.77565499, 'product_code': 'BTC_JPY', 'tick_id': 1730512, 'ltp': 1724530.0,
#     'timestamp': '2017-12-10T22:39:02.24', 'best_bid': 1723374.0, 'best_ask_size': 16.690179,
#     'total_ask_depth': 2087.30139103, 'volume_by_product': 39867.96588841, 'best_bid_size': 0.40004,
#     'total_bid_depth': 4277.58274837, 'best_ask': 1724530.0}

    print(ticker)
    retval={}
    retval['lastprice']=ticker['ltp']
    retval['bid']=ticker['best_bid']
    retval['bidsize']=ticker['best_bid_size']
    retval['ask']=ticker['best_ask']
    retval['asksize']=ticker['best_ask_size']
    retval['bid_depth']=ticker['total_bid_depth']
    retval['ask_depth']=ticker['total_ask_depth']
#    s=pandas.Series(data=retval,index=index)
    index=['lastprice']
    df=pandas.DataFrame(data=retval,columns=['lastprice'],index=index)
    return df


def bit2c_ticker(url_ticker='https://www.bit2c.co.il/Exchanges/BtcNis/Ticker.json'):
    data = safe_get(url_ticker)
    print('url {} text {}'.format(data.url,data.text))
    print('data for rget:{}'.format(data))
    tick=ast.literal_eval(data.text)
#    t=json.dumps(data.text)
 #   print(tick)
    print('last {} highest buy order {} lowest sell {} vol24h {} av24h {}'.format(tick['ll'],tick['h'],tick['l'],tick['a'],tick['av']))

    url_ticker='https://www.bit2c.co.il/Exchanges/BtcNis/orderbook.json'
    data = safe_get(url_ticker)
    if data is None:
        return None,None,None
#    print('url {} text {}'.format(data.url,data.text))
#    print('data for rget:{}'.format(data))
    book=ast.literal_eval(data.text)
#    t=json.dumps(data.text)
#    print(book)
  #  print('last {} highest buy order {} lowest sell {} vol24h {} av24h {}'.format(t['ll'],t['h'],t['l'],t['a'],t['av']))
    #pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])

    retval={}
    retval['bids']=book['bids']
    retval['asks']=book['asks']
    retval['ticker']=tick
    print('bids {}'.format(book['bids']))
    df1=pandas.DataFrame(data=book['bids'],columns=['ils_btc','vol','time'])
    df2=pandas.DataFrame(data=book['asks'],columns=['ils_btc','vol','time'])
    tickdata=[[tick['ll'],tick['h'],tick['l']]]
    print('tickdata {}'.format(tickdata))
    df3=pandas.DataFrame(data=tickdata,columns=['last','highbuy','lowsell'])
    return(df1,df2,df3)

def kraken_ticker():
    api = krakenex.API()
    k = KrakenAPI(api)

#   pair="BCHUSD"
    pair='XXBTZEUR'
    ohlc, last = k.get_ohlc_data(pair=pair)
 #   print(ohlc)
 #   print(last)
    latest_row=ohlc.iloc[0,:]
    print('ticker {}'.format(latest_row))
    # p=k.get_tradable_asset_pairs( info=None, pair=None)
    # print(p)

    # p=k.get_asset_info(asset="BTC")
    # print(p)
    tick=k.get_ticker_information(pair=pair)
    #ticker info:
        # <pair_name> = pair name
    # a = ask array(<price>, <whole lot volume>, <lot volume>),
    # b = bid array(<price>, <whole lot volume>, <lot volume>),
    # c = last trade closed array(<price>, <lot volume>),
    # v = volume array(<today>, <last 24 hours>),
    # p = volume weighted average price array(<today>, <last 24 hours>),
    # t = number of trades array(<today>, <last 24 hours>),
    # l = low array(<today>, <last 24 hours>),
    # h = high array(<today>, <last 24 hours>),
    # o = today's opening price
#    print('ticker {}'.format(tick))

  #  help(KrakenAPI)
    book=k.get_order_book( pair=pair, count=100)
    print('book {}'.format(book))
    spread=k.get_recent_spread_data( pair=pair, since=None)
 #   print('spread {}'.format(spread))
    # p=k.get_recent_trades( pair=pair, since=None)
    # print(p)
    # k.get_open_orders()
    # k.get_open_positions()
    retval={}
    retval['book']=book
    retval['spread']=spread

#    retval['asks']=book['asks']
    retval['ticker']=tick
    return(book,spread,tick)

def safe_get(url,max_attempts=5):
    n_attempts=0
    while(n_attempts<max_attempts):
        try:
            data = requests.get(url)
            return data
        except:
            print('exception '+str(sys.exc_info()))
            n_attempts+=1
            time.sleep(5)
    return None


def currency_conversion():
    key='831d719df8441bcec7e2c4456f8f22ab'
    url='http://www.apilayer.net/api/live?access_key=831d719df8441bcec7e2c4456f8f22ab&format=1'
    success=False
    n_attempts=0
    data=safe_get(url)
    if data is None:
        return None
 #   print('url {} text {}'.format(data.url,data.text))
#    print('data for rget:{}'.format(data))
#    dict=ast.literal_eval(data.text)
    dict=data.text
    dict=json.loads(data.text)
    print('url {} text {}'.format(data.url,dict))
    usd_ils=dict['quotes']['USDILS']
    usd_eur=dict['quotes']['USDEUR']
    usd_btc=dict['quotes']['USDBTC']
    usd_jpy=dict['quotes']['USDJPY']
    listdata=[[usd_ils,usd_eur,usd_btc,usd_jpy]]
    print('listdata {}'.format(listdata))
    df=pandas.DataFrame(data=listdata,columns=['USDILS','USDEUR','USDBTC','USDJPY'])
    return(df)


if __name__=="__main__":
    while(1):
        fname='btc_data_'+str(int(time.time()))+'.xlsx'
        fname=os.path.join(os.getcwd(),fname)
        print('cwd:'+str(os.getcwd())+' fname '+str(fname))
        writer = pandas.ExcelWriter(fname, engine='xlsxwriter')

        # get bitflyer ticker
        bitflyer_ticker_df = bitflyer_ticker()

        #get eur-ils conversion (thru usd ,, didnt find straight conversion)
        convert=currency_conversion()

        #get bit2c bid/ask tables and ticker
        b2c_bid,b2c_ask,b2c_tick=bit2c_ticker()
      #  print('b2cbid:{}'.format(b2c_bid))
        print()
        kraken_book,kraken_spread,kraken_tick=kraken_ticker()
     #   print('krakenbook:{}]'.format(kraken_book))
        print('krakenbtick:{}]'.format(kraken_tick))


#        alldata={'ilsbtc@bt2c':bit2c_data,'eurbtc@kraken':kraken_data}

        # Write each dataframe to a different worksheet.
        sleeptime=5*60
        try:
            b2c_bid.to_excel(writer, sheet_name='b2cbid')
            b2c_ask.to_excel(writer, sheet_name='b2cask')
            b2c_tick.to_excel(writer, sheet_name='b2ctick')
            convert.to_excel(writer, sheet_name='conversions')
    #        print(np.ndim(kraken_spread))
     #       print(np.ndim(kraken_tick))
            # print(np.ndim(kraken_book))
            # kraken_spread.to_excel(writer, sheet_name='kraken_spread')
            kraken_tick.to_excel(writer, sheet_name='kraken_tick')
            # kraken_book.to_excel(writer, sheet_name='kraken_book')
            # help(KrakenAPI)

            bitflyer_ticker_df.to_excel(writer, sheet_name='bitflyer_tick')

            writer.save()
        except:
            print('some problem writing')
            print(sys.exc_info())
            sleeptime=30
        # with(open(fname,mode='a')) as fp:
        #     json.dump(alldata,fp,indent=4)
        #     fp.close()
        print('wrote {}'.format(fname))
        time.sleep(sleeptime)
