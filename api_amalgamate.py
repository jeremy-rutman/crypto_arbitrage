__author__ = 'jeremy'

"""
method1 - crpto->fiat 
method2 - crypto1->crypto2
method3 -  a vs b simultaneous , working on delta(delta) , no sending 
https://cryptowat.ch/docs/api#markets

binance
https://www.binance.com/restapipub.html
# whoever wants to bid ltc for btc
# needs to first  get ltc , by paying the ask of e..g euro-ltc
# so  the bid ltc-btc_bid = euro-btc_bid / euro-ltc_ask

#binance https://github.com/binance-exchange/binance-official-api-docs
"""

# import krakenex
# from pykrakenapi import KrakenAPI
#pip3 install pykrakenapi
#from bitflyer import public
#pip3 install bitflyer

import time
import ast
import sys
import os
#import pandas
import requests, json
from matplotlib import pyplot as plt
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


crypto_list = ['BCH', 'ETH', 'BTC', 'BTG','LTC']
fiat_list = ['USD', 'JPY', 'ILS', 'EUR']


class arbitrageur():
    def __init__(self):
        self.time_of_last_conversion_check=0 #seconds
        self.currency_update_interval = 3600 #seconds
        self.time_of_last_api_check = 0 #seconds
        self.api_update_interval = 10 #seconds
        self.update_info()

    def update_info(self):
        if time.time()-self.time_of_last_conversion_check > self.currency_update_interval:
            self.currency_conversions=get_currency_conversions()
            self.time_of_last_conversion_check = time.time()
        if time.time()-self.time_of_last_api_check > self.api_update_interval:
            self.api_prices = get_all_apis()
            how_many(self.api_prices)
            self.api_prices=generate_extra_pairs(self.api_prices)
            how_many(self.api_prices)

            self.api_prices = convert(self.api_prices,self.currency_conversions)
            how_many(self.api_prices)
            self.time_of_last_api_check = time.time()

        print('currencies last update {} '.format(self.time_of_last_conversion_check))
        print(json.dumps(self.currency_conversions,indent=2))
        print('apis last update {}'.format(self.time_of_last_api_check))
        print(json.dumps(self.api_prices,indent=2))
        chart_all(self.api_prices)
        identify_arbitrages(self.api_prices)
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

def how_many(ticklist_list):
    for ticklist in ticklist_list:
        print('exchange {} has {} prices'.format(ticklist[0]['exchange'],len(ticklist)))

def get_currency_conversions():
    '''
    todo - check this once/hr or dt since they are only updating 1/hr , or use another api
    :return:
    '''
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
    retval['exchange']='currencies_apilayer.net'
    retval['ILS_USD']=usd_ils
    retval['EUR_USD']=usd_eur
    retval['JPY_USD']=usd_jpy
    return retval

    # listdata=[[usd_ils,usd_eur,usd_btc,usd_jpy]]
    # print('listdata {}'.format(listdata))
    # df=pandas.DataFrame(data=listdata,columns=['USDILS','USDEUR','USDBTC','USDJPY'])
    # return(df)
#


def convert(ticklist_list,currency_convert):
    '''
    add euro prices to all fiat currencies that arent already euro
    :param prices:
    :param currency_convert:
    :return:
    '''
    jpy_eur = currency_convert['JPY_USD'] / currency_convert['EUR_USD']
    ils_eur = currency_convert['ILS_USD'] / currency_convert['EUR_USD']
    eur_jpy = currency_convert['EUR_USD'] / currency_convert['JPY_USD']
    eur_ils = currency_convert['EUR_USD'] / currency_convert['ILS_USD']
    print('currencies {}'.format(currency_convert))
    print('jpyeur {} eurjpy{} ilseur {} eurils {}'.format(jpy_eur,eur_jpy, ils_eur,eur_ils))
    for ticklist in ticklist_list:
        for tick in ticklist:
            print('tick:{}'.format(tick))
            coin1,coin2 = tick['pair'].split('_')
            if coin1 == 'JPY': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] * eur_jpy
                tick['bid_eur'] = tick['bid'] * eur_jpy
            elif coin1 == 'USD': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] * currency_convert['EUR_USD']
                tick['bid_eur']=tick['bid'] * currency_convert['EUR_USD']
            elif coin1 == 'ILS': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] * eur_ils
                tick['bid_eur']=tick['bid'] * eur_ils

            if coin2 == 'JPY': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] / eur_jpy
                tick['bid_eur'] = tick['bid'] / eur_jpy
            elif coin2 == 'USD': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] / currency_convert['EUR_USD']
                tick['bid_eur']=tick['bid'] / currency_convert['EUR_USD']
            elif coin2 == 'ILS': #       ,'USD','ILS']:
                tick['ask_eur']=tick['ask'] / eur_ils
                tick['bid_eur']=tick['bid'] / eur_ils
    return(ticklist_list)

