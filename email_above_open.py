# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 22:16:48 2021

@author: rejit
"""

import datetime
import yfinance as yf
import time
import smtplib, ssl
from apscheduler.schedulers.blocking import BlockingScheduler

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
trading_start_time_hour= 10
trading_end_time_hour = 22




sched = BlockingScheduler()
@sched.scheduled_job('interval',hours=1)
def download_and_email():
    ohlcv_data ={}
    print(datetime.datetime.now())
    for ticker in stocks.keys():
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        trading_current_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
        if (ohlcv_data[ticker]["Adj Close"][-1] > stocks[ticker])\
            and ((datetime.datetime.now().hour >= trading_start_time_hour) and\
            (datetime.datetime.now().hour <= trading_end_time_hour))== True:
           print(f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = {ohlcv_data[ticker]["Adj Close"][-1]} ')
           message = f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = Current value {ohlcv_data[ticker]["Adj Close"][-1]} '
           context = ssl.create_default_context()
           with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Email sent.")
    print("\n")
sched.start()
    
 
   
    