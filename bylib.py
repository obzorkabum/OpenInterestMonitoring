import math
import requests
import ast
from pybit.unified_trading import HTTP
import time
import coinsbBy as coBy

'''
Важно!
используйте свой api с свойством "только чтение" - эта программа не создаёт автоматические позиции, но
вам вряд-ли захочется увидеть ваш баланс с тремя нулями, если ваш api попадёт не в те руки :(

так же тут лежат "дебажные" команды, которые выводят информацию в консоль,
которые точно не понадобятся в вашем боте для личного(командного) пользования
'''

BYBIT_API_KEY = "" #оставляю этот момент на вас (регистрируйтесь на Bybit и создавайте свой api)
BYBIT_API_SECRET = "" #оставляю этот момент на вас (регистрируйтесь на Bybit и создавайте свой api)

timeRequestion = ["5min","15min","30min","1h","4h","1d"]
def openSession():
    return HTTP(testnet=False,api_key=BYBIT_API_KEY,api_secret=BYBIT_API_SECRET)

def getCoinInteres(session,symbolCoin="BTCUSD",tradeTime=timeRequestion[0],categoryTrade="linear"):
 #   return session.get_open_interest(category=categoryTrade,symbol=symbolCoin,intervalTime=tradeTime,startTime=(getServTime()-900)*1000,endTime=getServTime()*1000,limit=200)

    return session.get_open_interest(category=categoryTrade,symbol=symbolCoin,intervalTime=tradeTime,limit=200)

def getCoinDifference(session,symbolCoin="BTCUSD",categoryTrade="linear",TimeInterval=5):
    difference=[]
    info= session.get_kline(
        category=categoryTrade,
        symbol=symbolCoin,
        interval=TimeInterval
    )
    price = info.get('result').get('list')

    Pastcline = price[1]
    openPrice = float(Pastcline[1])  # цена открытия
    closePrice = float(Pastcline[4])  # цена закрытия
    difference.append(round((closePrice - openPrice), 3))
    difference.append(round(100-((openPrice/closePrice)*100), 2))
    return difference

def getTimeUnix(interestlist):
    return  int(interestlist.get('timestamp'))/1000


def prinTimeRegion(Time):
    print(time.strftime('%d.%m.%Y %H:%M',time.gmtime(Time+10800)))

def getTimeRegion(Time):
    return str(time.strftime('%d.%m.%Y %H:%M',time.gmtime(Time+10800)))

def printTimeServer(Time):
    print(time.strftime('%d.%m.%Y %H:%M', time.gmtime(Time)))

def getTimeServer(Time):
    return(time.strftime('%d.%m.%Y %H:%M', time.gmtime(Time)))

def getServTimeUnix()->int:
    url = "https://api-testnet.bybit.com/v5/market/time"
    payload={}
    headers = {}
    reqTime = requests.request("GET", url, headers=headers, data=payload)
    gateTime=ast.literal_eval(reqTime.text)
    return int(gateTime.get('result').get('timeSecond'))

def solveOpPercent(firstTime,lastTime):
    opFirts = int(math.trunc(float(firstTime.get('openInterest'))))
    opLast = int(math.trunc(float(lastTime.get('openInterest'))))
    rez = (float(opLast/opFirts)) * 100
    return rez


def printInfo(i,perc):
    print("Уведомление по монете "+ i +" - "+str(coBy.signalcount[i])+"\nОткрытый интерес монеты " + i + " составил = " + str(round(perc, 2)) + "%\nhttps://www.coinglass.com/tv/ru/Bybit_"+i)


def getInfo(i,perc,diff):
    simbolOI=''
    simbolPr=''
    if perc>=0:
        simbolOI='↗'
    else:
        simbolOI='↘'
    if diff[0]>=0:
        simbolPr = '↗'
    else:
        simbolPr = '↘'

    return str("Уведомление по монете "+ i +" - "+str(coBy.signalcount[i])+"\nОткрытый интерес монеты " + i + " составил = " + str(round(perc, 2)) + "% "+simbolOI+"\nИзменение цены "+i+" cоставило = "+str(diff[0])+"$ ("+str(diff[1])+"%) "+simbolPr+"\nhttps://www.coinglass.com/tv/ru/Bybit_"+i)

def checkTimeToRun(timeUnix):
     time.gmtime(timeUnix+10800)