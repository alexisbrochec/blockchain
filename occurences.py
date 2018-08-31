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
cursor = cnx.cursor(buffered=True)

#change a value in seconde into a proper date
def secTodate(nombre):
	listdate=[]
	annee=divmod(nombre, (3600*24*365))
	month=divmod(annee[1], (3600*24*31))
	jour=divmod(month[1], (3600*24))
	heure=divmod(jour[1], 3600)
	minute=divmod(heure[1], 60)
	seconde=minute[1]
	print (nombre, "s = ", annee[0], "an(s)", month[0], "mois", jour[0], "jour(s)", heure[0], "heure(s)", minute[0], "minute(s)", seconde, "seconde(s)")
	listdate.append(annee[0])
	listdate.append(month[0])
	listdate.append(jour[0])
	listdate.append(heure[0])
	listdate.append(minute[0])
	listdate.append(seconde)
	return listdate

# main part:
dateinput=input ("enter a date in order to check the occurences of this week")
calculedateinput=int(dateinput)
print(secTodate(calculedateinput))
calcule=int(dateinput)+604800
weeks=0

#loop for 42 weeks
while weeks!=42 :
	listofoccurences=[]
	listofminers=[]
	#dateend is the date after a week, in second
	dateinput=str(calculedateinput)
	dateend=str(calcule)
	#Getting all the wallet from that week
	query=("SELECT wallet, COUNT(wallet) FROM  minersinfo WHERE date>"+dateinput+" and date<"+dateend+" GROUP BY wallet ORDER BY COUNT(wallet) DESC LIMIT 5")
	cursor.execute(query)
	listofminers=cursor.fetchall()
	print(listofminers)
	calculedateinput=calcule
	calcule+=6048000
	weeks+=1

cursor.close()
cnx.close()

