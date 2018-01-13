__author__ = 'jeremy'

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


def bitflyer_ticker(pair='BTC_JPY'):
    ticker = public.Public().getticker()
    #returns eg
#    {'volume': 216014.77565499, 'product_code': 'BTC_JPY', 'tick_id': 1730512, 'ltp': 1724530.0,
#     'timestamp': '2017-12-10T22:39:02.24', 'best_bid': 1723374.0, 'best_ask_size': 16.690179,
#     'total_ask_depth': 2087.30139103, 'volume_by_product': 39867.96588841, 'best_bid_size': 0.40004,
#     'total_bid_depth': 4277.58274837, 'best_ask': 1724530.0}
    print(ticker)
    product = ticker['product_code']
    if product=='BTC_JPY':
        coin2 = 'BTC'
        coin1 = 'JPY'
    elif product == 'LTC_JPY':  # todo see how to get ltc/etc from bitflyer
        coin2 = 'LTC'
        coin1 = 'JPY'
    bidname='bid_'+coin1+'_'+coin2
    askname='ask_'+coin1+'_'+coin2

    all_vals=[]
    retval={}
    retval['lastprice']=ticker['ltp']
    retval[bidname]=ticker['best_bid']
    retval['bid_volume']=ticker['best_bid_size']
    retval[askname]=ticker['best_ask']
    retval['ask_volume']=ticker['best_ask_size']
    retval['bid_depth']=ticker['total_bid_depth']
    retval['ask_depth']=ticker['total_ask_depth']
    retval['exchange'] = 'bitflyer'
    retval['timestamp'] = ticker('timestamp')

    #    s=pandas.Series(data=retval,index=index)
    # row=[retval['bid'],retval['bidsize'],retval['bid_depth'],retval['ask'],retval['asksize'],retval['ask_depth'],retval['lastprice']]
    # df=pandas.DataFrame(data=[row],columns=['bid','bidsize','bid_depth','ask','asksize','ask_depth','lastprice'])
    all_vals.append(retval)
    return(all_vals)


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
    retval[bidname]=book['bids'][0][0]
    retval['bid_volume']=book['bids'][0][1]
    retval[askname]=book['asks'][0][0]
    retval['ask_volume'] = book['bids'][0][1]
    retval['exchange'] = 'bit2c'
    retval['timestamp'] = round(time.time(),1)
    all_vals.append(retval)
    return(all_vals)
#
def kraken_ticker(pair='BTC_EUR'):
    api = krakenex.API()
    k = KrakenAPI(api)

    if pair=='BTC_EUR':
        pair='XXBTZEUR'
        coin1='BTC'
        coin2='EUR'
    elif pair == 'BCH_USD':
        pair="BCHUSD"
        coin1 = 'BCH'
        coin2 = 'USD'

    elif pair == 'LTC_EUR':
        pair="XLTCZEUR"
        coin1 = 'LTC'
        coin2 = 'EUR'

    else:
        print('didnt understand coin pair {}'.format(pair))
        return None
 #
 #    ohlc, last = k.get_ohlc_data(pair=pair)
 # #   print(ohlc)
 # #   print(last)
 #    latest_row=ohlc.iloc[0,:]
 #    print('ticker latest row{}'.format(latest_row))
 #    # p=k.get_tradable_asset_pairs( info=None, pair=None)
 #    # print(p)
 #
 #    # p=k.get_asset_info(asset="BTC")
    # print(p)
    pairs = ['XXBTZEUR',"BCHUSD","XLTCZEUR"]
    tick=k.get_ticker_information(pair=pairs)
    print('kraken ticker info {}'.format(tick))


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
  #   print('book {}'.format(book))
  #   spread=k.get_recent_spread_data( pair=pair, since=None)
 #   print('spread {}'.format(spread))
    # p=k.get_recent_trades( pair=pair, since=None)
    # print(p)
    # k.get_open_orders()
    # k.get_open_positions()
    all_vals=[]
    retval={}
#    retval['book']=book
#    retval['spread']=spread

    api_url = 'https://api.kraken.com/0/public/Ticker?pair=XXBTZEUR'
    data = safe_get(api_url)
    if data is None:
        return None
    book=ast.literal_eval(data.text)
    print('and the boook {} '.format(book))


    bidname = 'bid_' + coin1 + '_' + coin2
    askname = 'ask_' + coin1 + '_' + coin2

    retval['lastprice']=tick['c'][0]
    retval[bidname]=tick['b'][0][0]
    retval['bid_volume']=tick['b'][0][2]
    retval[askname]=tick['a'][0][0]
    retval['ask_volume']=tick['a'][0][2]
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
  #  print('url {} text {}'.format(data.url,dict))
    usd_ils=dict['quotes']['USDILS']
    usd_eur=dict['quotes']['USDEUR']
    usd_btc=dict['quotes']['USDBTC']
    usd_jpy=dict['quotes']['USDJPY']
    listdata=[[usd_ils,usd_eur,usd_btc,usd_jpy]]
    print('listdata {}'.format(listdata))
    df=pandas.DataFrame(data=listdata,columns=['USDILS','USDEUR','USDBTC','USDJPY'])
    return(df)
#
#
if __name__=="__main__":
    d=kraken_ticker()
    print('kraken {}'.format(d))
    d=bit2c_ticker()
    print('bit2c {}'.format(d))
    d=bitflyer_ticker()
    print('bitflyer {}'.format(d))
    while(0):
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
