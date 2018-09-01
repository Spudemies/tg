import telepot
import time
import re
from random import randint
from telepot.loop import MessageLoop
from urllib.request import urlopen


TOKEN = ""
bot = telepot.Bot(TOKEN)
chat_id = ""

def MessageHandle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
#        print(msg)
        if msg["text"] == "/ip":
            try:
                bot.sendMessage(chat_id, "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
            except urllib.HTTPError as e:
                bot.sendMessage(chat_id, "Error: " + e.code)
            except:
                pass
        elif msg["text"] == "/miete":
            subjects = ['Yleinen', 'Tietotekniikka', 'Politiikka', 'Talous', 'Yritysmaailma', 'Oikeustiede', 'Opiskelijaelama', 'Monikulttuurisuus', 'Tulevaisuusselonteko']
            try:
                response = urlopen('http://puppulausegeneraattori.fi/aihe/' + subjects[randint(0, 8)])
                for line in response:
                    line = line.decode('cp1252')
                    if '<P CLASS="lause">' in line:
                        line = re.sub('<.*?>', '', line)
#                        print(line)
                        bot.sendMessage(chat_id, line)
                        break
            except urllib.HTTPError as e:
                bot.sendMessage(chat_id, "Error: " + e.code)
            except:
                pass

MessageLoop(bot, MessageHandle).run_as_thread()
while True:
   # response = urlopen('http://puppulausegeneraattori.fi/aihe/Politiikka')
   # for line in response:
   #      line = line.decode('cp1252')
   #      if '<P CLASS="lause">' in line:
   #            line = re.sub('<.*?>', '', line)
   #            print(line)
               #          bot.sendMessage(chat_id, line)
   #            break

    #print(urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
    time.sleep(5)
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

