import MyDictionary, random, math, ImageHandling
from Main import Item, Weapon, Armour


#class Weapon:
#	def __init__(self, name, weapon_type, damage, criticalChance, accuracy, magazine_capacity, shots_per_turn, weight):
#		self.name = name
#		self.damage = damage
#		self.critical_chance = criticalChance
#		self.accuracy = accuracy
#		self.weapon_type = weapon_type
#		self.magazine_capacity = magazine_capacity
#		self.current_ammo = self.magazine_capacity
#		self.shots_per_turn = shots_per_turn

#class Armour:
#	def __init__(self, description, name, protection, weight):
#		self.description = description
#		self.name = name
#		self.protection = protection

#class Item:
#
#	def __init__(self, item):
#		if(item == "stimpak"):
#			self.Stimpak()
#		elif(item == "gene_editor"):
#			self.Gene_synthesiser()
#
#	def Stimpak(self):
#		self.name = "Stimpak"
#		self.amount = 10
#		self.weight = 0.5
#		self.variation = "consumable"
#		self.affector = "health"
#
#	def Gene_synthesiser(self):
#		self.name = "Gene-synthesiser"
#		self.amount = 1
#		self.weight = 0.5
#		self.variation = "consumable"
#		self.affector = "player_stats"
#
#	def consume(self, obj_effector):
#		obj_effector.health += self.amount # Update to add further variation 





def create_weapon(game_progression, tier, current_town=None):
	# Generate weapon parameters
	weapon_type_choices = ("melee", "ranged")	

	weapon_type_decider = random.randrange(0,2) 											   # Generate random number from 0-1
	weapon_name = MyDictionary.get_weapon_name(weapon_type_choices[weapon_type_decider], tier) # Use MyDictionary function to get a random name for the weapon

	weapon_type = weapon_type_choices[weapon_type_decider]									   # Decide if weapon is melee or ranged using random number 
	weapon_damage = math.ceil((game_progression**(math.e/3.2) + 12) * (random.uniform(1 - 0.25/tier, 1+0.2*tier) ) ) # Function to scale weapon damage with game progression 	

	#damage_deviation = 
	# Determine crit chance for weapon
	base_weapon_crit_chance = []

	for p in range(1,7):	#Populate array with 6 low crit chance options
		base_weapon_crit_chance.append(p * tier + random.randrange(0, round(game_progression / 3) + 1) )

	for j in range(7,10):	#Populate array with 3 medium crit chance options
		base_weapon_crit_chance.append(j * 2 * tier + random.randrange(0,round(game_progression / 3) + 1) )

	# Add a single high crit option to array (low chance)  
	base_weapon_crit_chance.append((j + 1) * 3 * tier + random.randrange(0,round(game_progression / 3) + 1) )

	weapon_crit_chance = random.choice(base_weapon_crit_chance)	

	weapon_accuracy = 0;
	add_accuracy_multiplier = 3;

	while random.random() <= add_accuracy_multiplier: # Progressive algorithm for determining accuracy of weapon 
		add_accuracy_multiplier *= 0.99;
		if(random.choice([True,False])):

			firstRandom = random.random();

			add_accuracy_multiplier -= (firstRandom / 5) * 0.2/tier;

		weapon_accuracy += 1;

	if(weapon_accuracy >= 100):
		weapon_accuracy = 100;		# Cap accuracy at 100%

	if("shotgun" in weapon_name.lower()): 	           			# If random weapon is a shotgun 
		magazine_capacity = 2 * tier;		           			# Make the magazine capacity a multiple of 2
		shots_per_turn = math.ceil(tier / 2)           			# Have the gun be 1 shot burst for tier 1 and 2 then 2 shot burst for tier 3
		weapon_damage = round(weapon_damage * 1.35)    			# Increase damage by 35%
		weapon_accuracy = round(weapon_accuracy * 0.9) 			# Decrease acuracy by 10%
	elif("revolver" in weapon_name.lower() or "hand" in weapon_name.lower(), "pistol" in weapon_name.lower()):   # If random weapon is a type of hand gun
		magazine_capacity = random.randrange(4, 6 * tier)		# Set magazine capacity to a specified range scaling on tier
		shots_per_turn = random.randrange(1, tier + 1) 			# Set shots per turn between 1 and tier 
	elif("rifle" in weapon_name.lower()):						# If weapon is a rifle
		magazine_capacity = random.randrange(3, tier * 4 + 1)   # Set magazine capacity between 3 and tier * 4
		weapon_damage = round(weapon_damage * 1.2)				# Increase damage by 20%
		shots_per_turn = 1										# Rifles always only shoot once per turn
	else:														# For any other type of gun
		magazine_capacity = random.randrange(5*tier, 10*tier)	# Large Magazine capacity 
		shots_per_turn = random.randrange(1, tier + 1)			# Random shots per round based off tier

	if(weapon_type == "melee"):	  			   # If weapon is a melee weapon
		magazine_capacity = 0;	  			   # Unlimited capacity (No reloading)
		shots_per_turn = math.ceil(tier / 2)   # Have the weapon hit once for tier 1 and 2 then twice for tier 3

	weapon_weight = random.randrange(1, 3*tier)

	# Generate weapon
	random_weapon = Weapon(weapon_name, weapon_type, weapon_damage, weapon_crit_chance, weapon_accuracy, magazine_capacity, shots_per_turn, weapon_weight)
	#print("Name:",random_weapon.name, "\n", "weapon_type:",random_weapon.weapon_type, "\n", "weapon_damage:",random_weapon.damage, "\n", "weapon_crit_chance:",random_weapon.critical_chance, "\n", "weapon_accuracy:",random_weapon.accuracy, "\n", "magazine_capacity:",random_weapon.magazine_capacity, "\n", "shots_per_turn:", random_weapon.shots_per_turn)
	return random_weapon


