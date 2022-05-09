#from asyncio.base_subprocess import *
from unittest import result
from iqoptionapi.stable_api import IQ_Option
from talib import  *
import numpy
import time
import concurrent.futures
from getpass import getpass
import numpy as np
from talib.abstract import *
from talib import BBANDS
from talib import SMA
from datetime import datetime
print("//////////*** BOT BBANDS ***\\\\\\\\\\")
#email = input("Please enter your email : ")
#password = getpass()
def bot_bbands(asset):
    I_want_money = IQ_Option('dsfkkdqsfmjkldmq@gmail.com','12345678')
    check = I_want_money.connect()
    goal=asset#input("enter Asset :")
    if check:
        print(f"Connect Successfully to {goal}")     
    else:
        print(f"Connect Failed to {goal}") 
    
    size=60
    maxdict=200
    deals_done = 0
    Money=1000
    expirations_mode=3
    I_want_money.start_candles_stream(goal,size,maxdict)
    while True:
        time.sleep(0.25)
        candles=I_want_money.get_realtime_candles(goal,size)
        inputs = {
            'open': np.array([]),
            'close': np.array([]),
        }
        for timestamp in list(candles.keys()):
            open=inputs["open"]=np.append(inputs["open"],candles[timestamp]["open"] )
            close = inputs["close"]=np.append(inputs["open"],candles[timestamp]["close"] )     
        upperband, middleband, lowerband = BBANDS(close*100000, timeperiod=20, nbdevup=2.5, nbdevdn=2.5, matype=0)
        real_200 = SMA(close*100000, timeperiod=200)
        real_50= SMA(close*100000, timeperiod=50)
        real_20 = SMA(close*100000, timeperiod=20)
        up = upperband[-1]
        dn = lowerband[-1]
        md = middleband[-1]
        cls = close[-1] * 100000
        rl_200 = real_200[-1]
        rl_50 = real_50[-1] 
        rl_20 = real_20[-1]  
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if up < rl_200 and rl_50 > rl_20:
            if cls > up or cls ==  up :
                print(f"#{goal} ¦Sell deal !!!!!!!!!!!!!!!¦ => current time : {current_time} ")
                ACTION="put"
                id=I_want_money.buy(Money,goal,ACTION,expirations_mode)
                remaning_time=I_want_money.get_remaning(expirations_mode)
                time.sleep(remaning_time) 
                deals_done += 1
        if dn > rl_200 and rl_20 > rl_50:
            if cls < dn or cls ==  dn : 
                print(f"#{goal} ¦Buy deal !!!!!!!!!!!!!!!!¦ => current time : {current_time} ")
                ACTION="call"
                id=I_want_money.buy(Money,goal,ACTION,expirations_mode)
                remaning_time=I_want_money.get_remaning(expirations_mode)
                time.sleep(remaning_time)
                deals_done += 1
        if cls != dn and cls != up :
           
            print(f"¦Deals donne :{deals_done}¦ => current time : {current_time} ")
        
with concurrent.futures.ProcessPoolExecutor() as executor:
    asset = ['EURUSD','EURJPY','EURGBP','GBPJPY','USDJPY','GBPUSD','USDJPY','AUDUSD','AUDJPY','AUDCAD']
    results = executor.map(bot_bbands,asset)


        
       
        
            
            
    

        
#<>