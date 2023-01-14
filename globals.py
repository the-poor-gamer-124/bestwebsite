art_full = []

syns = {}

with open("skeleton/template.html", "rb") as file:
 template = file.read().decode(errors="ignore")

with open("skeleton/subjects.txt", "rb") as file: 
 subjects = file.read().decode(errors="ignore").splitlines()
 
with open("skeleton/links.txt", "rb") as file: 
 links = file.read().decode(errors="ignore").splitlines()

with open("data/stops.txt", "r") as file:
 stopwords = file.read().splitlines()
