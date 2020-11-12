import MyDictionary, random, math, ImageHandling, Conventions
from Main import Item, Weapon, Armour


def randomise_tier(current_tier, fortune, t1_c_u_t2 = 5, t1_c_u_t3 = 2, t2_c_d_t1 = 65, t2_c_u_t3 = 5, t3_c_d_t2 = 35, t3_c_d_t1 = 50):
	# Rare chance to get a different tier weapon 
	new_tier = current_tier
	if(current_tier == 2):
		# Define probability for upgrade/downgrade scaling with the player's fortune stat
		chance_to_downgrade = t2_c_d_t1 - math.ceil(fortune / 5); # Percent
		chance_to_upgrade = t2_c_u_t3 * math.ceil(fortune / 10); # Percent
		upgrade_roll = random.uniform(0,101)
		if(upgrade_roll <= chance_to_upgrade): # Upgrade
			new_tier = 3;
		elif(upgrade_roll > chance_to_upgrade and upgrade_roll < (chance_to_downgrade + chance_to_upgrade)): # Downgrade
			new_tier = 1;
	elif(current_tier == 1):
		chance_to_upgrade_to_2 = t1_c_u_t2 * math.ceil(fortune / 10); # Percent 
		chance_to_upgrade_to_3 = t1_c_u_t3 * math.ceil(fortune / 10); # Percent
		upgrade_roll = random.uniform(0,101)

		if(upgrade_roll <= chance_to_upgrade_to_3): # Upgrade to 3
			new_tier = 3;
		elif(upgrade_roll <= chance_to_upgrade_to_2): # Upgrade to 2
			new_tier = 2;
	elif(current_tier == 3):
		chance_to_downgrade_to_2 = t3_c_d_t2 - math.ceil(fortune / 5); # Percent
		chance_to_downgrade_to_1 = t3_c_d_t1 - math.ceil(fortune / 5); # Percent
		downgrade_roll = random.uniform(0,101)

		if(downgrade_roll <= chance_to_downgrade_to_1): # Downgrade to 1
			new_tier = 1;
		elif(downgrade_roll > chance_to_downgrade_to_1 and downgrade_roll < (chance_to_downgrade_to_1 + chance_to_downgrade_to_2)): # Downgrade to 2
			new_tier = 2;

	return new_tier;




