# -*- coding: utf8 -*-
import os
import subprocess
import re
import json
from collections import Counter
import mysql.connector

BITCOIND_PATH = '/home/abrochec/blockchain/bitcoin-0.16.1'

cnx = mysql.connector.connect(user='root', password='Alexis2018!',host='localhost',database='miners') #10
cursor = cnx.cursor()

def getblockidfromdatabase():
    query=("SELECT blockid FROM `minersinfo` ORDER BY `blockid` DESC LIMIT 1")
    cursor.execute(query)
    blockid=cursor.fetchone()
    print(blockid[0])
    return blockid[0]

def getblocklenght():
    lenght = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockcount'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(lenght)
    return lenght

def getlistoftransactionidfromblock(block):
    listoftransactionid = [] #list storing the transaction ids
    jsonblock = json.loads(block) #20

    #Converting to json and getting the list of transaction
    listoftransactionid.append(jsonblock["tx"][0])
    return listoftransactionid

def getlistoftimefromblock(height):
    blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', str(height)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8')
    listoftime = [] #30
    jsonblock = json.loads(block) 
    listoftime=jsonblock["time"]
    return listoftime


def gettransactionid(height):
    blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', str(height)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8')
    transactionids = getlistoftransactionidfromblock(block)
    transactionid = transactionids[0] #40
    return transactionid

def getminerswallets(transactionid):
    rawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')
    decodedtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', rawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return decodedtransaction


def getVoutaddresses(decodedtransaction):
    #Converting the decoding transaction to json
    jsontransaction = json.loads(decodedtransaction)

    #Getting the correct addresses output from vout 50
    if ("nulldata" in jsontransaction["vout"][0]["scriptPubKey"]["type"]):
    	listofvoutaddresses.append(*jsontransaction["vout"][1]["scriptPubKey"]["addresses"])
    elif ("nulldata" in jsontransaction["vout"][0]["scriptPubKey"]["type"] and "nulldata" in jsontransaction["vout"][1]["scriptPubKey"]["type"]): #some block have no reward (like block 501726)
    	listofvoutaddresses.append(*jsontransaction["vout"][2]["scriptPubKey"]["addresses"])
    elif ("pubkey" in jsontransaction["vout"][0]["scriptPubKey"]["type"]):
    	listofvoutaddresses.append(*jsontransaction["vout"][0]["scriptPubKey"]["addresses"])
    else :
    	listofvoutaddresses.append("0")
    return listofvoutaddresses

# Function for add miners into the database  60
add_miners = ("INSERT INTO minersinfo " 
               "(blockid, date, wallet, transaction) "  # pas besoin de id car auto-incremente
               "VALUES (%s, %s, %s, %s)") 

# main part:
# delete = ("DELETE FROM minersinfo")
test=getblockidfromdatabase()
# cursor.execute(delete)
lenght = getblocklenght()
listofminers=[]
listoftime = []
listoftransaction=[]
listofvoutaddresses = [] #list of addresses of the output 70
listofelements = [] #list of elements in the Count function
for i in range(test,int(lenght)):
    listoftime.append(getlistoftimefromblock(i))
    transactionid=gettransactionid(i)
    listoftransaction.append(transactionid)
    decodedtransaction=getminerswallets(transactionid)
    listofminers=getVoutaddresses(decodedtransaction)
occurences=Counter(listofminers)
listofelements=list(occurences.elements())
count = 0

# cursor.execute("INSERT INTO minersinfo " "(blockid, date, wallet, transaction ) ""VALUES (0, 0, 0, 0)") #80

for i in range(0,int(lenght)-int(test)):
    count += 1
    id=test+i+1
    data_miners = (id, listoftime[i],listofminers[i],listoftransaction[i])
    cursor.execute(add_miners, data_miners) #add the element in "minerwallet" database
    if (count%1000==0):
    	cnx.commit()

# closing the database
cnx.commit()

cursor.close()
cnx.close()
