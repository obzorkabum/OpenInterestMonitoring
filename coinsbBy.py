signalcount={}  #сохраняет информацию по количеству сигналов по монетам, чистится в 00:00 по серверу ByBit
coin=[] #хранит список монет, которые будут мониторится

'''
так и не смог найти способ, как спарсить все монеты,
которые торгуются во фьючерсах ByBit, поэтому список писался в ручную :(
'''

def readCoins():
    f=open('coinName.txt')
    for line in f:
        tmp=line.strip('\n')
        coin.append(tmp)
        signalcount[tmp] = 0
    #return coin