def differentiate_weapon(weapon_name, weapon_type, tier, weapon_damage, weapon_accuracy):

	def small_mag():
		return random.randrange(2*tier, 3*tier)
	def medium_mag():
		return random.randrange(3*tier, 5*tier)
	def large_mag():
		return random.randrange(5*tier, 10*tier)
	# Add unique characteristics to different types of weapons
	# Set a default value for ammo 
	ammo_type = "9mm"
	shots_per_turn = 1;
	# General weapons
	if("shotgun" in weapon_name.lower()): 	           			# If random weapon is a shotgun 
		magazine_capacity = 2 * tier;		           			# Make the magazine capacity a multiple of 2
		shots_per_turn = math.ceil(tier / 2)           			# Have the gun be 1 shot burst for tier 1 and 2 then 2 shot burst for tier 3
		weapon_damage = round(weapon_damage * 1.35)    			# Increase damage by 35%
		weapon_accuracy = round(weapon_accuracy * 0.9) 			# Decrease acuracy by 10%
		ammo_type = random.choice(["12g slug", "12g buckshot"])
	elif("revolver" in weapon_name.lower()):   # If random weapon is a type of hand gun
		magazine_capacity = random.randrange(4, 6 * tier)		# Set magazine capacity to a specified range scaling on tier
		shots_per_turn = random.randrange(1, tier + 1) 			# Set shots per turn between 1 and tier 
		ammo_type = ".338 Magnum"
	elif("rifle" in weapon_name.lower()):						# If weapon is a rifle
		magazine_capacity = random.randrange(3, tier * 4 + 1)   # Set magazine capacity between 3 and tier * 4
		weapon_damage = round(weapon_damage * 1.2)				# Increase damage by 20%
		weapon_accuracy = round(weapon_accuracy * 1.15)			# Increase accuracy by 15%
		shots_per_turn = 1										# Rifles always only shoot once per turn
		ammo_type = random.choice([".22LR", "6.5 Creedmoor", "7.62.X39mm"])
	# Tier 1 weapons
	elif("steam cannon" in weapon_name.lower()):
		magazine_capacity = small_mag()	
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "20cm^3 water"
	elif("pistol" in weapon_name.lower()):
		magazine_capacity = small_mag()	
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "9mm"
	elif("boomerang" in weapon_name.lower()):
		magazine_capacity = 0;
		weapon_damage = round(weapon_damage * 1.25)
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "boomerang"
	elif("hunting-bow" in weapon_name.lower()):
		magazine_capacity = 0;
		weapon_accuracy = round(weapon_accuracy * 0.9)
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "arrow"
	elif("slingshot" in weapon_name.lower()):
		magazine_capacity = random.randrange(5*tier, 10*tier)	
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "rock"
	elif("musket" in weapon_name.lower()):
		magazine_capacity = 1;	
		weapon_damage = round(weapon_damage * 1.3) 
		shots_per_turn = 1			
		ammo_type = "Lead ball"
	elif("nail-gun" in weapon_name.lower()):
		magazine_capacity = medium_mag();	
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		ammo_type = "12D nail"

	# Tier 2 Weapons
	elif("sub-machine gun" in weapon_name.lower()):
		weapon_damage = round(weapon_damage * 0.8);
		shots_per_turn = round(2, 2*tier)
		magazine_capacity = large_mag()	
		ammo_type = "9mm para"
	if("fusion rifle" in weapon_name.lower()):
		ammo_type = "hydrogen"
		shots_per_turn = random.randrange(1, 1 + round(tier / 2 + 0.5)) # 1-2
	elif("hand-cannon" in weapon_name.lower()):
		magazine_capacity = small_mag()	
		shots_per_turn = random.randrange(1, 1 + math.ceil(tier / 2))			# Random shots per round based off tier
		ammo_type = "50cal"
	elif("crossbow" in weapon_name.lower()):
		magazine_capacity = 1
		shots_per_turn = 1			# Random shots per round based off tier
		weapon_damage = round(weapon_damage * 1.3)
		weapon_accuracy = round(weapon_accuracy * 1.25)
		ammo_type = "Crossbow bolt"
	elif("blunderbuss" in weapon_name.lower()):
		magazine_capacity = small_mag()
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier
		weapon_accuracy = round(weapon_accuracy * 1.25)
		ammo_type = "Lead ball"
	elif("sawed-off" in weapon_name.lower()):
		magazine_capacity = small_mag()
		shots_per_turn = 2
		ammo_type = "12g buckshot"

	# Tier 3 weapons
	elif("rocket launcher" in weapon_name.lower()):
		magazine_capacity = 1;
		shots_per_turn = 1
		weapon_damage = (weapon_damage * 1.75)
		ammo_type = "Fat man"
	elif("gatling gun" in weapon_name.lower()):
		magazine_capacity = medium_mag()
		weapon_accuracy = round(weapon_accuracy * 0.8)
		shots_per_turn = random.randrange(2, tier*2)
		weapon_damage = round(weapon_damage * .75)
		ammo_type = ".50"
	elif("rotary cannon" in weapon_name.lower()):
		magazine_capacity = large_mag()
		weapon_accuracy = round(weapon_accuracy * 0.7)
		shots_per_turn = random.randrange(3, tier*3)
		weapon_damage = round(weapon_damage * .6)
		ammo_type = ".45"
	elif("rail gun" in weapon_name.lower()):
		magazine_capacity = medium_mag()
		weapon_accuracy = round(weapon_accuracy * 0.8)
		shots_per_turn = random.randrange(1, tier + 1)
		weapon_damage = round(weapon_damage * 1.2)
		ammo_type = "SABOT spear"
	elif("laser rifle" in weapon_name.lower()):
		magazine_capacity = medium_mag()
		weapon_accuracy = round(weapon_accuracy * 1.1)
		shots_per_turn = random.randrange(1, tier)
		ammo_type = "Deuterium fluoride"
	elif("coil gun" in weapon_name.lower()):
		magazine_capacity = medium_mag()
		weapon_accuracy = round(weapon_accuracy * 1.2)
		shots_per_turn = random.randrange(1, tier*3 + 1)
		weapon_damage = round(weapon_damage * 1.35)
		ammo_type = "Fe core"
	elif("particle-beam gun" in weapon_name.lower()):
		magazine_capacity = large_mag()
		ammo_type = "Atom"
	elif("bolt action rifle" in weapon_name.lower()):
		magazine_capacity = small_mag()
		weapon_accuracy = round(weapon_accuracy * 1.4)
		shots_per_turn = 1
		weapon_damage = round(weapon_damage * 1.5)
		ammo_type = "50 cal"
	elif("combat shotgun" in weapon_name.lower()):
		magazine_capacity = small_mag()
		weapon_accuracy = round(weapon_accuracy * 0.7)
		shots_per_turn = random.randrange(1, tier)
		weapon_damage = round(weapon_damage * 1.6)
		ammo_type = "8g flachette"
	elif("machine gun" in weapon_name.lower()):
		magazine_capacity = large_mag()
		ammo_type = ".227"
	elif("t-shirt cannon" in weapon_name.lower()):
		magazine_capacity = large_mag()
		weapon_accuracy = round(weapon_accuracy * 0.5)
		shots_per_turn = 1;
		weapon_damage = round(weapon_damage * 1.7)
		ammo_type = "T-shirt"
	elif("flamethrower" in weapon_name.lower()):
		magazine_capacity = small_mag()
		shots_per_turn = 1
		weapon_damage = round(weapon_damage * 1.2)
		ammo_type = "Jet fuel"


	if(weapon_type == "melee"):	  			   # If weapon is a melee weapon
		magazine_capacity = 0;	  			   # Unlimited capacity (No reloading)
		shots_per_turn = math.ceil(tier / 2)   # Have the weapon hit once for tier 1 and 2 then twice for tier 3

	return weapon_name, weapon_type, magazine_capacity, shots_per_turn, weapon_damage, weapon_accuracy, ammo_type;


