import telepot
import time, re
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from telepot.loop import MessageLoop

class TgBot:
    def __init__(self):
        self.TOKEN = ""
        self.bot = telepot.Bot(self.TOKEN)
        self.options = ""
        self.puppuUrl = "http://puppulausegeneraattori.fi/"

    def run(self):
        try:
            self.options = BeautifulSoup(urlopen(self.puppuUrl), 'html.parser').findAll('option')
            while True:
                time.sleep(60)
        except HTTPError as e:
            print("Unable to fetch puppu options: " + str(e) + ". Exiting.")
            raise SystemExit
        except KeyboardInterrupt:
            print("\nExiting.")
            raise SystemExit

    def messageHandle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == "text":
            cmd = msg["text"]
            if cmd == "/ip":
                try:
                    message = "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8")
                except HTTPError as e:
                    print("HTTP Error: " + str(e))
                    return
                except:
                    return
            elif cmd.startswith("/miete"):
                if cmd == "/miete":
                    try:
                        response = urlopen(self.puppuUrl + 'aihe/' + self.options[randint(1,len(self.options)-1)]['value'])
                    except HTTPError as e:
                        print("HTTP Error: " + str(e))
                        return
                    except Exception:
                        return
                elif cmd.startswith("/miete "):
                    try:
                        params = '+'.join(quote(cmd, safe='', encoding='iso-8859-1').split('%20')[1:])
                        response = urlopen(self.puppuUrl + '?avainsana=' + params)
                    except HTTPError as e:
                        print("HTTP Error: " + str(e))
                        return
                    except Exception:
                        return
                else:
                    return
                message = BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text
            else:
                return
            try:
                self.bot.sendMessage(chat_id, message)
            except Exception as e:
                print("Failed sending message to chat: " + str(chat_id) + "\nReason: " + str(e))
                return

tgBot = TgBot()
MessageLoop(tgBot.bot, tgBot.messageHandle).run_as_thread()
tgBot.run()
