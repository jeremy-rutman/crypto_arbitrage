__author__ = 'jeremy'

"""
method1 - crpto->fiat 
method2 - crypto1->crypto2
method3 -  a vs b simultaneous , working on delta(delta) , no sending 
"""

import krakenex
from pykrakenapi import KrakenAPI
#pip3 install pykrakenapi
from bitflyer import public
#pip3 install bitflyer

import time
import ast
import sys
import os
import pandas
import requests, json

from multiprocessing import Pool

import numpy as np
from random import choice

# import urllib.request
# from urllib.request import Request, urlopen
#from urllib.request import  urlopen
#import urllib2
# import requests
#selenium is a web browser spawnable from python
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def bitflyer_ticker_multi(pairs=['BTC_JPY','ETC_BTC','BCH_BTC']):
    all_results = []
    p=Pool(len(pairs))
    all_results = p.map(bitflyer_ticker,pairs)
    return all_results
    # for pair in pairs:
    #     all_results.append(pair)


def bitflyer_ticker(pair='BTC_JPY'):
#BTC_JPY,ETH_BTC,BCH_BTC

#for list of markets:
#    https: // api.bitflyer.jp / v1 / getmarkets
    ticker = public.Public().getticker()
    #returns eg
#    {'volume': 216014.77565499, 'product_code': 'BTC_JPY', 'tick_id': 1730512, 'ltp': 1724530.0,
#     'timestamp': '2017-12-10T22:39:02.24', 'best_bid': 1723374.0, 'best_ask_size': 16.690179,
#     'total_ask_depth': 2087.30139103, 'volume_by_product': 39867.96588841, 'best_bid_size': 0.40004,
#     'total_bid_depth': 4277.58274837, 'best_ask': 1724530.0}

    api_url = 'https://api.bitflyer.jp/v1/ticker?product_code='+pair
#    print(ticker)
    product = ticker['product_code']

    all_vals=[]
    retval={}
    retval['pair']=product
    retval['lastprice']=ticker['ltp']
    retval['bid']=ticker['best_bid']
    retval['bid_volume']=ticker['best_bid_size']
    retval['ask']=ticker['best_ask']
    retval['ask_volume']=ticker['best_ask_size']
    # retval['bid_depth']=ticker['total_bid_depth']
    # retval['ask_depth']=ticker['total_ask_depth']
    retval['exchange'] = 'bitflyer'
    retval['timestamp'] = ticker['timestamp']

    #    s=pandas.Series(data=retval,index=index)
    # row=[retval['bid'],retval['bidsize'],retval['bid_depth'],retval['ask'],retval['asksize'],retval['ask_depth'],retval['lastprice']]
    # df=pandas.DataFrame(data=[row],columns=['bid','bidsize','bid_depth','ask','asksize','ask_depth','lastprice'])
#    all_vals.append(retval)
    return(retval)


def bit2c_ticker_multi(pairs=['ILS_BTC','ILS_LTC']):
    all_retvals=[]
    p=Pool(len(pairs))
    all_results = p.map(bit2c_ticker,pairs)
    return all_results

    # for pair in pairs:
    #     retval = bit2c_ticker(pair)
    #     all_retvals.append(retval)

def bit2c_ticker(pair='ILS_BTC'):
    if pair=='ILS_BTC':
        #url_ticker = 'https://www.bit2c.co.il/Exchanges/BtcNis/Ticker.json'
        url_orderbook = 'https://www.bit2c.co.il/Exchanges/BtcNis/orderbook.json'
        coin1 = 'ILS'
        coin2 = 'BTC'
    elif pair=='ILS_LTC':
        url_orderbook = 'https://www.bit2c.co.il/Exchanges/LtcNis/orderbook.json'
        coin1 = 'ILS'
        coin2 = 'LTC'
    else:
        print('no pair chosen ')
        return None
    #     print('url {} text {}'.format(data.url,data.text))
#     print('data for rget:{}'.format(data))
#     tick=ast.literal_eval(data.text)
#     print('last {} highest buy order {} lowest sell {} vol24h {} av24h {}'.format(tick['ll'],tick['h'],tick['l'],tick['a'],tick['av']))
#     url_ticker='https://www.bit2c.co.il/Exchanges/BtcNis/orderbook.json'
    data = safe_get(url_orderbook)
    if data is None:
        return None
    book=ast.literal_eval(data.text)
#    t=json.dumps(data.text)
    # df3=pandas.DataFrame(data=tickdata,columns=['last','highbuy','lowsell'])
    bidname='bid_'+coin1+'_'+coin2
    askname='ask_'+coin1+'_'+coin2
    all_vals=[]
    retval = {}
    retval['pair'] = pair
    retval['bid']=book['bids'][0][0]
    retval['bid_volume']=book['bids'][0][1]
    retval['ask']=book['asks'][0][0]
    retval['ask_volume'] = book['bids'][0][1]
    retval['exchange'] = 'bit2c'
    retval['timestamp'] = round(time.time(),1)
    return(retval)