def generate_loot(weapon_quantity = 1, armour_quantity = 1, item_quantity = 1, game_progression = 1, fortune = 1, tier = 1, merchant = False):
	# This function is used to get loot for the 'loot' encounter in the main file
	# initialise weapon loots 
	baguettes = ((math.log(game_progression + 1) ** 6) / 0.2) + 20;
	baguettes = round(baguettes * random.uniform(0.4, 1))
	if(weapon_quantity > 0):
		weapon_loot = {

		}

		for i in range(weapon_quantity):
			# Create a new tier based off of loot parameters (we want loot to be better than enemy drops as they are more rare)
			loot_tier = randomise_tier(tier, fortune, t1_c_u_t2 = 50, t1_c_u_t3 = 10, t2_c_d_t1 = 15, t2_c_u_t3 = 35, t3_c_d_t1 = 5, t3_c_d_t2 = 25)
			# Create weapon
			loot_weapon = create_weapon(game_progression, loot_tier, fortune)
			loot_weapon.value *= 1 + (merchant * 5)
			# Add weapon to loot
			weapon_loot.update({loot_weapon:1})
	else: 
		weapon_loot = None;

	if(armour_quantity > 0):
		armour_loot = {

		}

		# Create a new tier based off of loot parameters (we want loot to be better than enemy drops as they are more rare)
		loot_tier = randomise_tier(tier, fortune, t1_c_u_t2 = 50, t1_c_u_t3 = 10, t2_c_d_t1 = 15, t2_c_u_t3 = 35, t3_c_d_t1 = 5, t3_c_d_t2 = 25)
		# Define function for armour amount then divide it up into armour pieces below
		if(tier == 1):
			armour_amount = random.randrange(7, round(15 + game_progression / 3 ))  
		elif(tier == 2):
			armour_amount = random.randrange(12, round(24 + game_progression / 4 ))
		else:
			armour_amount = random.randrange(20, round(32 + game_progression / 5 ))
		
		# Create armour 
		loot_armour = create_armour(game_progression, loot_tier, fortune, armour_amount, armour_quantity)
		for individual_armour in loot_armour:
			individual_armour.value *= 1 + (merchant * 5)
			armour_loot.update({individual_armour:1})

	else:
		armour_loot = None;

	if(item_quantity > 0):
		temp_item_loot = {
		
		}
		# Define items that the loot can contain
		items_by_tier = [															
				[Item("stimpak"), Item("Armour Piercing Rounds")], 											
				[Item("stimpak"), Item("gene_synthesiser"), Item("Armour Piercing Rounds"), Item("Concussion Rounds")],				
				[Item("stimpak"), Item("gene_synthesiser"), Item("Armour Piercing Rounds"), Item("Concussion Rounds")]					
				]	

		for i in range(item_quantity):
			
			# Create a new tier based off of loot parameters (we want loot to be better than enemy drops as they are more rare)
			loot_tier = randomise_tier(tier, fortune, t1_c_u_t2 = 50, t1_c_u_t3 = 10, t2_c_d_t1 = 15, t2_c_u_t3 = 35, t3_c_d_t1 = 5, t3_c_d_t2 = 25)
			
			# Get a random item from the items array
			item_to_add = random.choice(items_by_tier[loot_tier - 1])
			# Add the item to the loot inventory
			temp_item_loot.update({item_to_add:1})	

		# Loop through all items that have been added to item inventory and append their names to an array (Getting duplicates)
		item_instances = []
		for key in temp_item_loot:
			item_instances.append(key.name)
		item_loot = {

		}
		#print(item_instances)
		# Merge duplicates into one item
		for key in temp_item_loot:
			
			# get the total amount of this particular item to add
			instances_of_item = item_instances.count(key.name)
			
			if(instances_of_item > 1):
				# Add the item
				item_loot.update({key:instances_of_item})
				# Remove all instances of the item from array
				item_instances = Conventions.remove_values_from_list(item_instances, key.name)
			elif(key.name in item_instances):
				# Add item
				item_loot.update({key:instances_of_item})

	else:
		item_loot = None;



	return weapon_loot, armour_loot, item_loot, baguettes