#
def chart_all(ticklist,pairs=['EUR_BTC','LTC_BTC','ETH_BTC','BTG_BTC','BCH_BTC']):
    for i,pair in enumerate(pairs):
        chart(ticklist,pair_to_show=pair,fig_num=i+1)


def chart(tick_list,pair_to_show='EUR_BTC',fig_num=1):
    flat_list = [element for sublist in tick_list for element in sublist]
    # return flat_list
    symbol_map = {'bitflyer': 'o', 'bit2c': 'x', 'kraken': '*'}
    showcoin1, showcoin2 = pair_to_show.split('_')
    ncol=0
    plt.figure(fig_num)
    plt.ion()
    for tick in flat_list:
        pair = tick['pair']
        coin1, coin2 = pair.split('_')
        if (pair_to_show==pair) or (coin1 in fiat_list and coin2=='BTC' and pair_to_show=='EUR_BTC'):  #fiat-crypto pairs should all have extra ask_eur and bid_eur elements
            print('plotting {} vs {} on fig {}'.format(pair_to_show,pair,fig_num))
            exchange = tick['exchange']
            timestamp=tick['timestamp']
            if not exchange in symbol_map:
                print('no symbol for {}'.format(exchange))
                symbol_map[exchange]='.'
            ask_symbol = 'r'+symbol_map[exchange]
            bid_symbol = 'g'+symbol_map[exchange]
    #        plt.subplot(212)
    #first plot crpt vs fiat
            ask_to_plot = tick['ask']
            bid_to_plot = tick['bid']
            if coin1 in fiat_list and coin1!='EUR':
                ask_to_plot = tick['ask_eur']
                bid_to_plot = tick['bid_eur']
            plt.plot(timestamp,ask_to_plot,ask_symbol,label=exchange+' ask'+pair)
            plt.plot(timestamp,bid_to_plot,bid_symbol,label=exchange+' bid'+pair)
            ncol=ncol+1
    if ncol==0:
        return
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, mode="expand", borderaxespad=0., ncol=ncol)
    plt.title(pair_to_show)
    plt.grid(True)
    plt.show()
    plt.pause(0.001)

def identify_arbitrages(tick_list_list):
    for i,tick_list1 in enumerate(tick_list_list[:-1]):
        for tick1 in tick_list1:
            for j,tick_list2 in enumerate(tick_list_list[i+1:]):
                for tick2 in  tick_list2:

                    pair1=tick1['pair']
                    pair2=tick2['pair']
                    coin1_1,coin1_2=pair1.split('_')
                    coin2_1,coin2_2=pair2.split('_')
                    if pair1==pair2 or coin1_1 in fiat_list and coin1_2 == 'BTC' and coin2_1 in fiat_list and coin2_2=='BTC': #same pair on one fiat and one btc
                        exchange1=tick1['exchange']
                        exchange2=tick2['exchange']
                        print('looking for arbitrage in {} {} vs {} {}'.format(exchange1,exchange2,pair1,pair2))
                        if coin1_1 in fiat_list and coin1_1 != 'EUR':
                            bid1=tick1['bid_eur']
                            ask1=tick1['ask_eur']
                        else:
                            bid1=tick1['bid']
                            ask1 = tick1['ask']
                        if coin2_1 in fiat_list and coin2_1 != 'EUR':
                            bid2 = tick2['bid_eur']
                            ask2 = tick2['bid_eur']
                        else:
                            bid2 = tick2['bid']
                            ask2 = tick2['ask']
                        spread1=bid1-ask2
                        spread2=bid2-ask1
                        if spread1>0 :
                            print("{} {} spread {} {} %".format(pair1, pair2, spread1, spread1 / bid1))
                            if coin1_1 not in fiat_list:
                                print("OH MY @#$@#$ GOD")
                        if spread2>0 :
                            if coin1_1 not in fiat_list:
                                print("OH MY @#$@#$ GOD")
                            print("{} {} spread {} {} %".format(pair1,pair2,spread2,spread2/bid2))



def bitflyer_ticker_multi(pairs=['JPY_BTC','BTC_BCH','BTC_ETH']):  #'ETC_BTC'
    all_results = []
    p=Pool(len(pairs))
    all_results = p.map(bitflyer_ticker,pairs)
    return all_results
    # for pair in pairs:
    #     all_results.append(pair)


def bitflyer_ticker(pair='JPY_BTC'):
#BTC_JPY,ETH_BTC,BCH_BTC

#for list of markets:
#    https: // api.bitflyer.jp / v1 / getmarkets
  #  ticker = public.Public().getticker()
    #returns eg
