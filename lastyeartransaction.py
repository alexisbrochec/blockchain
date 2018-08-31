# -*- coding: utf8 -*-
import os
from time import *
import subprocess
import re
import json
from collections import Counter
import mysql.connector

BITCOIND_PATH = '/home/abrochec/blockchain/bitcoin-0.16.1'

cnx = mysql.connector.connect(user='root', password='Alexis2018!',host='localhost',database='miners') #10
cursor = cnx.cursor()


#part of the code that take last block timestamp
def get_lastblocktimestamp():
	listoftime=[]
	lenght = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockcount'], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', lenght], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	listoftime = [] #30
	jsonblock = json.loads(block)
	listoftime=jsonblock["time"]
	return listoftime

def get_blocktimestamp(lenght):
	blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', lenght], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	listoftime = [] #30
	jsonblock = json.loads(block)
	listoftime=jsonblock["time"]
	return listoftime

def get_listoftransactionidfromblock(block):
	listoftransactionid = [] #list storing the transaction ids 
	jsonblock = json.loads(block) #20
	#Converting to json and getting the list of transaction
	if len(jsonblock["tx"])>1: 
		for i in range(1, len(jsonblock["tx"])):
			listoftransactionid.append(jsonblock["tx"][i])
	else:
		listoftransactionid=[0]
	return listoftransactionid


def get_blockidfromblocktimestamp(time):
	yearprior=time-1
	str_yearprior=str(yearprior)
	query=("SELECT blockid FROM  minersinfo WHERE date>"+str_yearprior+" ORDER BY blockid ASC LIMIT 1")
	cursor.execute(query)
	yearpriorblockid=cursor.fetchall()
	return yearpriorblockid[0]

def get_transaction(height):
	transactionids=[]
	blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', str(height)], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	transactionids = get_listoftransactionidfromblock(block) 
	return transactionids

def get_decodedtransaction(transactionid):
	rawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	decodedtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', rawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	return decodedtransaction 

query=("INSERT INTO transactions VALUES (%s ,%s ,%s, %s)")


def get_Vinaddresses(transactionid, timestamp):
	decodedtransaction=[]
	rawtransaction=[]
	rawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction',transactionid , ' 1'], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	# print(rawtransaction)
	jsonblock = json.loads(rawtransaction)
	del(jsonblock["vout"])
	del(jsonblock["hex"])
	#print(jsonblock)
	# decodedtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', rawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8') 
	# print(decodedtransaction)
	listofvinaddresses = [] #list of addresses of the input of the current transaction
	listofvinposition = [] #list of the position of the vin in  the previous transaction
	listofvintransaction =[] #list of the previous transaction
	#Converting the decoding transaction to json
	# jsontransaction = json.loads(decodedtransaction)
	#appel de getVin
	if 'txid' in jsonblock['vin'][0]:
		for j in range(0, len(jsonblock["vin"])):
			listofvintransaction.append(jsonblock["vin"][j]["txid"])
	if 'vout' in jsonblock['vin'][0]:
		for j in range(0, len(jsonblock["vin"])):
			listofvinposition.append(jsonblock["vin"][j]["vout"])
		listofinputtransaction=','.join(listofvintransaction)
		listofinputposition=','.join(str(elem) for elem in listofvinposition)
		if len(listofinputtransaction)<50000:
			data_transaction=(listofinputtransaction, transactionid, listofinputposition, timestamp)
			cursor.execute(query, data_transaction)
			# listofvinaddresses.append(get_Vinaddress(listofvintransaction[j],listofvinposition[j]))
			cnx.commit()
		else :
			print("list of input transaction too big")
	else:
		data_transaction=(0,transactionid,0,timestamp)
		cursor.execute(query, data_transaction)
	# return listofvinaddresses


#Recovery of the financial input (with the previous transaction and it's position in that transaction)

def get_Vinaddress(transactionid, voutindex):
	vinrawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')
	vindecodedrawtransaction = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', vinrawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8')
	jsonvin = json.loads(vindecodedrawtransaction)

	#Recovery of every addresses of output of this "old" transaction
	vinaddress = jsonvin['vout'][voutindex]['scriptPubKey']['addresses']
	return vinaddress


# main part:
lenght = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockcount'], stdout=subprocess.PIPE).stdout.decode('utf-8')
lastblocktimestamp=get_lastblocktimestamp()
print(lastblocktimestamp)
print(lenght)
DatabaseHeight=("SELECT timestamp FROM transactions ORDER BY timestamp DESC LIMIT 1" )
cursor.execute(DatabaseHeight)
blocktimestamp=cursor.fetchall()
if not blocktimestamp:
	blockheight=70000
else:
	height=get_blockidfromblocktimestamp(blocktimestamp[0][0])
	calcul=int(height[0])+1
	blockheight=calcul
while blockheight!=lenght:
	listoftransaction=[]
	listoftransaction=get_transaction(str(blockheight))
	listoftransactions=listoftransaction[0]
	if listoftransaction[0]!=0:
		blocktimestamp=get_blocktimestamp(str(blockheight))
		for i in listoftransaction:
			indice=str(i)
			get_Vinaddresses(i, blocktimestamp)
	blockheight+=1

cursor.close()

cnx.close()
