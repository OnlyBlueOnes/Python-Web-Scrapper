#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests, re
import pandas as pd
import time
import pymongo


# In[2]:


from pymongo import MongoClient


# In[3]:


#polaczenie z db
klient = MongoClient("mongodb+srv://admin:admin@cluster0-rranm.mongodb.net/test?retryWrites=true&w=majority")


# In[4]:


#definicja db
db = klient['wyniki']

#definicja kolekcji
daneProduktow=db.dywany


# In[5]:


#pobieranie zawartosci stron
from bs4 import BeautifulSoup
strony=[]

strony.append(
    requests.get(
        "https://jysk.pl/do-domu/dywany"
    ))
time.sleep(1.5)

for i in range(0,3):
    strony.append(
        requests.get(
            "https://www.ikea.com/pl/pl/cat/dywany-10653/?page="+str(i)
        ))
    time.sleep(1.5)


# In[6]:


#definiujemy tablice, w ktorych bd przechowywane dane
tabela_cen = []
tabela_nazw = []
tabela_wymiarow = []
tabela_sklepow = ['Ikea','Jysk'] 


# In[8]:


#definicje znacznikow
for strona in strony: 
    soup = BeautifulSoup(strona.text, 'html.parser')
    cena = soup.findAll('span', attrs={'class':['product-price','product-compact__price__value']})
    nazwa = soup.findAll('span', attrs={'class':['product-name','product-compact__name']})
    wymiar = soup.findAll('span', attrs={'class':['product-name','product-compact__description']})

    #definicja slow kluczowych
    key_word = '80x'
    key_word_2 = '70x'

    #stworzenie pliku CSV i wykuszanie danych w petlach dla kazdej strony osobno
    f=open('fileDyw.csv','a+', encoding='UTF-8')
    
    if "ikea" in strona.text.lower():
        for i in range(len(nazwa)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_nazw.append(nazwa[i].text.strip())
            else:
                continue
        for i in range(len(cena)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_cen.append(cena[i].text.strip())
            else:
                continue
        for i in range(len(wymiar)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_wymiarow.append(wymiar[i].text.strip())
            else:
                continue
            
            f.write(tabela_sklepow[0]+";"+
                    nazwa[i].text.strip()+";"+
                    cena[i].text.strip()+";"+
                    wymiar[i].text.strip()+"\n")
            
    elif "jysk" in strona.text.lower():
        for i in range(len(nazwa)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_nazw.append(nazwa[i].text.split(" ")[1].strip())
            else:
                continue
        for i in range(len(cena)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_cen.append(cena[i].text.split(" ")[2].strip())
            else:
                continue
        for i in range(len(wymiar)):
            if key_word in wymiar[i].text.strip() or key_word_2 in wymiar[i].text.strip():
                tabela_wymiarow.append(wymiar[i].text.split(" ")[2].strip())
            else:
                continue

            f.write(tabela_sklepow[1]+";"+
                    nazwa[i].text.split(" ")[1].strip()+";"+
                    cena[i].text.split(" ")[2].strip()+";"+
                    wymiar[i].text.split(" ")[2].strip()+" cm"+"\n")
    f.close()


# In[9]:


#import danych z csv do db
# 1- odczyt danych zapisanych w csv
plik=pd.read_csv('fileDyw.csv',
               index_col=False,
               names=['sklep','nazwa','cena','wymiary'],
               delimiter=";",
               encoding='UTF-8')
plik


# In[10]:


# 2- dodanie zarartosci csv do kolekcji w db

for index, row in plik.iterrows():
    dywan={
        'sklep':row['sklep'],
        'nazwa':row['nazwa'],
        'cena':row['cena'],
        'wymiary':row['wymiary']
    }
    rezultat=daneProduktow.insert_one(dywan)
    print("Dywan ",row['nazwa'],"ze sklepu ",row['sklep']," wstawiono do db")
print("Koniec listy!")


# In[18]:


#wyswietlenie zawartosci kolekcji

dywany=daneProduktow.find({})
for d in dywany:
    print(d['_id'],d['nazwa'],d['cena'],d['wymiary'])


# In[11]:


def gdzieNaZakupy():
    print('Znaleziono '+str(plik['sklep'].count())+' pasujacych wyników')
    ikea = len(plik[plik['sklep']=='Ikea'])
    jysk = len(plik[plik['sklep']=='Jysk'])
    print('W Ikei znajdziedz ',ikea,'dywanow, w Jysku ',jysk,'\n\nWniosek:')
    
    if ikea > jysk:
        print('Idz na zakupy do Ikei. Tam masz wiekszy wybor.')
    else:
        print('Idz na zakupy do Jysku. Tam masz wiekszy wybor.')


# In[12]:


gdzieNaZakupy()


# In[ ]:




