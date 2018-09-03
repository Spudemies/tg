import telepot
import time
import re
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from telepot.loop import MessageLoop

TOKEN = ""
bot = telepot.Bot(TOKEN)
chat_id = ""

def MessageHandle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        if msg["text"] == "/ip":
            try:
                bot.sendMessage(chat_id, "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
            except urllib.HTTPError as e:
                bot.sendMessage(chat_id, "Error: " + e.code)
            except:
                pass
        elif msg["text"] == "/miete":
            options = BeautifulSoup(urlopen('http://puppulausegeneraattori.fi/'), 'html.parser').findAll('option')
            try:
                response = urlopen('http://puppulausegeneraattori.fi/aihe/' + options[randint(1,len(options)-1)]['value'])
                bot.sendMessage(chat_id, BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text)
            except urllib.HTTPError as e:
                bot.sendMessage(chat_id, "Error: " + e.code)
            except:
                pass

MessageLoop(bot, MessageHandle).run_as_thread()
while True:
    time.sleep(60)
#print("Looking for changes in external IP address every 60 seconds...")
#print("Listening for commands...")
#
#current_ip = None
#while current_ip is None:
#        try:
#                current_ip = urlopen("http://ip.42.pl/raw").read()
#        except:
#                print("No internet connection")
#
#while True:
#        old_ip = current_ip
#        try:
#                current_ip = urlopen("http://ip.42.pl/raw").read()
#                if old_ip != current_ip:
#                        bot.sendMessage(chat_id, "New IP: " + current_ip.decode("utf-8"))
#                        print("New IP found: " + current_ip.decode("utf-8"))
#                #else:
#                #       print("No changes.")
#        except:
#                print("No internet connection")
#        time.sleep(60)
