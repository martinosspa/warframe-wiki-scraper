import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import csv

url = 'https://warframe.fandom.com/wiki/Mod'
resp = urlopen(url).read()

soup = BeautifulSoup(resp, 'html.parser')
#print(soup.findAll('a'))
a = soup.find_all('table')
for pos, r in enumerate(a):
	with open(f'{pos}.txt', 'w', encoding='utf-16') as f:
		f.write(r.text)


'''
with open('test.csv', 'w') as f:
	writer = csv.DictWriter(f , headers)
	writer.writeheader()
	for item in mods:
		print(item)
		writer.writerow(item)
'''