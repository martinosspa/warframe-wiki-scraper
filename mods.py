import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import csv
import asyncio
import aiohttp
import grequests
base_url = 'https://warframe.fandom.com/wiki'
url = 'https://warframe.fandom.com/wiki/Mod'

mod_exceptions = ['Astral Autopsy', 'Scorch', 'Seeker', 'Coolant Leak', 'Sanctuary', 'Antitoxin']

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
		h = 'Category' if h == 'Subcategory' else h
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

	# filter out all spaces at the start of info
	text = [item.replace(' ', '', 1) if item.startswith(' ') else item for item in text]

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
			entry_text = text[info_pos + header_pos]

			header = 'Description' if header == ' Description' else header

			# exilus
			entry_split = entry_text.split(', ')
			if 'Exilus' in entry_split:
				if header == 'Category':
					entry_split.pop(0)
					mod['Subcategory'] = ''.join(entry_split)
				if title == 'Warframe':
					mod['Type'] = 'Exilus'
			else:
				# default haddling
				mod[header] = entry_text
		mods.append(mod)




# augment tables
'''
for table_pos, table in enumerate(special_tables):
	text = table.text.split('\n')
	text = list(filter(lambda info: not info == '', text))
	text = list(filter(lambda info: not info == ' ', text))
	text = [info.replace('\u2009', '') for info in text]
	#del text[0]
	print(text)
	# split based on volt 

'''



all_headers.insert(3, 'Drain')
all_headers.insert(2, 'Polarity')
all_headers.insert(4, 'Subcategory')

# sorts mods based on type
mods = sorted(mods, key=lambda mod: mod['Type'])

# filter out pvp mods
for mod in mods:
	if 'Exclusive to PvP' in mod['Description']:
		mods.remove(mod)

# gets polarities
reqs = [grequests.get(f'{base_url}/{item_name}') for item_name in [mod['Name'].replace(' ', '_') for mod in mods]]
responses = resp = grequests.map(reqs)

for resp_pos, resp in enumerate(responses):
	if not mods[resp_pos]['Name'] in mod_exceptions and not mods[resp_pos]['Type'] == 'Stance':
		s = BeautifulSoup(resp.text, 'html.parser')
		t = s.find('table', 'emodtable')
		text_ = list(filter(lambda info: not info == '', t.text.split('\n')))
		#aura_multiplier = -1 if mods[resp_pos]['Type'] == 'Aura' else 1

		if mods[resp_pos]['Type'] == 'Aura':
			mods[resp_pos]['Drain'] = int(text_[-1][-1]) * -1
		else:
			mods[resp_pos]['Drain'] = text_[-1][-1]
	else:
		mods[resp_pos]['Drain'] = 'Error'
# write csv
with open('mods.csv', 'w', encoding='utf-16', newline='') as f:
	writer = csv.DictWriter(f , all_headers)
	writer.writeheader()
	for mod in mods:
		writer.writerow(mod)