#
def kraken_ticker_multi(pairs=['EUR_BTC','EUR_LTC','USD_BCH']):
    api = krakenex.API()
    k = KrakenAPI(api)

    normal_to_kraken_names={'EUR_BTC':'XXBTZEUR','EUR_LTC':'XLTCZEUR','USD_BCH':'BCHUSD'}
    kraken_to_normal_names={v:k for k,v in normal_to_kraken_names.items()}
 #
 #    ohlc, last = k.get_ohlc_data(pair=pair)
 # #   print(ohlc)
 # #   print(last)
 #    latest_row=ohlc.iloc[0,:]
 #    print('ticker latest row{}'.format(latest_row))
 #    # p=k.get_tradable_asset_pairs( info=None, pair=None)
 #    # print(p)
 #    # p=k.get_asset_info(asset="BTC")
    # print(p)
#    pairs = ['XXBTZEUR',"BCHUSD","XLTCZEUR"]
    # tick=k.get_ticker_information(pair=pairs)
    # print('kraken ticker info {}'.format(tick))

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
  #   book=k.get_order_book( pair=pair, count=100)
  #   spread=k.get_recent_spread_data( pair=pair, since=None)
    # p=k.get_recent_trades( pair=pair, since=None)
    # k.get_open_orders()
    # k.get_open_positions()

    #get multiple pairs in one shot
    all_vals=[]
    api_url = 'https://api.kraken.com/0/public/Ticker?pair='
    for pair in pairs:
        api_url+=normal_to_kraken_names[pair]+','
    api_url=api_url[:-1]
#    print(api_url)
    data = safe_get(api_url)
    if data is None:
        return None
    book=ast.literal_eval(data.text)
    if 'error' in book:
        if book['error'] != []:
            print('error in kraken:{}'.format(book['error']))
#    print('and the boook {} '.format(book))
    for k,v in book['result'].items():
 #       print(k,v)
        pair=kraken_to_normal_names[k]
        coin1,coin2=pair.split('_')
#        print('pair {} coin1 {} coin2 {}'.format(pair,coin1,coin2))

        retval={}
        retval['pair']=pair
        retval['lastprice']=v['c'][0]
        retval['bid']=v['b'][0]
        retval['bid_volume']=v['b'][2]
        retval['ask']=v['a'][0]
        retval['ask_volume']=v['a'][2]
        retval['exchange'] = 'kraken'
        retval['timestamp'] = round(time.time(),1)

        all_vals.append(retval)
    return all_vals

#    retval['asks']=book['asks']
#    retval['ticker']=tick



#    return(book,spread,tick)

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


def get_api_infos():
    pass

def currency_conversions():
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

    retval = {}
    retval['exchange']='currencies'
    retval['ILS_USD']=usd_ils
    retval['EUR_USD']=usd_eur
    retval['JPY_USD']=usd_jpy
    return retval

    # listdata=[[usd_ils,usd_eur,usd_btc,usd_jpy]]
    # print('listdata {}'.format(listdata))
    # df=pandas.DataFrame(data=listdata,columns=['USDILS','USDEUR','USDBTC','USDJPY'])
    # return(df)
#
#
def func_wrap(func):
    return func

def get_all_apis(func_list=[kraken_ticker_multi(),bit2c_ticker_multi(),bitflyer_ticker_multi()]):
    p=Pool(len(func_list))
    all_results = p.map(func_wrap,func_list)
    flat_list = [element for sublist in all_results for element in sublist]
    return flat_list

def convert(prices,currency_convert):
    for tick in prices:
        print('tick:{}'.format(tick))
        coin1,coin2 = tick['pair'].split('_')
        print('usdjpy {} eurusd{} jpyeur {}'.format(currency_convert['JPY_USD'], currency_convert['EUR_USD'], jpy_eur))
        jpy_eur = currency_convert['JPY_USD'] / currency_convert['EUR_USD']
        if coin1 == 'JPY': #       ,'USD','ILS']:
      #      tick['ask_usd']=tick['ask'] / currency_convert['USD_JPY']
            tick['ask_eur']=tick['ask'] / jpy_eur
            tick['ask_eur'] = tick['ask'] / jpy_eur

        elif coin1 == 'JPY': #       ,'USD','ILS']:
            tick['ask_usd']=tick['ask'] / currency_convert['USD_JPY']
            tick['ask_eur']=tick['ask_usd'] / currency_convert['USD_EUR']

if __name__=="__main__":

    api_prices=get_all_apis()
    print(json.dumps(api_prices,indent=2))
    currency_convert = currency_conversions()
    convert(api_prices,currency_convert)

    # d=kraken_ticker_multi()
    # print('kraken {}'.format(json.dumps(d,indent=2)))
    # d=bit2c_ticker_multi()
    # print('bit2c {}'.format(json.dumps(d,indent=2)))
    # d=bitflyer_ticker_multi()
    # print('bitflyer {}'.format(json.dumps(d,indent=2)))


    while(0):
        fname='btc_data_'+str(int(time.time()))+'.xlsx'
        fname=os.path.join(os.getcwd(),fname)
        print('cwd:'+str(os.getcwd())+' fname '+str(fname))
        writer = pandas.ExcelWriter(fname, engine='xlsxwriter')

        # get bitflyer ticker
        bitflyer_ticker_df = bitflyer_ticker()

        #get eur-ils conversion (thru usd ,, didnt find straight conversion)
        convert=currency_conversions()

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
