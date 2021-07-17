# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 22:16:48 2021

@author: rejit
"""

import datetime
import yfinance as yf
import time
import smtplib, ssl
# from apscheduler.schedulers.blocking import BlockingScheduler
import schedule

#add ticker and average price on below dictionary 
#add ticker and average price on below dictionary 
stocks ={
         "V":245.83,
         "MSFT":282.68,
         "PRS.OL":2.77,
         "ARKK" :127.70,
         "CTXS":123.77,
         "CLOV":11.70,
         "WISH":13.54,
         "KMI":20.02,
         "NAS.OL":25,
         "MCHP":154.61,
         "ETH-USD":2169.2,
         "ARKK":130.3,
         "ZAP.OL":40.24,
         "PRS.OL":2.77,
         "AKRBP.OL":281.9,
         "ORK.OL":93.3
        
         }

print ("RUNNING")
print (f'Start time = {datetime.datetime.now()}')

interval_duration = "1h"
time_sleep_input = 3600 #print every hour

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

#add sender_gmail_email, reciever_email and gmail app password
#details regards how to generate app password https://support.google.com/accounts/answer/185833?hl=en

sender_email = "sender_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = "gmail_app_password"


# time duration for trading
trading_start_time_hour= "09"
trading_end_time_hour = "22"

# sched = BlockingScheduler()
# @sched.scheduled_job('interval',hours=1)
def download_and_email():
    ohlcv_data ={}
    print(datetime.datetime.now())
    message =""
    for ticker in stocks.keys():
        start = datetime.datetime.today() - datetime.timedelta(1)
        end = datetime.datetime.today()
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        trading_current_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
        if (ohlcv_data[ticker]["Adj Close"][-1] > stocks[ticker])\
            and (datetime.datetime.today().weekday() <= 4) and ((datetime.datetime.now().hour >= int(trading_start_time_hour)) and\
            (datetime.datetime.now().hour <= int(trading_end_time_hour)))== True:
           print(f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = {ohlcv_data[ticker]["Adj Close"][-1]} ')
           message = f'{ticker} is above. Avg.Value = {stocks[ticker]} and Current value = Current value {ohlcv_data[ticker]["Adj Close"][-1]} \n '
           message+=message
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent.")
    print("\n")
# 
# 

schedule.every().hour.do(download_and_email)

#scheduling every week day
schedule.every().monday.at(trading_start_time_hour+":00").do(download_and_email)
schedule.every().monday.at(trading_end_time_hour+":00").do(download_and_email)
schedule.every().tuesday.at(trading_start_time_hour+":00").do(download_and_email)
schedule.every().tuesday.at(trading_end_time_hour+":00").do(download_and_email)
schedule.every().wednesday.at(trading_start_time_hour+":00").do(download_and_email)
schedule.every().wednesday.at(trading_end_time_hour+":00").do(download_and_email)
schedule.every().thursday.at(trading_start_time_hour+":00").do(download_and_email)
schedule.every().thursday.at(trading_end_time_hour+":00").do(download_and_email)
schedule.every().friday.at(trading_start_time_hour+":00").do(download_and_email)
schedule.every().friday.at(trading_end_time_hour+":00").do(download_and_email)


while True:
    schedule.run_pending()
    time.sleep(1)    
 
   
    
