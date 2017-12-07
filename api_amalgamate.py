__author__ = 'jeremy'
__author__ = 'jeremy'

import krakenex
from pykrakenapi import KrakenAPI
import urllib.request
from urllib.request import Request, urlopen

import urllib.request
#from urllib.request import  urlopen
#import urllib2
from bs4 import BeautifulSoup
import pandas

from random import choice
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
import time
import ast
import sys

url='https://www.bit2c.co.il/'

import numpy as np

from selenium import webdriver



import requests, json

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
    print('url {} text {}'.format(data.url,data.text))
    print('data for rget:{}'.format(data))
#    dict=ast.literal_eval(data.text)
    dict=data.text
    dict=json.loads(data.text)
    print('url {} text {}'.format(data.url,dict))
    usd_ils=dict['quotes']['USDILS']
    usd_eur=dict['quotes']['USDEUR']
    listdata=[[usd_ils,usd_eur]]
    print('listdata {}'.format(listdata))
    df=pandas.DataFrame(data=listdata,columns=['USDILS','USDEUR'])
    return(df)


if __name__=="__main__":
    while(1):
        fname='btc_data_'+str(round(time.time(),0))+'.xlsx'
        writer = pandas.ExcelWriter(fname, engine='xlsxwriter')

        #get eur-ils conversion (thru usd ,, didnt find straight conversion)
        convert=currency_conversion()

        #get bit2c bid/ask tables and ticker
        b2c_bid,b2c_ask,b2c_tick=bit2c_ticker()
        print('b2cbid:{}'.format(b2c_bid))
        print()
        kraken_book,kraken_spread,kraken_tick=kraken_ticker()
        print('krakenbook:{}]'.format(kraken_book))
        print('krakenbtick:{}]'.format(kraken_tick))

#        alldata={'ilsbtc@bt2c':bit2c_data,'eurbtc@kraken':kraken_data}

        # Write each dataframe to a different worksheet.
        sleeptime=5*60
        try:
            b2c_bid.to_excel(writer, sheet_name='b2cbid')
            b2c_ask.to_excel(writer, sheet_name='b2cask')
            b2c_tick.to_excel(writer, sheet_name='b2ctick')
            convert.to_excel(writer, sheet_name='USDILSEUR')
    #        print(np.ndim(kraken_spread))
     #       print(np.ndim(kraken_tick))
            # print(np.ndim(kraken_book))
            # kraken_spread.to_excel(writer, sheet_name='kraken_spread')
            kraken_tick.to_excel(writer, sheet_name='kraken_tick')
            # kraken_book.to_excel(writer, sheet_name='kraken_book')

            writer.save
        except:
            print('some problem writing')
            print(sys.exc_info())
            sleeptime=30
        # with(open(fname,mode='a')) as fp:
        #     json.dump(alldata,fp,indent=4)
        #     fp.close()
        time.sleep(sleeptime)
# help(KrakenAPI)
#



# doselenium=False
# if(doselenium):
#     options = webdriver.ChromeOptions()
#     options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
#     options.add_argument('window-size=800x841')
#     options.add_argument('headless')
#     driver = webdriver.Firefox()
#     dr=driver.get(url_ticker)
#
#     time.sleep(6)
#
#     d=driver.find_elements()
#     print('driver {} d{}'.format(dr,d))
#     dr=driver.get(url_ticker)
#
#     print('driver {} d{}'.format(dr,d))
#
#     #EC.presence_of_element_located((By.NAME, "pre"))
#     # try:
#     #     element = WebDriverWait(driver, 10).until(
#     #         EC.presence_of_element_located((By.TAG_NAME, "pre"))
#     # #        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "pre"))
#     #      #   EC.presence_of_element_located((By.ID, "body"))
#     #      #   EC.text_to_be_present_in_element((By.TAG_NAME,'pre','ll')
#     #     )
#     # finally:
#     #     pass
#     #    driver.quit()
#     #print(element)
#     d=driver.find_elements()
#     print('elements:{}'.format(d))
#     d=driver.page_source
#     print('source:{}'.format(d))
#     # d=driver.find_element(by=By.NAME,value='pre')
#     # print('d={}'.format(d))
#     # topLinks = driver.find_elements_by_xpath("//div/p/a[contains(@class, 'title')]")
#     # for link in topLinks:
#     #   print 'Title: ', link.text
#     driver.quit()
#
#
#
#
# dob2c=False
# if dob2c:#using bit2c api
#     import Bit2cClient
#     key='361e37d6-688d-4e37-8889-24e7eb679389'
#     secret='65578FA4BF6AC1A82E505F931297B30992B93407C6A26F7352EDB7975DD08CBC'
#     client=Bit2cClient.Bit2cClient(Url=url,Key=key,Secret=secret)
#     client.GetTicker()
#     client.GetTicker(Pair='BtcNis')
#     #ll - last price
#     #av - last 24 hours price avarage
#     #a - last 24 hours volume
#     #h - highest buy order
#     #l - lowest sell order
#     print('last {} highest buy order {} lowest sell {} vol24h {} av24h {}'.format(t.ll(),t.h,t.l,t.a,t.av))
#
#
#
#     #url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
#    # payload = json.load(open("request.json"))
#    #  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
#    #  r = requests.get(url, headers=headers)
#    #  print(r)
#    #  print(r.content)
#   #  r = requests.post(url, data=json.dumps(payload), headers=headers)
#
# docurl=True
#
#
# doreq=True
# if doreq:#using get - hits 503
#     print('trying get req')
#     r = requests.get(url)
#     print(r.content)
#     response=urlopen(url)
#     print('r:'+str(response))
#
#
#
#
#
#
# # req = Request('https://www.bit2c.co.il/', headers={'User-Agent': 'Mozilla/5.0'})
# # webpage = urlopen(req).read()
# #
# # page = urllib.request.urlopen('https://www.bit2c.co.il/')
# # print(page.read())
# #
# #
# #

#url = 'https://www.bit2c.co.il/'


def random_headers():
    desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# r = requests.get(url,headers=random_headers())
# print(r)
# print(r.content)


#
# input('ret to cont')
# browser = webdriver.Firefox()
# print('ok')
#
# driver = webdriver.Firefox()
# driver.get(url)
# print(driver.title)
# #assert "Python" in driver.title
# elem = driver.find_element_by_name("TICKER_BUY")
#
#
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
#
# page = urlopen(url)
# print('page {}'.format(page))
#
#
# class AppURLopener(urllib.request.FancyURLopener):
#     version = "Mozilla/5.0"
#
# opener = AppURLopener()
# response = opener.open('https://www.bit2c.co.il/')
# print(response)
# print(response.info())
# print('code:{}'.format(response.code))
#
# req = Request('https://www.bit2c.co.il/', headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()
# print(webpage)
#
# page = urllib.request.urlopen('https://www.bit2c.co.il/')
# print(page.read())
