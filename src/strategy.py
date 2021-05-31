## https://docs.google.com/document/d/1rTk3wmyHzDmWItLolJ0Bj1wKoTwDZ2PJsndxA9X6Iwo/edit?usp=sharing
#  document for logic
import pymongo
import json
import pytz
import requests
import pandas as pd
import numpy as np
import io
import math
from time import sleep
from datetime import date, datetime, timedelta, time


def strike_nif_sell(item,nearest_expiry,monthend_expiry,exchange,xts, day_delta):
    # calculating entry, target, stoploss, suitable strike, and its premium to sell option as per above referenced document
    tradable = []
    spot_ce_nifty = []
    spot_pe_nifty = []
    spot_ce_BNF = []
    spot_pe_BNF = []    
    tzinfo = pytz.timezone('Asia/Kolkata') 
    now = datetime.now(tz= tzinfo)#tz= tzinf
    today = now.date()  
    df, _ = xts.read_data(item, 600, "NSECM",days=day_delta)
    print(df.head())
    if item=="NIFTY":
        max = xts.roundup(1.0015*df.high.max(),50)  ## step to roundup nifty after adding 0.15%
        if max:
            max_list = [max - x*50 for x in range(10)] # step 8 to step to find other contracts
            for element in max_list:
                da1, _ = xts.get_options_contract(item, "CE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
  
                quote = data0.oi[-1:].values[0]
                if data0.low.min() > 0.0085 * df.close[-1:].values[0] and quote > 37500: # step 9 and 10 or 11
                    # Calculating entry, target, and stoploss price
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'sell', "entry_p":xts.roundoff(0.9*data0.low.min()), "target": xts.roundoff(0.25*0.9*data0.low.min()),"stoploss":xts.roundoff(np.minimum(1.75*0.9*data0.low.min(),1.1*data0.high.max()))}) 
                    
        min = xts.rounddown(0.9985*df.low.min(),50) ## steps to round down nifty after subtracting 0.15%
        if min:
            min_list = [min + x*50 for x in range(10)] # step 8 to step up to find other contracts
            for element in min_list:
                da1, _ = xts.get_options_contract(item, "PE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
          
                quote = data0.oi[-1:].values[0]
                if data0.low.min() > 0.0085 * df.close[-1:].values[0] and quote > 37500:   # step 9 and 10 or 11
                    # Calculating entry, target, and stoploss price
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'sell', "entry_p":xts.roundoff(0.9*data0.low.min()), "target": xts.roundoff(0.25*0.9*data0.low.min()),"stoploss":xts.roundoff(np.minimum(1.75*0.9*data0.low.min(),1.1*data0.high.max()))}) 
    return tradable

def strike_bnf_sell(item,nearest_expiry,monthend_expiry,exchange,xts, day_delta):
    # calculating entry, target, stoploss, suitable strike, and its premium to sell option as per above referenced document
    tradable = []
    spot_ce_nifty = []
    spot_pe_nifty = []
    spot_ce_BNF = []
    spot_pe_BNF = []    
    tzinfo = pytz.timezone('Asia/Kolkata') 
    now = datetime.now(tz= tzinfo)#tz= tzinf
    today = now.date()  
    df, _ = xts.read_data(item, 600, "NSECM",days=day_delta)
    print(df.head())                    
    if item == "BANKNIFTY":
        max = xts.roundup(1.0015*df.high.max(),100)   ## steps to round down bank nifty after subtracting 0.15%
        if max:
            max_list = [max - x*100 for x in range(10)]    # step 8 to step to find other contracts
            for element in max_list:
                da1, _ = xts.get_options_contract(item, "CE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
         
                quote = data0.oi[-1:].values[0]
                if data0.low.min() > 0.011 * df.close[-1:].values[0] and quote > 10000:   # step 9 and 10 or 11
                    # Calculating entry, target, and stoploss price
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'sell', "entry_p":xts.roundoff(0.9*data0.low.min()), "target": xts.roundoff(0.25*0.9*data0.low.min()),"stoploss":xts.roundoff(np.minimum(1.75*0.9*data0.low.min(),1.1*data0.high.max()))})            
                    
        min = xts.rounddown(0.9985*df.low.min(),100)    ## steps to round down bank nifty after subtracting 0.15%
        if min:
            min_list = [min + x*100 for x in range(10)]    # step 8 to step to find other contracts
            for element in min_list:
                da1, _ = xts.get_options_contract(item, "PE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
            
                quote = data0.oi[-1:].values[0]
                if data0.low.min() > 0.011 * df.close[-1:].values[0] and quote > 10000:   # step 9 and 10 or 11
                    # Calculating entry, target, and stoploss price after looking at the table in document
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'sell', "entry_p":xts.roundoff(0.9*data0.low.min()), "target": xts.roundoff(0.25*0.9*data0.low.min()),"stoploss":xts.roundoff(np.minimum(1.75*0.9*data0.low.min(),1.1*data0.high.max()))})                 
    return tradable