# def generate_merchant_loot();


def create_weapon(game_progression, tier, fortune):
	# Generate weapon parameters
	weapon_type_choices = ("melee", "ranged")	

	# Allow for a rare chance of a different tiered weapon
	tier = randomise_tier(tier, fortune)

	weapon_type_decider = random.randrange(0,2) 											   # Generate random number from 0-1
	weapon_name = MyDictionary.get_weapon_name(weapon_type_choices[weapon_type_decider], tier) # Use MyDictionary function to get a random name for the weapon

	weapon_type = weapon_type_choices[weapon_type_decider]									   # Decide if weapon is melee or ranged using random number 
	weapon_damage = math.ceil((game_progression**(math.e/3.2) + 12) * (random.uniform(1 - 0.25/tier, 1+0.2*tier) ) ) # Function to scale weapon damage with game progression 	

	# Determine crit chance for weapon
	base_weapon_crit_chance = []

	for p in range(1,7):	#Populate array with 6 low crit chance options
		base_weapon_crit_chance.append(p * tier + random.randrange(0, round(game_progression / 3) + 1) )

	for j in range(7,10):	#Populate array with 3 medium crit chance options
		base_weapon_crit_chance.append(j * 2 * tier + random.randrange(0,round(game_progression / 3) + 1) )

	# Add a single high crit option to array (low chance)  
	base_weapon_crit_chance.append((j + 1) * 3 * tier + random.randrange(0,round(game_progression / 3) + 1) )

	weapon_crit_chance = random.choice(base_weapon_crit_chance)	

	# Determine accuracy

	if(tier == 1):
		weapon_accuracy = random.randrange(40, 80)
	elif(tier == 2):
		weapon_accuracy = random.randrange(55, 88)
	else:
		weapon_accuracy = random.randrange(72, 96)


	# Increase damage based off of tier
	if(tier == 2):
		weapon_damage *= 1.15;
	elif(tier == 3):
		weapon_damage *= 1.35;

	# Differentiate weapon based upon weapon name 
	weapon_name, weapon_type, magazine_capacity, shots_per_turn, weapon_damage, weapon_accuracy, ammo_type = differentiate_weapon(weapon_name, weapon_type, tier, weapon_damage, weapon_accuracy)

	# Determine weight of weapon
	weapon_weight = random.randrange(1, 3*tier)

	# Cap accuracy at 100%
	if(weapon_accuracy >= 95):
		weapon_accuracy = 95;		

	# Determine the approximate amount of wear for the weapon to endure every time it is fired
	weapon_wear = random.randrange(3,10)
	if(weapon_wear >= 6):
		weapon_wear = random.randrange(3, weapon_wear)

	# Determine the approximate value of the weapon when selling it at a merchant
	weapon_value = random.randrange(int(3 * ((game_progression + 1) / 4)) * (tier > 1) + 1, int(15 * ((game_progression + 1) / 4) )) * tier;

	weapon_damage = math.floor(weapon_damage)
	# Generate weapon
	random_weapon = Weapon(weapon_name, weapon_type, weapon_damage, weapon_crit_chance, weapon_accuracy, magazine_capacity, shots_per_turn, weapon_weight, tier, weapon_wear, ammo_type, weapon_value)
	#print("Name:",random_weapon.name, "\n", "weapon_type:",random_weapon.weapon_type, "\n", "weapon_damage:",random_weapon.damage, "\n", "weapon_crit_chance:",random_weapon.critical_chance, "\n", "weapon_accuracy:",random_weapon.accuracy, "\n", "magazine_capacity:",random_weapon.magazine_capacity, "\n", "shots_per_turn:", random_weapon.shots_per_turn)
	return random_weapon

