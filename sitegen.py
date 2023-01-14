import sys
import requests
from bs4 import BeautifulSoup
import urllib
import random
import threading
import base64
import json
import config
import generator
import globals
import util

def fuck_process():
 try:
  ftitle,fdata = util.get_results_from_page(random.choice(globals.subjects))
  print("Adding {}".format(ftitle))
  generator.make_page(ftitle,fdata)
 except Exception as error:
  print(error)

def fthread():
 global config
 while config.config["articlenum"] > 0:
  try:
   fuck_process()
   config.config["articlenum"] -= 1
  except Exception as error:
   print(error)

threads = []
for i in range(config.config["threadnum"]):
 t=threading.Thread(target=fthread)
 t.start()
 threads.append(t)
for t in threads:
 t.join()
generator.mkindex()
