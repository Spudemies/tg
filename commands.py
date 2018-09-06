import time, datetime
from bs4 import BeautifulSoup
from random import randint
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.parse import quote

def ip():
    try:
        return "Current IP: " + urlopen("http://ip.42.pl/raw").read().decode("utf-8")
    except HTTPError as e:
        print("HTTP Error: " + str(e))
        return
    except:
        return

def puppulause(cmd, options, puppuUrl):
    if cmd == "/miete":
        try:
            response = urlopen(puppuUrl + 'aihe/' + options[randint(1,len(options)-1)]['value'])
        except HTTPError as e:
            print("HTTP Error: " + str(e))
            return
        except Exception:
            return
    elif cmd.startswith("/miete "):
        try:
            params = '+'.join(quote(cmd, safe='', encoding='iso-8859-1').split('%20')[1:])
            response = urlopen(puppuUrl + '?avainsana=' + params)
        except HTTPError as e:
            print("HTTP Error: " + str(e))
            return
        except Exception:
            return
    else:
        return
    return BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text

def hltv_matches():
    url = "https://www.hltv.org"
    try:
        con = urlopen(Request(url + '/matches', headers={'User-Agent' : "Magic Browser"}))
    except HTTPError as e:
        print("HTTP Error: " + str(e))
        return
    except Exception:
        return
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
    return message
