from random import random
from numpy.random import choice
from math import ceil

_base_stats = ['impact', 'puncture' ,'slash']
class Enemy:
	def __init__(self, level):
		h = 300 * (1 + (pow(level - 8, 2)) * 0.015)
		self.armor = 500 * (1 + pow(level - 8, 1.75) * 0.005)
		self.damage_reduction = 1 - (self.armor / (self.armor + 300))
		self.health = h * self.damage_reduction
	def __repr__(self):
		return str(self.health)


class Weapon:
	def __init__(self,
				impact=0,
				puncture=0,
				slash=0,
				cold=0,
				electricity=0,
				heat=0,
				toxin=0,
				blast=0,
				corrosive=0,
				gas=0,
				magnetic=0,
				radiation=0,
				viral=0,
				crit_chance=0,
				crit_multiplier=0,
				status_chance=0,
				fire_rate=0,
				clip_ammo=0,
				multishot=0,
				reload_time=0):

		self.damage_types = {
		'impact' : impact,
		'puncture' : puncture,
		'slash' : slash,
		'cold' : cold,
		'electricity' : electricity,
		'heat' : heat,
		'toxin' : toxin,
		'blast' : blast,
		'corrosive' : corrosive,
		'gas' : gas,
		'magnetic' : magnetic,
		'radiation' : radiation,
		'viral' : viral
		}

		self.damage_distributions = {
		'impact' : impact * 4,
		'puncture' : puncture * 4,
		'slash' : slash * 4,
		'cold' : cold,
		'electricity' : electricity,
		'heat' : heat,
		'toxin' : toxin,
		'blast' : blast,
		'corrosive' : corrosive,
		'gas' : gas,
		'magnetic' : magnetic,
		'radiation' : radiation,
		'viral' : viral
		}


		# base elements * 4 + others status
		self.total_proportional_damage = sum([self.damage_distributions[p] for p in self.damage_distributions])
		self.proportial_distributions = {p : self.damage_distributions[p] / self.total_proportional_damage for p in self.damage_distributions}
		self.total_damage = sum([self.damage_types[p] for p in self.damage_types])
		
		self.crit_chance = crit_chance
		self.crit_multiplier = crit_multiplier
		self.status_chance = status_chance/100
		self.fire_rate = fire_rate
		self.clip_ammo = clip_ammo
		self.multishot = multishot
		self.reload_time = reload_time

	def simulate_hit(self, enemy):
		status_roll = random()



		if self.status_chance >= status_roll:
			# status proc
			proc = choice([p for p in self.damage_distributions], 
							1, 
							p = [self.proportial_distributions[p] for p in self.proportial_distributions])
			proc = proc[0]

			#print(proc)
			
			if proc == 'slash':
				pass
		enemy.health = enemy.health - self.total_damage

		sum_ = sum(self.damage_types[k] for k in _base_stats)
		q = sum_ / 16

		for base_element in _base_stats:
			
			d = ceil(self.damage_types[base_element] / q)*q
			#print(self.damage_types[base_element])
			#print(q)
			print(d)
		#damage_to_enemy = 300/()
		#DM=300300+AR(1−AM)(1+AM)(1+HM)








weapon = Weapon(status_chance=10, impact=30, puncture=30, slash=40)

#print(weapon.total_damage)
enemy = Enemy(100)
#print(weapon.total_damage * enemy.damage_reduction)
weapon.simulate_hit(enemy)
#print(enemy)






#https://warframe.fandom.com/wiki/Status_Effect