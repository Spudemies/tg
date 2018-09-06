import telepot
import time, re, datetime
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from urllib.request import Request
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
            elif cmd == "/hltv matches":
                url = "https://www.hltv.org"
                con = urlopen(Request(url + '/matches', headers={'User-Agent' : "Magic Browser"}))
                soup = BeautifulSoup(con, 'html.parser').find(text=str((datetime.datetime.now()).isoformat())[0:10]).parent.parent
                matches = soup.findChildren('a', {'class' : 'a-reset block upcoming-match standard-box'})
                a = []
                for match in matches:
                    m = []
                    time = match.find('div', {'class' : 'time'}).text
                    m.append((datetime.datetime.strptime(time, '%H:%M') + datetime.timedelta(hours=1)).strftime('%H:%M'))
                    for team in match.findAll('div', {'class' : 'team'}):
                        m.append(team.text)
                    m.append(match.find('span', {'class' : 'event-name'}).text)
                    m.append(match['href'])
                    a.append(m)
                message = ""
                for match in a:
                    message = "%s%s | %s vs %s\n[%s]\n%s%s\n\n" % (message, match[0], match[1], match[2], match[3], url, match[4])
            else:
                return
            try:
                self.bot.sendMessage(chat_id, message, disable_web_page_preview=True, disable_notification=True)
            except Exception as e:
                print("Failed sending message to chat: " + str(chat_id) + "\nReason: " + str(e))
                return

tgBot = TgBot()
MessageLoop(tgBot.bot, tgBot.messageHandle).run_as_thread()
tgBot.run()
