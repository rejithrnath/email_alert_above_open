# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 22:16:48 2021

@author: rejit
"""

import datetime
import yfinance as yf
import time
import smtplib, ssl
import temp.config
import schedule
import yfinance as yf2

#add ticker and average price on below dictionary 
#add ticker and average price on below dictionary 
stocks ={
         "V":245.83,
         "MSFT":282.68,
         "ARKK" :127.70,
         "CTXS":123.77,
         "CLOV":11.70,
         "WISH":13.54,
         "KMI":20.02,
         "NAS.OL":25,
         "MCHP":154.61,
         "ETH-USD":2169.2,
         "ARKK":130.3,
         "AKRBP.OL":281.9,
         "ORK.OL":93.3,
         "NVAX":217.98,
         "SPCE":32.8,
         "ADSK":298,
         "VTR":61,
         "SNPS":280,
         "ISRG":961,
         "PYPL":300,
         "WLTW":222.8,
         "TFX":388.5,
         "COG":16.21,
         
         }

print ("RUNNING")
print (f'Start time = {datetime.datetime.now()}')

interval_duration = "15m"
# time_sleep_input = 3600 #print every hour

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

#add sender_gmail_email, reciever_email and gmail app password
#details regards how to generate app password https://support.google.com/accounts/answer/185833?hl=en

sender_email = temp.config.sender_email
receiver_email = temp.config.receiver_email
password = temp.config.password


# time duration for trading
trading_start_time_hour= "09"
trading_end_time_hour = "22"

# sched = BlockingScheduler()
# @sched.scheduled_job('interval',hours=0.25)
def download_and_email():
    ohlcv_data ={}
    day_ohlcv_data = {}
    df_pos = {}
    print(datetime.datetime.now())
    message =""
    for ticker in stocks.keys():
        start = datetime.datetime.today() - datetime.timedelta(1)
        end = datetime.datetime.today()
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        ohlcv_data[ticker]['gain_pc'] =(ohlcv_data[ticker]["Adj Close"] - stocks[ticker]) *100 /stocks[ticker]
        day_ohlcv_data[ticker] = yf2.download(ticker,start,end, interval="1d", progress = False)
        day_ohlcv_data[ticker]['daily_pc'] = (day_ohlcv_data[ticker]['Close'] /day_ohlcv_data[ticker]['Close'].shift(1) -1)*100
        # trading_current_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
        if (ohlcv_data[ticker]["Adj Close"][-1] > stocks[ticker])\
            and (datetime.datetime.today().weekday() <= 4) and ((datetime.datetime.now().hour >= int(trading_start_time_hour)) and\
            (datetime.datetime.now().hour <= int(trading_end_time_hour)))== True:
           print(f'{ticker} is above. Avg.Value = {stocks[ticker]}, Gain  = { round(float(ohlcv_data[ticker]["gain_pc"][-1]),2) } %, Gain for day ={ round(float(day_ohlcv_data[ticker]["daily_pc"][-1]),2) } %')
           temp = f'{ticker} is above. Avg.Value = {stocks[ticker]}, Gain  = { round(float(ohlcv_data[ticker]["gain_pc"][-1]),2) } %, Gain for day ={ round(float(day_ohlcv_data[ticker]["daily_pc"][-1]),2) } %'
           
         
           message=message+ "\n"+temp
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        if(message!=""):
            server.sendmail(sender_email, receiver_email, message)
            print("Email sent.")
    # print({message})
    
# 
# 

download_and_email()
schedule.every(15).minutes.do(download_and_email)

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
 
   
    
