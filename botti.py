import telepot
import time, re
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from telepot.loop import MessageLoop

TOKEN = ""
bot = telepot.Bot(TOKEN)

def run():
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        raise SystemExit

def MessageHandle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        txt = msg["text"]
        if txt == "/ip":
            try:
                bot.sendMessage(chat_id, "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass
        elif txt == "/miete":
            try:
                options = BeautifulSoup(urlopen('http://puppulausegeneraattori.fi/'), 'html.parser').findAll('option')
                response = urlopen('http://puppulausegeneraattori.fi/aihe/' + options[randint(1,len(options)-1)]['value'])
                bot.sendMessage(chat_id, BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text)
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass
        elif txt.startswith("/miete "):
            try:
                params = '+'.join(quote(txt, safe='', encoding='iso-8859-1').split('%20')[1:])
                response = urlopen('http://puppulausegeneraattori.fi/?avainsana=' + params)
                bot.sendMessage(chat_id, BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text)
            except HTTPError as e:
                print("HTTP Error: " + e)
            except:
                pass

MessageLoop(bot, MessageHandle).run_as_thread()
run()
