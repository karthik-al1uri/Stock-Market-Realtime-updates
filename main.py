import requests
from twilio.rest import Client
import pandas as pd
import random



df = pd.read_csv('stocks.csv')
stock_names = []
company_names = []
for index, row in df.iterrows():
    stock_names.append(row['STOCK_NAME'])
    company_names.append(row['COMPANY_NAME'])

random_index = random.randint(0, len(stock_names) - 1)
STOCK_NAME = stock_names[random_index]
COMPANY_NAME = company_names[random_index]


API_KEY = "METO71VESI71HVHE"
NEWS_API_KEY = "2bf9075742f64c0397987c63e8c3bcdb"
TWILIO_SID = "AC627a4db481f42579fd8195811862140a"
TWILIO_AUTH_TOKEN = "546b2e8a7dd94a99ee823bb3ab11c61c"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_PARAM = {
    "function": "TIME_SERIES_DAILY" ,
    "symbol":  STOCK_NAME,
    "apikey": API_KEY,
}

response = requests.get(STOCK_ENDPOINT,params=STOCK_PARAM)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]


yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

daybefore_yesterday_data = data_list[1]
daybefore_yesterday_closing_price = daybefore_yesterday_data["4. close"]


difference = abs(float(yesterday_closing_price) - float(daybefore_yesterday_closing_price))


up_down = None
if difference >=0:
    up_down = "🔺"

else:
    up_down = "🔻"

percentage = round((difference/float(yesterday_closing_price)) *100)
if abs(percentage) > 0 :
    
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    
    
    articles_list = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {article['title']} \n Brief: {article['description']}" for article in articles[:3]]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in articles_list:
        message = client.messages.create(
            body = article,
            from_= "+12565738509",
            to = "+919676228226",
        )
    