def create_enemy(game_resolution, game_progression, towns_discovered, current_town=None, tier_override=None, enemy_type = None, special=None, mutated=False, boss=False):
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
						   ["Scavenger", "Bruiser", "Nuclear-waste farmer", "Three-legged", "Skinny", "Poor"],     		   # Tier 1		# Update with more items
						   ["Colony-Guard", "Mutant", "10 Thumbed", "Irradiated", "Rich", "Outlaw", "Ex-marine"], 		   # Tier 2		# Update with more items
						   ["Super Mutant", "Genesis Guardian" ]														   # Tier 3		# Update with more items
						   ]
	# Allowing for override of random selection 
	if(enemy_type == None):
		this_enemy_type = enemy_types_per_tier[tier-1][random.randrange(0, len(enemy_types_per_tier[tier-1]))]	# If no enemy type provided, select a random relevant tiered enemy type
	else:
		this_enemy_type = enemy_type # Otherwise, use provided enemy type

	# From the enemy type, get the sprite using internal module
	enemy_sprite_name = this_enemy_type.replace(" ", "_").lower()
	enemy_sprite = ImageHandling.get_sprite(this_enemy_type, game_resolution)	 # Naming convention for sprites is first_lastname.png in sprites folder all lower case

	statModifier = 1;

	if(mutated == True):
		statModifier = 1.2; 	# Initialised for altering stats if the enemy is mutated
	if(boss == True):
		statModifier = 1.5;		# Initialised for altering stats if the enemy is a boss

    
	#Generate health 
	min_health = 12
	max_health = 20
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
	for i in range(random.choice([1,1,1,1,1,1,1,2,2,2,3])): # Decide how many weapons the enemy should carry
		# Put random weapon into inventory dictionary
		weapon = create_weapon(game_progression, tier)
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
	armour_pieces = random.choice([3,3,3,3,3,3,3,2,4,5,6]) # Decide how many pieces of armour enemy will have  
	
	#Generate array of 6 items of either 1 or 0, with amount of 1's corresponding to armour_pieces
	armour_locations = [0,0,0,0,0,0]
	current_location = 0
	while armour_locations.count(1) < armour_pieces:
		if(random.choice([False,True])):
			armour_locations[current_location % 6] = 1 
		current_location += 1

	current_index = 0
	for possible_armour_piece in ["left_arm", "right_arm", "left_leg", "right_leg", "helmet", "chest_piece"]:
		if(armour_locations[current_index] == 1):
			armour_piece = Armour(possible_armour_piece, MyDictionary.get_armour_name(possible_armour_piece, tier), round(random.randrange( round((enemy_armour / armour_pieces) - (enemy_armour / armour_pieces / 3)), round((enemy_armour / armour_pieces) + (enemy_armour / armour_pieces / 2))) *  (1.2 + (current_index / 20 ))), 3 )
			#print(armour_piece.description + ":" + str(armour_piece.protection))
			armour_inventory.update({armour_piece:1}) # Create armour piece and define armour amount as a random number ranging from 2/3 to 4/3 of the enemies armour amount 
		current_index += 1


	# Populate Item Inventory

	items_by_tier = [															# Update with more items
					[Item("stimpak")], 											# Update with more items
					[Item("stimpak"), Item("gene_synthesiser")],				# Update with more items
					[Item("stimpak"), Item("gene_synthesiser")]					# Update with more items
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
	for i in range(0, len(items_by_tier[tier]) - 1): # Populate item_locations array with quantity of 0's corresponding to the length of the current possible items
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
				item_inventory.update({items_by_tier[tier][loop_location_in_array + 1]:item_amount}) # Add item to inventory
			loop_location_in_array += 1

	
	if(this_enemy_type.lower() == "10 thumbed" or this_enemy_type.lower() == "three-legged"):
		enemy_vars = [this_enemy_type + " " + MyDictionary.get_name("male", True, False, False), enemy_health, enemy_armour, equipped_weapon, weapon_inventory, armour_inventory, item_inventory, enemy_sprite] #Name, Health, Armour, Weapons_Inventory, Armour_inventory, Items_Inventory, sprite
	else:
		enemy_vars = [MyDictionary.get_name("male", True, False, False) + " the " + this_enemy_type, enemy_health, enemy_armour, equipped_weapon, weapon_inventory, armour_inventory, item_inventory, enemy_sprite] #Name, Health, Armour, Weapons_Inventory, Armour_inventory, Items_Inventory, sprite

	return enemy_vars

	#Make the items in inventory an object of the main program
#print(create_enemy("1024x576", 30, 4, None, None))


