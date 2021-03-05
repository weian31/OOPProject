import requests
from bs4 import BeautifulSoup
from datetime import date
import mysql.connector
import time
from decimal import Decimal


class Data:
      def __init__(coin,name,date,marketcap, volume,open,close):
          coin.name = name
          coin.date = date
          coin.marketcap = marketcap
          coin.volume = volume
          coin.open = open
          coin.close = close

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="F2814939p",
  database="DataProject"
)

CalculateTime = Decimal(time.perf_counter())

def sublink():
    
  output = []
  enddate = date.today().strftime("%Y-%m-%d")
  startdate = "2010-01-01"
  endwith = ["compare","trending","high_volume","all","recently_added"]
    
  request = requests.get('https://coingecko.com/',headers={'User-agent': 'Super Bot Power Level Over 9000'})

  soup = BeautifulSoup(request.content, 'html.parser')

  for match in soup.find_all('a', href=lambda value:value and value.startswith("/en/coins") and not value.endswith(tuple(endwith))): # Comment Link
            if "https://www.coingecko.com" + match['href'] + "/historical_data/sgd?end_date="+ enddate + "&start_date=" + startdate not in output:
                output.insert(0,"https://www.coingecko.com" + match['href'] + "/historical_data/sgd?end_date="+ enddate + "&start_date=" + startdate)

  return output
pass

def gethistoricaldataforallcoin():

  link = sublink()
  temp = []
  temp2 = []
  temp3 = []
  dataset =  []

  for position in range(len(link)-90): #change this to get the number of coins,Currently 10 coins
    
      request = requests.get(link[99-position],headers={'User-agent': 'Super Bot Power Level Over 9000'})

      temp3.insert(0,link[99-position].split("/")[5])

      soup = BeautifulSoup(request.content, 'html.parser')

      match = soup.find('table')
      
      for match in soup.find_all(attrs={"scope": 'row'}): # Comment Link
          temp.insert(len(temp),match.text)

      for match in soup.find_all("td",class_='text-center'): # Comment Link
          abc = match.get_text(strip=True)
          temp2.insert(len(temp),abc)

      inc =0;
      for x in range(len(temp)):
          dataset.insert(0,Data(temp3[0],temp[x],temp2[x+3+inc],temp2[x+2+inc][2:],temp2[x+1+inc],temp2[x+inc]))   
          inc += 3
    
  mycursor = mydb.cursor()
  sql = 'DELETE FROM CoinGeckoData'
  mycursor.execute(sql,'')  
  for x in range(len(dataset)):
    
    position = len(dataset) -1
    
    sql = 'INSERT INTO CoinGeckoData (Name, Date, MarketCap, Volume, Open, Close) VALUES (%s, %s, %s, %s, %s, %s)'
    val = (str(dataset[position-x].name),str(dataset[position-x].date),str(dataset[position-x].marketcap),str(dataset[position-x].volume),str(dataset[position-x].open),str(dataset[position-x].close))
    mycursor.execute(sql, val)

    mydb.commit()

gethistoricaldataforallcoin()
CalculateTime = Decimal(time.perf_counter()) - CalculateTime
print(str(CalculateTime) + " Seconds")