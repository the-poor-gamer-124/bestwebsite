import requests
import urllib.parse
import random
import time
import re
from bs4 import BeautifulSoup
import config
import json
import util
import globals

def gen_template(title, content):
 template_local = str(globals.template)
 template_local = template_local.replace("{{pagetitle}}", title)
 description = BeautifulSoup(content[:160], "lxml").text
 description = re.sub(r'\W+', ' ', description)
 template_local = template_local.replace("{{pagedesc}}", description)
 template_local = template_local.replace("{{content}}", content)
 template_local = template_local.replace("{{cloakscript}}", util.cloak_script())
 return template_local

def make_page(ftitle,fdata):
 global globals
 ftitle = ftitle.replace('"', "")
 page = gen_template(ftitle, fdata)
 fname = ""
 for i in ftitle:
  if i == " ":
   fname += "_"
  elif i.isalnum():
   fname += i
 with open(f"generated/{fname}.html", "wb") as file:
  file.write(page.encode())
  globals.art_full.append({"fname":fname,"ftit":ftitle})

def mkindex():
 links = ""
 links += "<ul>"
 for i in globals.art_full:
  fname = i["fname"]
  ftit = i["ftit"]
  links += f"<li><a href=\"{fname}.html\">{ftit}</a></li>"
 links += "</ul>"
 ftitle,fdata = util.get_results_from_page(config.config["mainsubject"])
 index = gen_template(config.config["sitename"], fdata+links)
 with open("generated/index.html", "wb") as file:
  file.write(index.encode())