#    {'volume': 216014.77565499, 'product_code': 'BTC_JPY', 'tick_id': 1730512, 'ltp': 1724530.0,
#     'timestamp': '2017-12-10T22:39:02.24', 'best_bid': 1723374.0, 'best_ask_size': 16.690179,
#     'total_ask_depth': 2087.30139103, 'volume_by_product': 39867.96588841, 'best_bid_size': 0.40004,
#     'total_bid_depth': 4277.58274837, 'best_ask': 1724530.0}

    if pair == 'JPY_BTC':
        api_pair = 'BTC_JPY'
    elif pair == 'BTC_ETH':
        api_pair = 'ETH_BTC'
    elif pair == 'BTC_BCH':
        api_pair = 'BCH_BTC'
    elif pair == 'JPY_LTC':
        api_pair = 'LTC_JPY'
    else:
        print('pair {} not recognized'.format(pair))
        return None
    api_url = 'https://api.bitflyer.jp/v1/ticker?product_code='+api_pair
    print('bitflyer url {}'.format(api_url))

    data = safe_get(api_url)
    if data is None:
        return None
    ticker = data.text
#    print('bitflyer ticker {}'.format(ticker))

    ticker = ast.literal_eval(ticker)

    product = ticker['product_code']

    retval={}
    retval['pair']=pair
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


def bit2c_ticker_multi(pairs=['ILS_BTC','ILS_LTC','ILS_BCH','ILS_BTG']):
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
    elif pair=='ILS_LTC':
        url_orderbook = 'https://www.bit2c.co.il/Exchanges/LtcNis/orderbook.json'
    elif pair == 'ILS_BCH':
        url_orderbook = 'https://www.bit2c.co.il/Exchanges/BchNis/orderbook.json'
    elif pair == 'ILS_BTG':
        url_orderbook = 'https://www.bit2c.co.il/Exchanges/BtgNis/orderbook.json'
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

    retval = {}
    retval['pair'] = pair
    retval['bid']=book['bids'][0][0]
    retval['bid_volume']=book['bids'][0][1]
    retval['ask']=book['asks'][0][0]
    retval['ask_volume'] = book['asks'][0][1]
    retval['exchange'] = 'bit2c'
    retval['timestamp'] = round(time.time(),1)
    return(retval)
#

def generate_extra_pairs(tick_lists):
    '''
    given e.g. eur-ltc and eur-btc , generate ltc-btc
    for now generate everything in terms of btc
    :param tick_lists: list of ticks , one per exchange
    :return:
    '''
    fiat_currencies=['ILS','EUR','JPY'] #add as necessary
    fiat_btc_currencies={f:[] for f in fiat_currencies}
    for tick_list in tick_lists:
        # if tick['pair'] == 'ILS_BTC':
        #     fiat_btc_currencies['ILS'].append(tick)
        # elif tick['pair'] == 'EUR_BTC':
        #     fiat_btc_currencies['EUR'].append(tick)
        # elif tick['pair'] == 'JPY_BTC':
        #     fiat_btc_currencies['JPY'].append(tick)
        exchange=tick_list[0]['exchange']
        pairs=[tick['pair'] for tick in tick_list]
#        print('looking for extra pairs in exchange {} which has pairs {}'.format(exchange,pairs))
        got_btc = False
        for tick in tick_list:    #make btc-other_crypto ticks - 1. find btc tick
            pair = tick['pair']
            coin1,coin2=pair.split('_')
            if coin1 in fiat_currencies and coin2 == 'BTC':
                exchange_coin=coin1
                btc_pair = pair
                btc_tick = tick
                got_btc=True
 #               print('btc exchange {} coin {} '.format(tick['exchange'],exchange_coin))
                # exchange_coin_btc_bid=tick['bid']
                # exchange_coin_btc_ask=tick['ask']
                # exchange_coin_btc_bidvol=tick['bid_volume']
                # exchange_coin_btc_askvol=tick['bid_volume']
        if not got_btc:
            print('did not find any btc for exchange {}'.format(exchange))
            continue

        for tick in tick_list:    #make btc-other_crypto ticks  2.convert fiat-nonbtc_crypto to nonbtc_crypto-btc
            pair = tick['pair']
            coin1,coin2=pair.split('_')
            if coin1 in fiat_currencies and coin2 != 'BTC':
                if coin1!=exchange_coin:
                    print('pair {} not comparable to pair {} on exchange {}'.format(pair,btc_pair,exchange))
                    continue
                new_tick={}
                new_tick['pair'] = coin2+'_BTC'
                # whoever wants to bid ltc for btc
                # needs to first  get ltc , by paying the ask of e..g euro-ltc
                # so  the bid ltc-btc_bid = euro-btc_bid / euro-ltc_ask
                new_tick['bid'] = btc_tick['bid']/tick['ask']   #need to pay the ltc ask and the btc bid
                new_tick['ask'] = btc_tick['ask']/tick['bid']
                new_tick['exchange'] = exchange
                new_tick['timestamp']=btc_tick['timestamp']
                new_tick['n_transactions']=2
                #volume is determined by min between the btc and non-btc crypto vol, i compare them in terms of fiat
                ask_min_vol_fiat = min(tick['ask']*tick['ask_volume'],btc_tick['ask']*btc_tick['ask_volume'])
                ask_vol_btc=ask_min_vol_fiat/btc_tick['ask']
                new_tick['ask_volume'] = ask_vol_btc
                bid_min_vol_fiat = min(tick['bid'] * tick['bid_volume'],btc_tick['bid']*btc_tick['bid_volume'])
                bid_vol_btc=bid_min_vol_fiat/btc_tick['bid']
                new_tick['bid_volume'] = bid_vol_btc
             #   print('ask min vol fiat {} bid min vol fiat {}'.format(ask_min_vol_fiat,bid_min_vol_fiat))
             #    print('new tick:\n')
             #    print(json.dumps(new_tick,indent=2))
             #    print('current tick:\n')
             #    print(json.dumps(tick,indent=2))
             #    print('btc tick:\n')
             #    print(json.dumps(btc_tick,indent=2))
                tick_list.append(new_tick)
    return(tick_lists)


