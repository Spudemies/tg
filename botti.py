import telepot
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from telepot.loop import MessageLoop
from commands import ip, puppulause, hltvMatches, fetchWhiteList

class TgBot:
    def __init__(self):
        self.TOKEN = ""
        self.bot = telepot.Bot(self.TOKEN)
        self.options = ""
        self.whitelist = []

    def run(self):
        try:
            self.options = BeautifulSoup(urlopen("http://puppulausegeneraattori.fi/"), 'html.parser').findAll('option')
            self.whitelist = fetchWhiteList()
            self.whitelist.append("TBD")
            while True:
                time.sleep(60)
        except HTTPError as e:
            print("Unable to fetch puppu options: " + str(e) + "\nExiting.")
            raise SystemExit
        except KeyboardInterrupt:
            print("\nExiting.")
            raise SystemExit

    def messageHandle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == "text":
            cmd = msg["text"]
            if cmd == "/ip":
                message = ip()
                if not message: return
            elif cmd.startswith("/miete"):
                message = puppulause(cmd, self.options, "http://puppulausegeneraattori.fi/")
                if not message: return
            elif cmd == "/matches":
                message = hltvMatches(self.whitelist)
                if not message: return
            else: return
            try:
                while len(message):
                    self.bot.sendMessage(chat_id, message[:4095], disable_web_page_preview=True, disable_notification=True)
                    message = message[4096:]
                    time.sleep(1)
            except Exception as e:
                print("Failed sending message to chat: " + str(chat_id) + "\nReason: " + str(e))
                return

tgBot = TgBot()
MessageLoop(tgBot.bot, tgBot.messageHandle).run_as_thread()
tgBot.run()
