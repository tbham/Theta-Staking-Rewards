import requests as req
import csv
import threading as thr
import queue as qu
from datetime import *
from decimal import *

thread_count = 8
threads = []
tx = 0
limit = 50
wei = 1000000000000000000
pages: int()

def Theta(wallet):
    global thread_count
    global pages
    csv_row = []
    tx_hash: str
    timestamp: int
    thetawei: int
    tfuelwei: int

    URL = "https://explorer.thetatoken.org:8443/api/accounttx/" + str(wallet) + "?type=" + str(tx) + "&pageNumber=1&limitNumber=" + str(limit) + "&isEqualType=true"
    res = req.get(URL)
    pages = int(res.json()['totalPageNumber'])
    
    print("Requesting page 1 of %i" %(pages))
    print("Request URL: %s" %(URL))
    print("Response code: %i" %(res.status_code))
    print("Response time: %i ms" %(res.elapsed.total_seconds()*1000))
    print()

    if res.status_code == 200:
        for x in res.json()['body']:
            for y in x['data']['outputs']:
                if y['address'] == wallet:

                    tx_hash = x['hash']
                    timestamp = datetime.fromtimestamp(int(x['timestamp']))
                    thetawei = Decimal(int(y['coins']['thetawei'])/wei)
                    tfuelwei = Decimal(int(y['coins']['tfuelwei'])/wei)

                    csv_row = [tx_hash, timestamp, thetawei, tfuelwei]
                    print("Queued: %s" %csv_row)
                    queue.put(csv_row)

    for i in range(1, thread_count + 1):
        x = thr.Thread(target=ThetaWorker, args=(wallet, i))
        threads.append(x)
        x.start()
    
    for i in threads:
        i.join()

    ToCSV()
    
def ThetaWorker(wallet, thread):
    global thread_count
    global pages
    global queue
    csv_row = []
    tx_hash: str
    timestamp: int
    thetawei: int
    tfuelwei: int

    for i in range(1 + thread, pages + 1, thread_count):
        URL = "https://explorer.thetatoken.org:8443/api/accounttx/" + str(wallet) + "?type=" + str(tx) + "&pageNumber=" + str(i) + "&limitNumber=" + str(limit) + "&isEqualType=true"
        res = req.get(URL)
        #print("Thread: %i, Requesting page %i of %i" %(thread,i,pages))
        #print("Thread: %i, Request URL: %s" %(thread,URL))
        #print("Thread: %i, Response code: %i" %(thread,res.status_code))
        #print("Thread: %i, Response time: %i ms" %(thread,(res.elapsed.total_seconds()*1000)))

        print("Requesting page %i of %i" %(i,pages))
        print("Request URL: %s" %(URL))
        print("Response code: %i" %(res.status_code))
        print("Response time: %i ms" %(res.elapsed.total_seconds()*1000))

        if res.status_code == 200:
            for x in res.json()['body']:
                for y in x['data']['outputs']:
                    if y['address'] == wallet:

                        tx_hash = x['hash']
                        timestamp = datetime.fromtimestamp(int(x['timestamp']))
                        thetawei = Decimal(int(y['coins']['thetawei'])/wei)
                        tfuelwei = Decimal(int(y['coins']['tfuelwei'])/wei)

                        csv_row = [tx_hash, timestamp, thetawei, tfuelwei]
                        print("Queued: %s" %(csv_row))
                        queue.put(csv_row)
            print()

def ToCSV():   
    with open("tx.csv","w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["tx_hash", "timestamp","thetawei", "tfuelwei"])

        while queue.qsize() > 0:
            tx_item = queue.get()
            wr.writerow(tx_item)
            queue.task_done()
            print("Writing: %s" %tx_item)

        f.close()

print()
print("--------------------------------------------------------")
print("Theta Explorer API - Staking Rewards")
print("--------------------------------------------------------")
print()
print("Public Wallet Address (Not Mnemonic Phrase): ")
wallet = input().lower()
print()

queue = qu.Queue()

Theta(wallet)