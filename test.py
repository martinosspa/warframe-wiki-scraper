import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import csv
url = 'https://warframe.fandom.com/wiki/Mod'
resp = urlopen(url).read()

soup = BeautifulSoup(resp, 'html.parser')
mods = []

tables = soup.find_all('div', class_='tabbertab')
for _ in range(6):
	tables.pop(len(tables) - 1)

for table in tables:
	info = table.find_all('a', title='Polarity')
	for pol in info:
		print(pol.img.attrs['alt'].replace(' Pol', ''))



#print(headers)
'''
with open('mods.csv', 'w', encoding='utf-16', newline='') as f:
	writer = csv.DictWriter(f , headers)
	writer.writeheader()
	for mod in mods:
		writer.writerow(mod)
'''