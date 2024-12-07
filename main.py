import telebot
import bylib as by
import coinsbBy as coBy
import threading
import schedule
import time
import math

'''
Краткий ликбес по вопросу
"А на кой эта программа вообще нужна?"

Объясняю:

Данная программа позволяет мониторить всплеск открытого интереса - вливания новых денег в монету,
что позволяет сделать определенные выводы по дальнейшему развитию курса монеты.
Если монета "на дне", открытый интерес растёт - она растёт (вместе с этим должен быть и 
денежный рост монеты в этом промежутке)
Если монета "на пике", открытый интерес растёт и цена падает - ждите падение.

Так же этот вопрос вы можете изучить самостоятельно, о применении открытого интереса в своём торговом плане
'''


bot = telebot.TeleBot('') #BotFather в помощь
idChat='' #свой не буду оставлять)
session = by.openSession()
coBy.readCoins()




def cleanDiary():
  bot.send_message(idChat,"Очистка сессии завершена! Настал новый торговый день.")
  coBy.signalcount.clear()
  coBy.readCoins()


def fun():
  threading.Timer(300.0, fun).start()  # Перезапуск через 5 минут
  by.prinTimeRegion(by.getServTimeUnix())
  for i in coBy.coin:
    openinteresDic =by.getCoinInteres(session,i)
    interestList = openinteresDic.get('result').get('list')
    lastInd = int(len(interestList[0])) - 1

    opLast = int(math.trunc(float(interestList[0].get('openInterest'))))

    if opLast>0:
      rez=by.solveOpPercent(interestList[0],interestList[lastInd])
      perc=100-rez
      if perc>=5 or perc<=-5: #можно изменить по желанию
        coBy.signalcount[i] += 1
        difer=by.getCoinDifference(session,i)
        bot.send_message(idChat, str(by.getInfo(i,perc,difer)))
    clearJob() #отмена задач, т.к. бот запускается один раз и самовыполняется через 5 минут, см. первую строчку функции

def clearJob():
  schedule.cancel_job(job2)
  schedule.cancel_job(job3)
  schedule.cancel_job(job4)
  schedule.cancel_job(job5)
  schedule.cancel_job(job6)
  schedule.cancel_job(job7)
  schedule.cancel_job(job8)
  schedule.cancel_job(job9)
  schedule.cancel_job(job10)
  schedule.cancel_job(job11)
  schedule.cancel_job(job12)
  schedule.cancel_job(job13)


if __name__ == '__main__':
  #задержка в 10 секунд, чтобы данные с api точно были на сервере.
  job1=schedule.every().day.at("03:10").do(cleanDiary)
  job2 = schedule.every().hour.at("00:10").do(fun)
  job3 = schedule.every().hour.at("05:10").do(fun)
  job4 = schedule.every().hour.at("10:10").do(fun)
  job5 = schedule.every().hour.at("15:10").do(fun)
  job6 = schedule.every().hour.at("20:10").do(fun)
  job7 = schedule.every().hour.at("25:10").do(fun)
  job8 = schedule.every().hour.at("30:10").do(fun)
  job9 = schedule.every().hour.at("35:10").do(fun)
  job10 = schedule.every().hour.at("40:10").do(fun)
  job11 = schedule.every().hour.at("45:10").do(fun)
  job12 = schedule.every().hour.at("50:10").do(fun)
  job13 = schedule.every().hour.at("55:10").do(fun)
  #fun()
  while True:
    schedule.run_pending()
    time.sleep(1)
    #bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
    #вышестоящая команда не нужна, если бот работает самостоятельно, что он и делает)