def create_armour(game_progression, tier, fortune, armour_amount, armour_pieces):
	#Generate array of 6 items of either 1 or 0, with amount of 1's corresponding to armour_pieces
	armour_to_return = []
	armour_locations = [0,0,0,0,0,0]
	current_location = 0
	while armour_locations.count(1) < armour_pieces:
		if(random.choice([False,True])):
			armour_locations[current_location % 6] = 1 
		current_location += 1

	current_index = 0
	for possible_armour_piece in ["left_arm", "right_arm", "left_leg", "right_leg", "helmet", "chest_piece"]:
		if(armour_locations[current_index] == 1):
			# Create armour protection value as an amount ranging from 2/3 to 4/3 of the enemies armour amount
			armour_piece_protection_value = round(random.randrange( round((armour_amount / armour_pieces) - (armour_amount / armour_pieces / 3)), 1 + round((armour_amount / armour_pieces) + (armour_amount / armour_pieces / 2))) *  (1.2 + (current_index / 20 )))
			# Chance to get a higher tier armour piece
			new_tier = randomise_tier(tier, fortune)
			# if armour piece is higher tier, increase protection value
			if(new_tier == 2):
				armour_piece_protection_value = round((armour_piece_protection_value + new_tier) * 1.15)
			elif(new_tier == 3):
				armour_piece_protection_value = round((armour_piece_protection_value + new_tier) * 1.3)

			armour_piece_protection_value *= 1-(1/(armour_pieces + 1))
			
			try:
				armour_value = random.randrange(round(armour_piece_protection_value / 2 + 1) * (tier > 1 + 1) + (tier < 1) * random.randrange(1,7), round(12 * (game_progression + 1) / 8) * tier + (tier < 1) * random.randrange(6, 13))
			except:
				armour_value = 5 * tier + math.floor(game_progression / 5)
				print("Excepted armour value")
			armour_piece = Armour(possible_armour_piece, MyDictionary.get_armour_name(possible_armour_piece, new_tier), round(armour_piece_protection_value), new_tier + random.randrange(round(-new_tier / 2), new_tier + (4 - new_tier)) , new_tier, armour_value)
			armour_to_return.append(armour_piece)

		current_index += 1



	return armour_to_return;

