import time
import requests
from datetime import date
from datetime import datetime
from datetime import timedelta

# Info on STOCK Act, requiring members of Congress to disclose trades
    #https://www.congress.gov/112/plaws/publ105/PLAW-112publ105.htm



rep_running_total = 0
disclosure_running_total = 0
current_price = 0



def disclosure_performance(disclosure_date, ticker):
    ''' Returns stock performance from the disclosure date to today '''

    global disclosure_running_total

    url="https://api.polygon.io/v1/open-close/"+ticker+"/"+disclosure_date+"?adjusted=true&apiKey=gxYIocKQw3bc7usXJxEdplxdivNWRNjF"
    response = requests.get(url)
    day_info = response.json()
    
    if 'close' in day_info:

        buy_price = day_info["close"]

        performance = (current_price-buy_price)/buy_price * 100

        disclosure_running_total += performance

        performance_result = str(performance)[0:7]+'%'

        return performance_result



def rep_performance(rep_date, ticker):
    ''' Returns stock performance from the date represenatatives's bought to today '''

    global current_price
    global rep_running_total

    url="https://api.polygon.io/v1/open-close/"+ticker+"/"+rep_date+"?adjusted=true&apiKey=gxYIocKQw3bc7usXJxEdplxdivNWRNjF"
    response = requests.get(url)
    day_info = response.json()
    
    if 'close' in day_info:

        buy_price = day_info["close"]

        yesterday_date = date.today() - timedelta(days = 1)

        url2="https://api.polygon.io/v1/open-close/"+str(ticker)+"/"+str(yesterday_date)+"?adjusted=true&apiKey=gxYIocKQw3bc7usXJxEdplxdivNWRNjF"
        response = requests.get(url2)
        day_info = response.json()
        x=2
        while 'close' not in day_info:
                yesterday_date = date.today() - timedelta(days = x)
                url3 = "https://api.polygon.io/v1/open-close/"+ticker+"/"+x_days_before+"?adjusted=true&apiKey=gxYIocKQw3bc7usXJxEdplxdivNWRNjF"
                response = requests.get(url3)
                day_info = response.json()
                x+=1
                time.sleep(30)
        x=2

        current_price = day_info["close"]

        performance = (current_price-buy_price)/buy_price * 100

        rep_running_total += performance

        performance_result = str(performance)[0:7]+'%'

        return performance_result

    

''' Request aggregate list of Represenatatives' trades and call above functions to find each trade's return and the running total '''
response = requests.get("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json")
full_list = response.json()

for trade in full_list:
        if trade['ticker'] != '--':
            if trade['type'] == 'purchase':
                print(trade)
                date_list = trade['transaction_date'].split('-')
                rep_date = date_list[0]+'-'+date_list[1]+'-'+date_list[2]
                date_list2 = trade['disclosure_date'].split('/')
                disclosure_date = date_list2[2]+'-'+date_list2[0]+'-'+date_list2[1]
                ticker = trade['ticker']

                try:

                    print('-----------------------------------------------------')
                    print('Rep Trade Performance for', ticker, 'from', rep_date + ':', rep_performance(rep_date, ticker))
                    time.sleep(30)
                    print('Disclosure Trade Performance for', ticker, 'from', disclosure_date + ':', disclosure_performance(disclosure_date, ticker))

                except:
                    ('################################ fail')

                print('Represenatatives Running Total:', str(rep_running_total)[0:5]+'%')
                print('Disclosure Running Total:', str(disclosure_running_total)[0:5]+'%')


                print('-----------------------------------------------------')

                time.sleep(61)