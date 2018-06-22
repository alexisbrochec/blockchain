# -*- coding: utf8 -*-
import os
import subprocess
import re
import json


listoftransactionid = [] #list storing the transaction ids
listofvoutaddresses = [] #list of addresses of the output
listofvin = [] #list of addresses of the input of the current transaction
listofvinposition = [] #list of the position of the vin in  the previous transaction
listofvintransaction =[] #list of the previous transaction

#function used to ask the user for the block height
def askheight():
    height = input ("Please enter the height of the block :")
    return height

#Recovery of the financial input (with the previous transaction and it's position in that transaction)
def getVin(transactionid, voutindex):
    vinrawtransaction= subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')
    vindecodedrawtransaction = subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'decoderawtransaction', vinrawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8') 
    jsonvin = json.loads(vindecodedrawtransaction)

    #Recovery of every addresses of output of this "old" transaction
    vinaddress = jsonvin['vout'][voutindex]['scriptPubKey']['addresses']
    return vinaddress

if __name__ == "__main__":
 entering = input("continue: otherinput than b")
    
 while entering!='b':
    blockheight = askheight()
    blockhash = subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'getblockhash', blockheight], stdout=subprocess.PIPE).stdout.decode('utf-8')
    block = subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'getblock', blockhash], stdout=subprocess.PIPE).stdout.decode('utf-8')
    jsonblock = json.loads(block)

    #Converting to json and getting the list of transaction
    for transactionids in jsonblock['tx']:
        listoftransactionid.append(transactionids)

    #For test only
    for transaction in enumerate(listoftransactionid):
        print(transaction)

    indexoftransaction = input("Which transaction should be looked into ?")


    #getting the transaction txid
    transactionid = listoftransactionid[int(indexoftransaction)]

    #getting the rawtransaction from the txid
    rawtransaction= subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'getrawtransaction', transactionid], stdout=subprocess.PIPE).stdout.decode('utf-8')

    #decoding the rawtransaction
    decodedtransaction= subprocess.run(['./bitcoin-0.16.1/bin/bitcoin-cli', 'decoderawtransaction', rawtransaction.strip()], stdout=subprocess.PIPE).stdout.decode('utf-8')

    #Converting the decoding transaction to json
    jsontransaction = json.loads(decodedtransaction)

    #Getting the addresses output from vout
    for i in range(0, len(jsontransaction["vout"])):
        listofvoutaddresses.append(jsontransaction["vout"][i]["scriptPubKey"]["addresses"])
    print("list of output wallets :")
    print(listofvoutaddresses)

    #appel de getVin
    for j in range(0, len(jsontransaction["vin"])):
        listofvintransaction.append(jsontransaction["vin"][j]["txid"])
    for j in range(0, len(jsontransaction["vin"])):
        listofvinposition.append(jsontransaction["vin"][j]["vout"])
        listofvin.append(getVin(listofvintransaction[j],listofvinposition[j]))
    print("list of Input wallets :")
    print(listofvin)
    entering = input ("continue ? (if not input b)")

pass
