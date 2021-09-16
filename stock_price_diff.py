from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import investpy
import datetime


def get_last_price(stock_no):
    """
    Get the last price of the stock
    Args:
        stock_no (str): Code number for stock in KLSE eg: AIRASIA: 5099.jsp

    Returns:
        Last Price of the stock
    """
    klse_url = "https://klse.i3investor.com/servlets/stk/"
    url = klse_url+stock_no
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'lxml')
    news_table = html.find(id='stockhdr')
    for row in news_table.findAll('td'):
        try:
            float(row.text)
            return float(row.text)
        except:
            pass


def get_previous_price(stock, date):
    """
    Get the closing date price of the given date provided
    Args:
        stock (str): stock name in investpy
        date (str): date with format 'dd/mm/yyyy'

    Returns:
        Last price of the given date
    """
    day, month, year = date.split('/')
    next_day = str(int(day)+1)+'/'+month+'/'+year
    price_list = investpy.get_stock_historical_data(stock=stock, country='Malaysia', from_date=date, to_date=next_day)['Close'].to_list()
    return price_list[0]


if __name__ == '__main__':
    stock_no = '5099.jsp'   #AirAsia
    stock_symbol = 'aira'
    date = '18/03/2020'
    prediction = '0.20'
    last_price = get_last_price(stock_no)
    # print(last_price)
    previous_price =get_previous_price(stock_symbol, date)
    # print(previous_price)
    price_diff = last_price - previous_price
    if float(prediction) > price_diff:
        print(f'Wrong Prediction\n Prediction: {prediction}\n date prediction of {date} with stock price {previous_price} \nLast Price: {last_price} \n Price diff: {price_diff}')
    else:
        print(f'Correct Prediction\n Prediction: {prediction}\n date prediction: {date} with stock price {previous_price} \nLast Price: {last_price} \n Price diff: {price_diff}')
# news_tables = {}
#
# for ticker in tickers:
#     url = klse_url + ticker
#     req = Request(url=url, headers={'user-agent': 'my-app'})
#     response = urlopen(req)
#
#     html = BeautifulSoup(response, 'html')
#     news_table = html.find(id='nbTable')
#     news_tables[ticker] = news_table