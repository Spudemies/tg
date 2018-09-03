import telepot
import time
import re
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from telepot.loop import MessageLoop

TOKEN = ""
bot = telepot.Bot(TOKEN)

def MessageHandle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        if msg["text"] == "/ip":
            try:
                bot.sendMessage(chat_id, "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass
        elif msg["text"] == "/miete":
            options = BeautifulSoup(urlopen('http://puppulausegeneraattori.fi/'), 'html.parser').findAll('option')
            try:
                response = urlopen('http://puppulausegeneraattori.fi/aihe/' + options[randint(1,len(options)-1)]['value'])
                bot.sendMessage(chat_id, BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text)
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass
        elif msg["text"].startswith("/miete "):
            try:
                params = '+'.join(quote(msg["text"], safe='').split('%20')[1:])
                response = urlopen('http://puppulausegeneraattori.fi/?avainsana=' + params)
                bot.sendMessage(chat_id, BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text)
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass

MessageLoop(bot, MessageHandle).run_as_thread()
while True:
    time.sleep(60)
