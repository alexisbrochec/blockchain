# -*- coding: utf8 -*-
import os
import subprocess
import re
import json

BITCOIND_PATH = '/home/abrochec/blockchain/bitcoin-0.16.1'

#function used to ask the user for the block height///////////////
def askheight():
    height = input ("Please enter the height of the block :")
    return height

def getblockhashfromheight(height):
    blockhash = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblockhash', str(height)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return blockhash

def getblockfromblockhash(blockhash):
    block = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return block

def getlistoftransactionidfromblock(block):
    listoftransactionid = [] #list storing the transaction ids
    jsonblock = json.loads(block)

    #Converting to json and getting the list of transaction
    for transactionids in jsonblock['tx']:
        listoftransactionid.append(transactionids)

    #For test only
    for transaction in enumerate(listoftransactionid):
        print(transaction)

    return listoftransactionid

#Ask the transaction needing to be looked into//////////////

def getrawtransactionfromtransactionid(transactionid):
    #getting the rawtransaction from the txid
    rawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return rawtransaction

def decoderawtransactionfromrawtransaction(rawtransaction):
    #decoding the rawtransaction
    decodedtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', rawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return decodedtransaction

def getVoutaddresses(decodedtransaction):
    listofvoutaddresses = [] #list of addresses of the output
    #Converting the decoding transaction to json
    jsontransaction = json.loads(decodedtransaction)

    #Getting the addresses output from vout
    for i in range(0, len(jsontransaction["vout"])):
        listofvoutaddresses.append(jsontransaction["vout"][i]["scriptPubKey"]["addresses"])
    print("list of output wallets :")
    print(listofvoutaddresses)
    return listofvoutaddresses


#Recovery of the financial input (with the previous transaction and it's position in that transaction)
def getVinaddress(transactionid, voutindex):
    vinrawtransaction= subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')
    vindecodedrawtransaction = subprocess.run([BITCOIND_PATH + '/bin/bitcoin-cli', 'decoderawtransaction', vinrawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8')
    jsonvin = json.loads(vindecodedrawtransaction)

    #Recovery of every addresses of output of this "old" transaction
    vinaddress = jsonvin['vout'][voutindex]['scriptPubKey']['addresses']
    return vinaddress

def getVinaddresses(decodedtransaction):
    listofvinaddresses = [] #list of addresses of the input of the current transaction
    listofvinposition = [] #list of the position of the vin in  the previous transaction
    listofvintransaction =[] #list of the previous transaction

    #Converting the decoding transaction to json
    jsontransaction = json.loads(decodedtransaction)

    #appel de getVin
    for j in range(0, len(jsontransaction["vin"])):
        listofvintransaction.append(jsontransaction["vin"][j]["txid"])
    for j in range(0, len(jsontransaction["vin"])):
        listofvinposition.append(jsontransaction["vin"][j]["vout"])
        listofvinaddresses.append(getVinaddress(listofvintransaction[j],listofvinposition[j]))
    print("list of Input wallets :")
    print(listofvinaddresses)
    return listofvinaddresses

def getValuesOut(decodedtransaction):
    listofvaluesout = [] #list of values of bitcoin transfert out
    
    jsontransaction = json.loads(decodedtransaction)

    #Getting the values output from vout
    for i in range(0, len(jsontransaction["vout"])):
        listofvaluesout.append(jsontransaction["vout"][i]["value"])
    print("list of values per wallets :")
    print(listofvaluesout)
    return listofvaluesout
