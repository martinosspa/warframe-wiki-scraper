import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import csv


url = 'https://warframe.fandom.com/wiki/Mod'
resp = urlopen(url)

soup = BeautifulSoup(resp, 'html.parser')
tables = soup.find_all('div', class_='tabbertab')


# remove special tables from 'tables' and add them to special_tables
special_tables = []
for _ in range(6):
	special_tables.append(tables.pop(len(tables) - 1))

# generate all headers from normal mod lists
all_headers = ['Type']
specific_headers = []
for table in tables:
	headers = table.text.split('\n\n')[1].split('\n')
	headers.remove('')
	if 'Polarity' in headers:
		headers.remove('Polarity')
	for h in headers:
		if not h in all_headers:
			# special case
			if not h == ' Description':
				all_headers.append(h)

	specific_headers.append(headers)

# mod handling
mods = []


# normal tables
for table_pos, table in enumerate(tables):
	title = tables[table_pos].attrs['title']
	#print(title)
	
	text = table.text.split('\n')
	text = list(filter(lambda info: not info == '', text))
	text = list(filter(lambda info: not info == ' ', text))
	header_size = len(specific_headers[table_pos])
	del text[0:header_size + 1]
	
	# filter out u2009
	text = [info.replace('\u2009', '') for info in text]

	# polarities for the table
	polarities = [pol.img.attrs['alt'].replace(' Pol', '') for pol in table.find_all('a', title='Polarity')]
	# special case
	if title == 'Melee':
		_special_case_pos = text.index('Focused Defense')
		text[_special_case_pos+1].join(text.pop(_special_case_pos+2))
	

	for info_pos in range(0, len(text), header_size):
		mod = {}
		mod['Type'] = title
		mod['Polarity'] = polarities[(info_pos // header_size)]
		for header_pos in range(header_size):
			header = specific_headers[table_pos][header_pos]
			# special case
			if header == ' Description':
				header = 'Description'
			mod[header] = text[info_pos + header_pos]
		mods.append(mod)

# augment tables

for table_pos, table in enumerate(special_tables):
	text = table.text.split('\n')
	text = list(filter(lambda info: not info == '', text))
	text = list(filter(lambda info: not info == ' ', text))
	text = [info.replace('\u2009', '') for info in text]
	del text[0]
	for item in text:
		print(item)
	# split based on volt 





all_headers.insert(2, 'Polarity')

#print(headers)
with open('mods.csv', 'w', encoding='utf-16', newline='') as f:
	writer = csv.DictWriter(f , all_headers)
	writer.writeheader()
	for mod in mods:
		writer.writerow(mod)