def get_target_locations(name):
	coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	if(name == "Assailant"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Halfling"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Gnome"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Diesel-Mechanic"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Dwarf"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Nuclear-waste Farmer"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "High-brow"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Automaton"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];
	elif(name == "Baguettist"):
		coordinates = [[220,5],[240,180],[395,140],[37,140],[350,290],[37,290]];

	return coordinates;



def create_enemy(game_res_scale, game_progression, towns_discovered, fortune, current_town=None, tier_override=None, enemy_type = None, special=None, mutated=False, boss=False):
	if(tier_override == None):
		towns_required_for_tier_2 = 2
		towns_required_for_tier_3 = 5
		# Determine Tier based off of towns discovered (Tier 1 < Tier 2 < Tier 3)
		if(towns_discovered >= towns_required_for_tier_3):
			tier = 3;
		elif(towns_discovered >= towns_required_for_tier_2):
			tier = 2;
		else: 
			tier = 1;
	else:
		tier = tier_override


	if(game_progression == 0):
		game_progression = 0.01

	enemy_types_per_tier = [
						   ["Clock-work Mage", "Pirate", "Diesel-Mechanic", "Dwarf", "Nuclear-waste Farmer"],     		    # Tier 1		# Update with more items
						   ["High-brow", "Automaton", "Baguettist", "Irradiated", "Rich", "Outlaw", "Ex-marine"], # Tier 2		# Update with more items
						   ["Super Mutant", "French Soldier", "Monocle bandit"]														   		# Tier 3		# Update with more items
						   ]
	# Allowing for override of random selection 
	if(enemy_type == None):
		this_enemy_type = enemy_types_per_tier[tier-1][random.randrange(0, len(enemy_types_per_tier[tier-1]))]	# If no enemy type provided, select a random relevant tiered enemy type
	else:
		this_enemy_type = enemy_type # Otherwise, use provided enemy type

	button_locations = get_target_locations(this_enemy_type)

	# From the enemy type, get the sprite using internal module
	enemy_sprite_name = this_enemy_type.replace(" ", "_").lower()
	enemy_sprite = ImageHandling.get_enemy_sprite(this_enemy_type, game_res_scale)	 # Naming convention for sprites is first_lastname.png in sprites folder all lower case
	no_enemy_sprite = ImageHandling.get_enemy_sprite("NoEnemy", game_res_scale)
	statModifier = 1;

	if(mutated == True):
		statModifier = 1.2; 	# Initialised for altering stats if the enemy is mutated
	if(boss == True):
		statModifier = 1.5;		# Initialised for altering stats if the enemy is a boss

	
	#Generate health 
	min_health = 20
	max_health = 30
	health_lower = int(min_health * (1 + game_progression / 10) + (random.randrange(round(game_progression / 6), round(1 + game_progression / 3))))
	health_upper = int(max_health * (1 + game_progression / 8) + (random.randrange(round(game_progression / 6), round(1 + game_progression / 3))))

	enemy_health = round(random.randrange(health_lower, health_upper) * statModifier)


	# Define weapon, armour and item inventories
	weapon_inventory = { 

	}
	armour_inventory = {

	}
	item_inventory = {

	}

	# Populate weapon inventory with weapon objects
	for i in range(random.choice([1,1,1,1,1,1,1,1,1,2,3])): # Decide how many weapons the enemy should carry
		# Put random weapon into inventory dictionary
		weapon = create_weapon(game_progression, tier, fortune)
		weapon_inventory.update({weapon:1})
		equipped_weapon = weapon

	# Define armour amounts 
	if(tier == 1):
		enemy_armour = random.randrange(5, round(13 + game_progression / 3 ))  # define function for armour amount then divide it up into armour pieces below
	elif(tier == 2):
		enemy_armour = random.randrange(10, round(20 + game_progression / 4 ))
	else:
		enemy_armour = random.randrange(19, round(28 + game_progression / 5 ))

	#print(enemy_armour)
	# Generate armour parameters
	armour_pieces = random.choice([2,2,2,2,3,3,3,2,4,5,6]) # Decide how many pieces of armour enemy will have  

	armour_array = create_armour(game_progression, tier, fortune, enemy_armour, armour_pieces)

	for individual_armour in armour_array:
		armour_inventory.update({individual_armour:1})  


	# Populate Item Inventory
	items_by_tier = [															# Update with more items
					[Item("gene_synthesiser")], 											# Update with more items
					[Item("gene_synthesiser"), Item("Armour Piercing Rounds")],				# Update with more items
					[Item("gene_synthesiser"), Item("Armour Piercing Rounds"), Item("Concussion Rounds")]					# Update with more items
					]															# Update with more items

	stimpaks_to_carry = random.choice([0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) # 75% Chance to hold a stimpak
	stimpaks_to_carry *= tier
	stimpaks_to_carry = random.randrange(0, stimpaks_to_carry + 1) # Max stimpaks an enemy can carry is the current tier that the player is in (unless enemy is a boss)

	if(boss == True):
		stimpaks_to_carry += random.randrange(1, 4) # Ensure bosses always drop stimpaks, with a higher likelihood to carry more than a regular enemy 

	if(stimpaks_to_carry > 0):
		item_inventory.update({Item("stimpak"):stimpaks_to_carry}) # Add stimpaks to inventory
	
	other_item_chance = random.random() * 100 # Generate random number between 0 and 100

	item_quantity = 0
	if(other_item_chance > 95): # 5% chance to carry another 3 items
		item_quantity =  3;
	elif(other_item_chance > 87): # 13% chance to carry 2 other items
		item_quantity =  2;
	elif(other_item_chance > 80): # 20% chance to carry 1 other item
		item_quantity =  1;

	
	# Create an array with numerical entries corresponding to the items_by_tier variable
	item_locations = []
	for i in range(0, len(items_by_tier[tier - 1])): # Populate item_locations array with quantity of 0's corresponding to the length of the current possible items
		item_locations.append(0)
	current_location = 0
	items_positioned = 0
	while items_positioned < item_quantity: # Loop through until quantity of items has been reached
		if(random.choice([False,True])):	# Randomly choose whether or not to put a 1 in the items array at the current location
			item_locations[current_location % (len(item_locations))] = item_locations[current_location % (len(item_locations))] + 1  # Add 1 to the current location
			items_positioned += 1 # Update total items positioned
		current_location += 1 # Regardless of whether or not an item was added to the current location, update the current current_location
	
	if(item_locations.count(1) > 0 or item_locations.count(2) > 0 or item_locations.count(3) > 0): # If we do have an item to add
		loop_location_in_array = 0 
		for item_amount in item_locations: # Loop through item_locations
			if(item_amount != 0): # Is an item to be added in this position
				item_inventory.update({items_by_tier[tier - 1][loop_location_in_array]:item_amount}) # Add item to inventory
			loop_location_in_array += 1

	# Give enemy baguettes 
	baguettes_to_carry = ((math.log(4*((game_progression + 2)**5))) / 0.5) * random.uniform(0.3,0.8)
	baguettes_to_carry = round(baguettes_to_carry * random.uniform(1, (1+fortune/100)))

	# Modify enemy titles so that they are more grammaticaly correct
	if(this_enemy_type.lower() == "high-brow" or this_enemy_type.lower() == "three-legged"):
		enemy_vars = [this_enemy_type + " " + MyDictionary.get_name("male", True, False, False), enemy_health, enemy_armour, equipped_weapon, weapon_inventory, armour_inventory, item_inventory, enemy_sprite, baguettes_to_carry, no_enemy_sprite, button_locations] #Name, Health, Armour, Weapons_Inventory, Armour_inventory, Items_Inventory, sprite
	else:
		enemy_vars = [MyDictionary.get_name("male", True, False, False) + " the " + this_enemy_type, enemy_health, enemy_armour, equipped_weapon, weapon_inventory, armour_inventory, item_inventory, enemy_sprite, baguettes_to_carry, no_enemy_sprite, button_locations] #Name, Health, Armour, Weapons_Inventory, Armour_inventory, Items_Inventory, sprite

	return enemy_vars