def kraken_ticker_multi(pairs=['EUR_BTC','EUR_LTC','BTC_BCH','BTC_ETH','EUR_BCH']): #eur_btg
    #asset pairs -  https://api.kraken.com/0/public/AssetPairs
    # api = krakenex.API()
    # k = KrakenAPI(api)

    normal_to_kraken_names={'EUR_BTC':'XXBTZEUR','EUR_LTC':'XLTCZEUR','EUR_BCH':'BCHEUR','BTC_ETH':'XETHXXBT','BTC_BCH':'XETHXXBT'}
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
        retval['lastprice']=float(v['c'][0])
        retval['bid']=float(v['b'][0])
        retval['bid_volume']=float(v['b'][2])
        retval['ask']=float(v['a'][0])
        retval['ask_volume']=float(v['a'][2])
        retval['exchange'] = 'kraken'
        retval['timestamp'] = round(time.time(),1)

        all_vals.append(retval)
    return all_vals

def func_wrap(func):
    return func

def get_all_apis(func_list=[kraken_ticker_multi(),bit2c_ticker_multi(),bitflyer_ticker_multi()]):
    # flat_list = [element for sublist in all_results for element in sublist]
    # return flat_list
    p=Pool(len(func_list))
    all_results = p.map(func_wrap,func_list)
    return all_results


if __name__=="__main__":
    my_arbitrator = arbitrageur()
    last_time=time.time()
    while(1):
        if time.time()-last_time>60:
            my_arbitrator.update_info()
            last_time=time.time()

    # api_prices = update_info()
    # api_prices=get_all_apis()
    # print(json.dumps(api_prices,indent=2))
    # currency_convert = currency_conversions()
    # full_prices = convert(api_prices,currency_convert)
    # print(json.dumps(full_prices,indent=2))

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




"""  kraken oairs
BCHEUR	{…}
BCHUSD	{…}
BCHXBT	{…}
DASHEUR	{…}
DASHUSD	{…}
DASHXBT	{…}
EOSETH	{…}
EOSXBT	{…}
GNOETH	{…}
GNOXBT	{…}
USDTZUSD	{…}
XETCXETH	{…}
XETCXXBT	{…}
XETCZEUR	{…}
XETCZUSD	{…}
XETHXXBT	{…}
XETHXXBT.d	{…}
XETHZCAD	{…}
XETHZCAD.d	{…}
XETHZEUR	{…}
XETHZEUR.d	{…}
XETHZGBP	{…}
XETHZGBP.d	{…}
XETHZJPY	{…}
XETHZJPY.d	{…}
XETHZUSD	{…}
XETHZUSD.d	{…}
XICNXETH	{…}
XICNXXBT	{…}
XLTCXXBT	{…}
XLTCZEUR	{…}
XLTCZUSD	{…}
XMLNXETH	{…}
XMLNXXBT	{…}
XREPXETH	{…}
XREPXXBT	{…}
XREPZEUR	{…}
XXBTZCAD	{…}
XXBTZCAD.d	{…}
XXBTZEUR	{…}
XXBTZEUR.d	{…}
XXBTZGBP	{…}
XXBTZGBP.d	{…}
XXBTZJPY	{…}
XXBTZJPY.d	{…}
XXBTZUSD	{…}
XXBTZUSD.d	{…}
XXDGXXBT	{…}
XXLMXXBT	{…}
XXMRXXBT	{…}
XXMRZEUR	{…}
XXMRZUSD	{…}
XXRPXXBT	{…}
XXRPZEUR	{…}
XXRPZUSD	{…}
XZECXXBT	{…}
XZECZEUR	{…}
XZECZUSD	{…}
"""