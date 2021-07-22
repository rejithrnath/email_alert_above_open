  
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 20:15:13 2021
@author: Rejith Reghunathan 
@email: rejithrnath@gmail.com
"""

import datetime
import yfinance as yf
import time
import smtplib, ssl
import temp.config
import schedule
import requests
from bs4 import BeautifulSoup

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
         "ADSK":298,
         "VTR":61,
         "SNPS":280,
         "ISRG":961,
         "PYPL":300,
         "COG":16.21,
         "HES":76.41,
         }

print ("RUNNING")
print (f'Started time = {datetime.datetime.now()}')

#interval_duration = "1h"
interval_duration = "1h"

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

#add sender_gmail_email, reciever_email and gmail app password
#details regards how to generate app password https://support.google.com/accounts/answer/185833?hl=en

sender_email = temp.config.sender_email
receiver_email = temp.config.receiver_email
password = temp.config.password


# time duration for trading
trading_start_time_hour= "08"
trading_end_time_hour = "22"

def download_and_email():
    ohlcv_data ={}
    day_ohlcv_data = {}
    df_pos = {}
    gain_day={}
    print(datetime.datetime.now())
    message =""
    for ticker in stocks.keys():
        start = datetime.datetime.today() - datetime.timedelta(30)
        end = datetime.datetime.today()
        ohlcv_data[ticker] = yf.download(ticker,start,end, interval=interval_duration, progress = False)
        ohlcv_data[ticker].dropna(axis = 0, inplace = True) # remove any null rows 
        ohlcv_data[ticker]['gain_pc'] =(ohlcv_data[ticker]["Adj Close"] - stocks[ticker]) *100 /stocks[ticker]
        
        #Webscrapping
        temp_dir = {}
        url = 'https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
        headers={'User-Agent': "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        page_content = page.content
        soup = BeautifulSoup(page_content,'html.parser')
        tabl = soup.find_all("div", {"class" : "D(ib) Va(m) Maw(65%) Ov(h)"})
        for t in tabl:
            rows = t.find_all("span", {"class" : "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)"})
            for row in rows:
                temp_dir[row.get_text(separator=' ').split(" ")[1]]=row.get_text(separator=' ').split(" ")[1]
        
        #combining all extracted information with the corresponding ticker
        gain_day[ticker] = temp_dir
        
        
        #Gain Indicators
        
        ohlcv_data[ticker]['8dayEWM']  = ohlcv_data[ticker]['Adj Close'].ewm(span=8 , adjust=False).mean()
        ohlcv_data[ticker]['13dayEWM'] = ohlcv_data[ticker]['Adj Close'].ewm(span=13, adjust=False).mean()
        ohlcv_data[ticker]['21dayEWM'] = ohlcv_data[ticker]['Adj Close'].ewm(span=21, adjust=False).mean()
        ohlcv_data[ticker]['34dayEWM'] = ohlcv_data[ticker]['Adj Close'].ewm(span=34, adjust=False).mean()
        ohlcv_data[ticker]['55dayEWM'] = ohlcv_data[ticker]['Adj Close'].ewm(span=55, adjust=False).mean()
        ohlcv_data[ticker]['89dayEWM'] = ohlcv_data[ticker]['Adj Close'].ewm(span=89, adjust=False).mean()
        
        if ohlcv_data[ticker]['Adj Close'][-1]> ohlcv_data[ticker]['21dayEWM'][-1]:
            ohlcv_data[ticker]['above_21ema_on'] = "ON"
        else:
            ohlcv_data[ticker]['above_21ema_on'] = "OFF"
        
        
        if ohlcv_data[ticker]['Adj Close'][-1]> ohlcv_data[ticker]['8dayEWM'][-1] > ohlcv_data[ticker]['13dayEWM'][-1] and ohlcv_data[ticker]['13dayEWM'][-1] > ohlcv_data[ticker]['21dayEWM'][-1] and ohlcv_data[ticker]['21dayEWM'][-1] > ohlcv_data[ticker]['34dayEWM'][-1] and ohlcv_data[ticker]['34dayEWM'][-1] > ohlcv_data[ticker]['55dayEWM'][-1] and ohlcv_data[ticker]['55dayEWM'][-1] > ohlcv_data[ticker]['89dayEWM'][-1]:
            ohlcv_data[ticker]['stacked_on'] = "ON"
        else :
            ohlcv_data[ticker]['stacked_on'] = "OFF"
        
        if (ohlcv_data[ticker]["Adj Close"][-1] >= stocks[ticker])\
            and (datetime.datetime.today().weekday() <= 4) and ((datetime.datetime.now().hour >= int(trading_start_time_hour)) and\
            (datetime.datetime.now().hour <= int(trading_end_time_hour)))== True:
           print(f'{ticker} is above. Avg.Value = {stocks[ticker]}, Gain  = { round(float(ohlcv_data[ticker]["gain_pc"][-1]),2) } %, Gain for day ={ str(list(gain_day[ticker])) },above 21EWM = {ohlcv_data[ticker]["above_21ema_on"][-1]}, stacked = {ohlcv_data[ticker]["stacked_on"][-1]} ')
           temp = f'{ticker} is above. Avg.Value = {stocks[ticker]}, Gain  = { round(float(ohlcv_data[ticker]["gain_pc"][-1]),2) } %, Gain for day ={ str(list(gain_day[ticker])) } ,above 21EWM = {ohlcv_data[ticker]["above_21ema_on"][-1]}, stacked = {ohlcv_data[ticker]["stacked_on"][-1]} '
           
         
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
 
   
    