def strike_nif_buy(item,nearest_expiry,monthend_expiry,exchange,xts, day_delta):
    # calculating entry, target, stoploss, suitable strike, and its premium to sell option as per above referenced document
    tradable = []
    spot_ce_nifty = []
    spot_pe_nifty = []
    spot_ce_BNF = []
    spot_pe_BNF = []   
    tzinfo = pytz.timezone('Asia/Kolkata') 
    now = datetime.now(tz= tzinfo)#tz= tzinf
    today = now.date()     
    df, _ = xts.read_data(item, 600, "NSECM",days=day_delta)
    print(df.head())
    if item=="NIFTY":
        max = xts.roundup(1.0015*df.high.max(),50)  ## step to roundup nifty after adding 0.15%
        if max:
            max_list = [max - x*50 for x in range(10)] # step 8 to step to find other contracts
            for element in max_list:
                da1, _ = xts.get_options_contract(item, "CE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)

                quote = data0.oi[-1:].values[0]
                # Calculating entry, target, and stoploss price
                if quote > 37500 and today.weekday() in [0,1,4,5,6]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.1*data0.high.max()), "target": xts.roundoff(1.6*1.1*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.4*1.1*data0.high.max(),0.9*data0.low.min()))}) 
                    
                if quote > 37500 and today.weekday() in [2,3]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.07*data0.high.max()), "target": xts.roundoff(1.5*1.07*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.5*1.07*data0.high.max(),0.93*data0.low.min()))}) 
                    
        min = xts.rounddown(0.9985*df.low.min(),50) ## steps to round down nifty after subtracting 0.15%
        if min:
            min_list = [min + x*50 for x in range(10)] # step 8 to step up to find other contracts
            for element in min_list:
                da1, _ = xts.get_options_contract(item, "PE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
         
                quote = data0.oi[-1:].values[0]
                # Calculating entry, target, and stoploss price
                if quote > 37500 and today.weekday() in [0,1,4,5,6]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.1*data0.high.max()), "target": xts.roundoff(1.6*1.1*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.4*1.1*data0.high.max(),0.9*data0.low.min()))}) 
                    
                if quote > 37500 and today.weekday() in [2,3]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.07*data0.high.max()), "target": xts.roundoff(1.5*1.07*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.5*1.07*data0.high.max(),0.93*data0.low.min()))}) 
    return tradable

def strike_bnf_buy(item,nearest_expiry,monthend_expiry,exchange,xts, day_delta):
    # calculating entry, target, stoploss, suitable strike, and its premium to sell option as per above referenced document
    tradable = []
    spot_ce_nifty = []
    spot_pe_nifty = []
    spot_ce_BNF = []
    spot_pe_BNF = []   
    tzinfo = pytz.timezone('Asia/Kolkata') 
    now = datetime.now(tz= tzinfo)#tz= tzinf
    today = now.date()     
    df, _ = xts.read_data(item, 600, "NSECM",days=day_delta)
    print(df.head())                    
    if item == "BANKNIFTY":
        max = xts.roundup(1.0015*df.high.max(),100)   ## steps to round down bank nifty after subtracting 0.15%
        if max:
            max_list = [max - x*100 for x in range(10)]    # step 8 to step to find other contracts
            for element in max_list:
                da1, _ = xts.get_options_contract(item, "CE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
              
                quote = data0.oi[-1:].values[0]
                # Calculating entry, target, and stoploss price
                if quote > 10000 and today.weekday() in [0,1,4,5,6]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.1*data0.high.max()), "target": xts.roundoff(1.6*1.1*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.4*1.1*data0.high.max(),0.9*data0.low.min()))}) 
                    
                if quote > 10000 and today.weekday() in [2,3]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.07*data0.high.max()), "target": xts.roundoff(1.5*1.07*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.5*1.07*data0.high.max(),0.93*data0.low.min()))}) 
                    
        min = xts.rounddown(0.9985*df.low.min(),100)    ## steps to round down bank nifty after subtracting 0.15%
        if min:
            min_list = [min + x*100 for x in range(10)]    # step 8 to step to find other contracts
            for element in min_list:
                da1, _ = xts.get_options_contract(item, "PE", element, nearest_expiry, monthend_expiry) # step to get contracts
                spot_ce_nifty.append(da1)
                data0, _ = xts.read_data(da1, 600,exchange, item, days=day_delta)
                
                quote = data0.oi[-1:].values[0]
                # Calculating entry, target, and stoploss price
                if quote > 10000 and today.weekday() in [0,1,4,5,6]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.1*data0.high.max()), "target": xts.roundoff(1.6*1.1*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.4*1.1*data0.high.max(),0.9*data0.low.min()))}) 
                    
                if quote > 10000 and today.weekday() in [2,3]: # step 9 and 10 or 11
                    tradable.append({"symbol":da1,'category':item,"current_p":data0.close[-1:].values[0],'time':now,'action':'buy', "entry_p":xts.roundoff(1.07*data0.high.max()), "target": xts.roundoff(1.5*1.07*data0.high.max()),"stoploss":xts.roundoff(np.maximum(0.5*1.07*data0.high.max(),0.93*data0.low.min()))})       
    return tradable