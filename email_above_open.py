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

start = datetime.datetime.today() - datetime.timedelta(1)
end = datetime.datetime.today()

interval_duration = "1h"
time_sleep_input = 3600 #print every hour

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

#add sender_gmail_email, reciever_email and gmail app password
#details regards how to generate app password https://support.google.com/accounts/answer/185833?hl=en

sender_email = "senderemail@gmail.com"
receiver_email = "reciveremail@gmail.com"
password = "password"

while True:
    ohlcv_data ={}
    print(datetime.datetime.now())
    for ticker in stocks.keys():
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        if ohlcv_data[ticker]["Adj Close"][-1] > stocks[ticker]:
           print(f'{ticker} is above. Current value {stocks[ticker]} ')
           message = f'{ticker} is above. Current value {stocks[ticker]} '
           
           context = ssl.create_default_context()
           with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
 
    print("\n")
    time.sleep(time_sleep_input)