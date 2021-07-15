# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 22:16:48 2021

@author: rejit
"""

import datetime
import yfinance as yf
import time
import smtplib, ssl

#add ticker and average price on below dictionary 
stocks ={
         "V":245.83,
         "MSFT":282.68
         }

start = datetime.datetime.today() - datetime.timedelta(7)
end = datetime.datetime.today()

interval_duration = "1h"
time_sleep_input = 3600 #print every hour

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

#add sender_gmail_email, reciever_email and gmail app password
#details regards how to generate app password https://support.google.com/accounts/answer/185833?hl=en

sender_email = "enter_sender_email@gmail.com"
receiver_email = "enter_receiver_email@gmail.com"
password = "enter_password"


# time duration for trading
trading_start_time= "09:00"
trading_end_time = "22:00"


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


while True:
    ohlcv_data ={}
    print(datetime.datetime.now())
    for ticker in stocks.keys():
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        trading_current_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
        if (ohlcv_data[ticker]["Adj Close"][-1] > stocks[ticker] and \
            is_between(trading_current_time, (trading_start_time, trading_end_time)))\
            == True:
           print(f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = {ohlcv_data[ticker]["Adj Close"][-1]} ')
           message = f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = Current value {ohlcv_data[ticker]["Adj Close"][-1]} '
           context = ssl.create_default_context()
           with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
 
    print("\n")
    if ((trading_current_time == trading_start_time) or\
            (trading_current_time == trading_end_time) ):
        time.sleep(0)
    else:    
        time.sleep(time_sleep_input)