import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import csv
list_of_wanted_tables = [i for i in range(4, 14)]
url = 'https://wf.snekw.com/weapons-wiki'
resp = urlopen(url).read()
json_data = json.loads(resp)['data']['Weapons']

def filter_weapon(item):
	_item = {}
	_item['Name'] = item['Name']
	_item['Weapon Class'] = item['Type']
	_item['Mastery Rank'] = item['Mastery'] if 'Mastery' in item.keys() else 0 
	if 'Prime' in item['Name']:
		_item['Crafting Cost'] = 'Prime Parts'
	elif 'Cost' in item.keys():
		if 'Parts' in item['Cost'].keys():
			string = ''
			for resource in item['Cost']['Parts']:
				amount = resource['Count']
				name = resource['Name']
				string = string + f'{name} {amount}, '
			_item['Crafting Cost'] = string
	return _item


weapons = []
for weapon in json_data:
	weapons.append(filter_weapon(json_data[weapon]))

headers = weapons[0].keys()

with open('weapons.csv', 'w', newline='') as f:
	writer = csv.DictWriter(f , headers)
	writer.writeheader()
	for weapon in weapons:
		writer.writerow(weapon)
