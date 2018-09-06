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
        except:
            return
    elif cmd.startswith("/miete "):
        try:
            params = '+'.join(quote(cmd, safe='', encoding='iso-8859-1').split('%20')[1:])
            response = urlopen(puppuUrl + '?avainsana=' + params)
        except HTTPError as e:
            print("HTTP Error: " + str(e))
            return
        except:
            return
    else:
        return
    return BeautifulSoup(response, 'html.parser').find('p', {'class' : 'lause'}).text

def matchesOfDay(soup, url, day, message=""):
    matches = (soup.find(text=str(day)).parent.parent).findChildren('a', {'class' : 'a-reset block upcoming-match standard-box'})
    listOfMatches = []
    for match in matches:
        singleMatch = []
        time = match.find('div', {'class' : 'time'}).text
        singleMatch.append((datetime.datetime.strptime(time, '%H:%M') + datetime.timedelta(hours=1)).strftime('%H:%M'))
        if match.find('td', {'class' : 'placeholder-text-cell'}):
            singleMatch.append("TBD")
            singleMatch.append("TBD")
            singleMatch.append(match.find('td', {'class' : 'placeholder-text-cell'}).text)
        else:
            for team in match.findAll('div', {'class' : 'team'}):
                singleMatch.append(team.text)
            singleMatch.append(match.find('span', {'class' : 'event-name'}).text)
        singleMatch.append(match['href'])
        listOfMatches.append(singleMatch)
    for match in listOfMatches:
        message = "%s%s | %s vs %s\n[%s]\n%s%s\n\n" % (message, match[0], match[1], match[2], match[3], url, match[4])
    return message

def hltvMatches():
    url = "https://www.hltv.org"
    try:
        con = urlopen(Request(url + '/matches', headers={'User-Agent' : "Magic Browser"}))
    except HTTPError as e:
        print("HTTP Error: " + str(e))
        return
    except:
        return
    now = datetime.datetime.now()
    soup = BeautifulSoup(con, 'html.parser')
    message = matchesOfDay(soup, url, now.isoformat()[0:10])
    return matchesOfDay(soup, url, (now + datetime.timedelta(days=1)).isoformat()[0:10], message)
