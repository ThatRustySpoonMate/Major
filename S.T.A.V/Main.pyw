#
# All player sprites used are from the game "Hotline Miami" all credit to them for the artwork Accessed from https://hotlinemiami.fandom.com
#


import threading, random, os, math, ObjectHandling, Conventions
from tkinter.ttk import *

class Player:
	def __init__(self, name, health, armour, currentWeapon, stats, gender):
		self.name = name
		self.gender = gender
		self.health = health;
		self.health_max = 100;
		self.equipped_armour = armour; #[0] = Helmet [1] = Chest_Piece [2] = Left_Arm [3] = Right_Arm [4] = Left_Leg [5] = Right_Leg
		
		# Defining stats based off of how the player allocated them
		self.fortune = stats[2] 
		self.insight = stats[1]
		self.charisma = stats[3]
		self.agility = stats[4]
		self.strength = stats[0]
		self.experience = 0;
		self.level = 1;
		self.unspent_skillpoints = 0;
		
		self.baguettes = 0;
		self.game_progression = 0
		self.towns_discovered = 0
		self.current_town = None
		self.update_stats()
		self.update_armour_total()

		self.at_town = False;

		# Set player to starting position in game map
		self.current_map_index = 0
		self.current_town_index = 0 
		self.current_location_index = -1

		self.equipped_weapon = currentWeapon

		self.weapon_inventory = {
		
		}

		self.armour_inventory = {
			
		}

		self.item_inventory = {
			
		}
		self.update_carry_weight()
		self.picked_starting_location = False;

	def take_damage(self, initial_damage):

		if(self.armour > 400):
			self.armour = 400 #Cap at 400 otherwise protection amount = > 1 meaning attacks will deal negative damage (essentially healing you)
			
		protection_amount = ((math.log2(self.armour + 64) / 3) * 100 - 200) # Given the amount of armour the player has, calculate percentage of damage to reduce
		
		damage_dealt = round(random.randrange(round(initial_damage * 0.8), round(initial_damage * 1.2)) * (1-protection_amount/100) )
		
		if(damage_dealt < 0):
			damage_dealt = 0 
		self.health -= damage_dealt;

		action_window.main_textbox.config(state=NORMAL)
		output_to_action_text(" " + str(damage_dealt) + " damage", True)
		action_window.main_textbox.config(state=DISABLED)

		self.check_remaining_health();

	def check_remaining_health(self):
		if(self.health <= 0):
			output_to_action_text("You have been slain by " + Adversary.name, True)
			action_frame.after(2000, lambda:end_game(False))
			

	def deal_damage(self, target, accuracy):
		this_attack_damage = self.equipped_weapon.damage;
		ammo_type = action_window.selected_ammo.get()
		# Define the modifier value as n for "normal" before special rounds are detected
		modifier = "n";
		if("AP rounds" in ammo_type):
			for key in self.item_inventory.keys():
				if(key.name == "AP rounds"):
					# Define parameter as ap to pass to the enemy when attacking them, results in 1.5* damage after armour is applied
					modifier = "ap";
					# Remove one copy of the item
					self.remove_item(key)
					break;
		elif("Concussion rounds" in ammo_type):
			for key in self.item_inventory.keys():
				if(key.name == "Concussion rounds"):
					# Define parameter as c for concussion to pass to the enemy when attacking them
					modifier = "c";
					# Remove once copy of the item
					self.remove_item(key)
					break;

		# Play appropriate audio file as to the equipped weapon
		for i in range(0, self.equipped_weapon.shots_per_turn):
			action_window.main_textbox.config(state=NORMAL)
			player_attack_hit = random.randrange(1, 101) <= accuracy #Calculate if attack hit based on players current weapon accuracy
			if(player_attack_hit == True): 
				if(Adversary.health > 0):

					if(self.equipped_weapon.weapon_type == "ranged"): # Ranged attack
						audio_handler.play_sound_effect(0.5, self.equipped_weapon.attack_file_data[0], self.equipped_weapon.attack_file_data[1])
					else: # Melee Attack
						this_attack_damage *= 1 + (self.strength /  30) # Scale melee damage so that increasing strength stat increases melee damage
						if("chainsaw" in self.equipped_weapon.name.lower()):
							audio_handler.play_sound_effect(0.6, "Hit_Chainsaw")
						else:
							audio_handler.play_sound_effect(0.9, "Hit_Melee")
					# Damage logistics
					if(random.randrange(1, 101) <= self.equipped_weapon.critical_chance + ((player_character.insight / 2) * (player_character.equipped_weapon.weapon_type == "ranged") ) ): #Hit did crit
						output_to_action_text("You crit for", False) 
						Adversary.takeDamage(this_attack_damage * 2, special = modifier, target = target) #Apply damage * 2 due to crit
					else: # Hit didn't crit
						output_to_action_text("You hit for", False)
						Adversary.takeDamage(this_attack_damage, special = modifier, target = target) #Apply standard weapon damage 

					self.equipped_weapon.attacked(self);
				else:
					# Enemy is dead
					break;
			else:
				audio_handler.play_sound_effect(1, "Miss")
				#Hit missed
				output_to_action_text("You missed", True)
				self.equipped_weapon.attacked(self);

			if(self.equipped_weapon.condition <= 0):
				break;
		
		action_window.main_textbox.config(state=DISABLED)
		loadActionFrame(Adversary)

	def broken_weapon(self):
		# Add in broken Weapon sound and remove item drop sound
		action_frame.after(800, lambda:audio_handler.play_dialogue(1, "Narrator_Weapon_Broken"))
		output_to_action_text("Your weapon has broken!", True)
		
	def heal(self, amount):
		self.health += amount
		if(self.health > self.health_max):
			self.health = self.health_max;

	def curse(self, affected, affect):
		affected += affect;
		return affected

	def get_ammo_types(self):
		ammo_types = []
		if(self.equipped_weapon.weapon_type == "ranged"):
			ammo_types.append([self.equipped_weapon.ammo_type, "x"])
		else:
			ammo_types.append(["None"])
		for item in self.item_inventory:
			if(item.variation == "ammo"):
				ammo_types.append([item.name, self.item_inventory[item]])

		return ammo_types

	def update_stats(self):
		self.max_carry_weight = 28 + (2 * self.strength);

	def update_armour_total(self):
		self.armour = 0
		for armour in self.equipped_armour:
			self.armour += armour.protection


	def update_carry_weight(self):
		self.current_carry_weight = 0

		for weapon in self.weapon_inventory:
			self.current_carry_weight += weapon.weight
		for armour_piece in self.armour_inventory:
			self.current_carry_weight += armour_piece.weight

		item_inventory_duplicates = list(self.item_inventory.values()) # Gets all values of keys (items) in the item inventory as an array
		i = 0
		for item in self.item_inventory:
			# Add the item's weight multiplied by the amount of them to the on-going total
			self.current_carry_weight += item.weight * item_inventory_duplicates[i]
			i += 1
		# Round current carry weight after calculation as rounding each element added to the total would result in an incorrect measurement (e.g. 0.5 getting rounded to 1 multiple times)
		self.current_carry_weight = round(self.current_carry_weight, 1)
		return

	def add_experience(self, amount): # Add experience to player
		self.experience += amount;
		stats_window.player_exp_bar['value'] = self.experience;
		root.update_idletasks();

		if(self.experience >= stats_window.player_exp_bar['maximum']): # Check if player has leveled up 
			self.level_up();
			

	def level_up(self):
		action_frame.after(1250, lambda:audio_handler.play_sound_effect(1, "Level_Up"))
		# Increment level
		self.level += 1;
		# Add skillpoint
		self.unspent_skillpoints += 1;
		# Add amount of exp passed the maximum required to level up to new maximum
		roll_over_exp = self.experience - stats_window.player_exp_bar['maximum']
		self.experience = 0;
		self.add_experience(roll_over_exp)
		# Update new maximum 
		stats_window.player_exp_bar.configure(maximum = (self.level + 4) ** 2)
		output_to_action_text("You have leveled up!", True)
		# Heal player
		self.heal(15)

	def upskill(self, skill_name):
		if(skill_name == "fortune"):
			self.fortune += 1;
		elif(skill_name == "insight"):
			self.insight += 1;
		elif(skill_name == "charisma"):
			self.charisma += 1;
		elif(skill_name == "agility"):
			self.agility += 1;
		elif(skill_name == "strength"):
			self.strength += 1;

		self.unspent_skillpoints -= 1;
		self.update_stats()
		load_stats_frame();
		

	def add_item(self, item, amount):

		if("Weapon" in str(item.__class__)):
			if(item in self.weapon_inventory.keys()): # If item already exists in inventory i.e. picking up another one
				self.weapon_inventory[item] += amount
			else:
				self.weapon_inventory.update({item:amount})

		if("Armour" in str(item.__class__)):
			if(item in self.armour_inventory.keys()): # If item already exists in inventory i.e. picking up another one
				self.armour_inventory[item] += amount
			else:
				self.armour_inventory.update({item:amount})

		if("Item" in str(item.__class__)):
			item_names_in_item_inventory = []
			for temp_item in self.item_inventory.keys(): 	# Loop through each object in inventory
				if(temp_item.name not in item_names_in_item_inventory):
					item_names_in_item_inventory.append(temp_item.name)


			if(item.name in item_names_in_item_inventory): # If item already exists in inventory i.e. picking up another one
				for temp_item in self.item_inventory.keys(): 	# Loop through each object in inventory
					if(temp_item.name == item.name):
						self.item_inventory[temp_item] += amount
				#self.item_inventory[item] += amount
			else:
				self.item_inventory.update({item:amount})
		self.update_carry_weight()

	def remove_item(self, item_id):
		# This function handles internal dropping of items with no user interaction
		# Check which class the item belongs to so that we know which inventory to look into
		if(isinstance(item_id, Weapon)):
			pass;
		elif(isinstance(item_id, Armour)):
			pass;
		elif(str(type(item_id)) == "<class '__main__.Item'>" or str(type(item_id)) == "<class 'Main.Item'>"):
			if(self.item_inventory.get(item_id) == 1):
				# Only one quantity of item to remove
				del self.item_inventory[item_id]
			else:
				self.item_inventory[item_id] -= 1;

		

	def drop_item(self, play_audio=True, index=None):
		# This function handles dopping of items through GUI, i.e when an item is selected to be dropped, this function is called
		# Play random click sound effect when this button is clicked

		if(play_audio == True):
			audio_handler.play_sound_effect(1, "Drop")

		item_to_drop_index = inventory_window.inventory_contents.curselection() #Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" also counts as an index)
		try:
			item_to_drop_index = item_to_drop_index[0]
			item_to_drop = self.get_item_in_inventory(item_to_drop_index)
		except Exception as e:
			item_to_drop = None;
		

		if(item_to_drop != None and index == None): # Dropping an item with no given index

			#Delete Item and then check if it was the currently equipped weapon/armour by the player
			if(item_to_drop[1] == "weapon"):
				#Drop weapon
				if(self.weapon_inventory[item_to_drop[0]] == 1): # If there is only one instance of the weapon
					del self.weapon_inventory[item_to_drop[0]] # Delete it
				else:
					self.weapon_inventory[item_to_drop[0]] -= 1 # Otherwise take one away

				# Check to see if the item dropped was the equipped item
				if(self.equipped_weapon == item_to_drop[0]):
					if(len(self.weapon_inventory) > 0): # Check we have atleast 1 weapon in our inventory to auto-equip
						self.equipped_weapon = list(self.weapon_inventory.keys())[0] # Default equip first item in weapon inventory
					else:
						self.equipped_weapon = default_weapon


			if(item_to_drop[1] == "armour"):
				if(self.armour_inventory[item_to_drop[0]] == 1):
					del self.armour_inventory[item_to_drop[0]]
				else:
					self.armour_inventory[item_to_drop[0]] -= 1

				replacement_equipped = False
				for armour_item in self.armour_inventory: #Loop through all armour items in inventory
					if(armour_item.description == item_to_drop[0].description and armour_item != item_to_drop[0]): #Check if any are matching types (e.g left arm = left arm)
						self.equip_item(armour_item) #Auto-replace item
						replacement_equipped = True #Flag that it has been replaced

				if(replacement_equipped == False): #If no replacement could be found
					if(item_to_drop[0] in self.equipped_armour):
						self.equipped_armour[self.equipped_armour.index(item_to_drop[0])] = default_armour #Replace with no armour

			if(item_to_drop[1] == "item"):
				if(self.item_inventory[item_to_drop[0]] == 1):
					del self.item_inventory[item_to_drop[0]]
				else:
					self.item_inventory[item_to_drop[0]] -= 1
		
		elif(index != None):

			item_to_drop = self.get_item_in_inventory(index + 1)

			#Delete Item and then check if it was the currently equipped weapon/armour by the player
			if(item_to_drop[1] == "weapon"):
				#Drop weapon
				if(self.weapon_inventory[item_to_drop[0]] == 1):
					del self.weapon_inventory[item_to_drop[0]]
				else:
					self.weapon_inventory[item_to_drop[0]] -= 1

				# Check to see if the item dropped was the equipped item
				if(self.equipped_weapon == item_to_drop[0]):
					if(len(self.weapon_inventory) > 0): # Check we have atleast 1 weapon in our inventory to auto-equip
						self.equipped_weapon = list(self.weapon_inventory.keys())[0] # Default equip first item in weapon inventory
					else:
						self.equipped_weapon = default_weapon


			if(item_to_drop[1] == "armour"):
				if(self.armour_inventory[item_to_drop[0]] == 1):
					del self.armour_inventory[item_to_drop[0]]
				else:
					self.armour_inventory[item_to_drop[0]] -= 1

			if(item_to_drop[1] == "item"):
				if(self.item_inventory[item_to_drop[0]] == 1):
					del self.item_inventory[item_to_drop[0]]
				else:
					self.item_inventory[item_to_drop[0]] -= 1

		self.update_carry_weight()
		self.update_armour_total()
		if(active_frame == inventory_frame):
			loadInventoryFrame()

	def equip_item(self, given_item=None):
		# Play random click sound effect when this button is clicked
		audio_handler.play_sound_effect(1, "Click")
		item_to_equip_index = inventory_window.inventory_contents.curselection() #Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" also counts as an index)
		try:
			item_to_equip_index = item_to_equip_index[0]
		except Exception as ex:
			return

		item = self.get_item_in_inventory(item_to_equip_index)

		if(item != None and given_item == None): #Equip button has been clicked in inventory menu
			if(item[1] == "weapon"):
				if(item[0] == self.equipped_weapon): #If selected weapon to equip is our current weapon, "dequip" it 
					self.equipped_weapon = default_weapon
				else:
					self.equipped_weapon = item[0]

			elif(item[1] == "armour"):
				if(item[0].description == "helmet"):
					if(item[0] == self.equipped_armour[0]):
						self.equipped_armour[0] = default_armour
					else:
						self.equipped_armour[0] = item[0]

				elif(item[0].description == "chest_piece"):
					if(item[0] == self.equipped_armour[1]):
						self.equipped_armour[1] = default_armour
					else:
						self.equipped_armour[1] = item[0]

				elif(item[0].description == "left_arm"):
					if(item[0] == self.equipped_armour[2]):
						self.equipped_armour[2] = default_armour
					else:
						self.equipped_armour[2] = item[0]

				elif(item[0].description == "right_arm"):
					if(item[0] == self.equipped_armour[3]):
						self.equipped_armour[3] = default_armour
					else:
						self.equipped_armour[3] = item[0]

				elif(item[0].description == "left_leg"):
					if(item[0] == self.equipped_armour[4]):
						self.equipped_armour[4] = default_armour
					else:
						self.equipped_armour[4] = item[0]

				elif(item[0].description == "right_leg"):
					if(item[0] == self.equipped_armour[5]):
						self.equipped_armour[5] = default_armour
					else:
						self.equipped_armour[5] = item[0]
			
			elif(item[1] == "item"):
				item[0].consume(self)
				self.drop_item(False, item_to_equip_index - 1)

		elif(given_item != None): # Item is given in function
			if("Weapon" in str(given_item.__class__)): # Item to equip is a weapon
				self.equipped_weapon = given_item
			elif("Armour" in str(given_item.__class__)): # Item to equip is an armour item
				if(given_item.description == "helmet"):
					self.equipped_armour[0] = given_item
				elif(given_item.description == "chest_piece"):
					self.equipped_armour[1] = given_item
				elif(given_item.description == "left_arm"):
					self.equipped_armour[2] = given_item
				elif(given_item.description == "right_arm"):
					self.equipped_armour[3] = given_item
				elif(given_item.description == "left_leg"):
					self.equipped_armour[4] = given_item
				elif(given_item.description == "right_leg"):
					self.equipped_armour[5] = given_item

		self.update_armour_total()
		loadInventoryFrame()

	def pick_up_item(self):
		item_to_pickup_index = action_window.loot_window.curselection() # Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" and other dividers also count as an index)

		try:
			item_to_pickup_index = item_to_pickup_index[0]
		except Exception as ex:
			return

		item = Adversary.get_item_in_inventory(item_to_pickup_index) 
		if(item != None): # A valid object has been selected to pick-up
			if(player_character.current_carry_weight + item[0].weight <= player_character.max_carry_weight): # Ensure that the player can carry the item
				audio_handler.play_sound_effect(0.9, "Loot")
				self.add_item(item[0], 1) # Add item to your inventory
				Adversary.drop_item(item_to_pickup_index) # Remove item from adversary inventory

				text_to_pickup = action_window.loot_window.get(item_to_pickup_index)
				text_to_pickup_list = text_to_pickup.replace("(", "").replace(")", "")
				text_to_pickup_list = text_to_pickup_list.split(" ")

				try:
					quantity = int(text_to_pickup_list[len(text_to_pickup_list) - 1])
					

					if(quantity > 1):
						action_window.loot_window.delete(item_to_pickup_index) # PROBLEM HERE
						action_window.loot_window.insert(item_to_pickup_index, text_to_pickup[:len(text_to_pickup) - (2 + len(str(quantity)))] + "(" + str(quantity - 1) + ")")
					else:
						action_window.loot_window.delete(item_to_pickup_index)

				except Exception as ex:
					action_window.loot_window.delete(item_to_pickup_index) # Remove from available loot
			else:
				# If this item puts the player over the max carry weight, tell them
				audio_handler.play_dialogue(1, "Narrator_Encumbered")
				output_to_action_text("You cannot carry anymore.", True)


		
		self.update_carry_weight()
			

	def get_item_in_inventory(self, index):
		
		item_iterator = index + 1
		weapon_inv_length = len(self.weapon_inventory)
		armour_inv_length = len(self.armour_inventory)
		item_inv_length = len(self.item_inventory)

		item_iterator -= 1
		index -= 1


		if(item_iterator > weapon_inv_length): # Item is not in weapons inventory
			item_iterator -= weapon_inv_length + 1 # Add one because of the divider we have in the text box
			index -= weapon_inv_length + 1 # Add one because of the divider we have in the text box

			if(item_iterator > armour_inv_length): # Item is not in armour inventory
				item_iterator -= armour_inv_length + 1
				index -= armour_inv_length + 1

				# Item must be in items inventory
				i = 0
				for key in self.item_inventory:
					if(i == index):
						return [list(self.item_inventory.keys())[i], "item" ]
					i += 1

			else: #Item is in armour inventory
				i = 0
				for key in self.armour_inventory:
					if(i == index):
						return [list(self.armour_inventory.keys())[i], "armour"]
					i += 1

		else: #Item is in weapons inventory
			i = 0
			for key in self.weapon_inventory:

				if(i == index):
					return [list(self.weapon_inventory.keys())[i], "weapon"]
				i += 1


class Weapon:
	def __init__(self, name, weapon_type, damage, criticalChance, accuracy, magazine_capacity, shots_per_turn, weight, tier, wear_value, ammo_type, value):
		self.name = name
		self.damage = damage
		self.critical_chance = criticalChance
		self.accuracy = accuracy
		self.weapon_type = weapon_type
		self.magazine_capacity = magazine_capacity
		self.current_ammo = self.magazine_capacity
		self.ammo_type = ammo_type
		self.shots_per_turn = shots_per_turn
		self.weight = weight
		self.tier = tier
		self.ready = True; # Used for flagging if the weapon is ready to fire or not (reloading)

		self.condition = 100;
		self.wear_value = wear_value;
		if (value <= 0):
			self.value = random.randrange(1 + tier, 9 * self.tier)
		else:
			self.value = value

		# Get random weapon sound filename
		if(self.weapon_type.lower() == "ranged"):
			self.attack_file_data = self.generate_fire_sound()

	def attacked(self, player):
		# Function that is called when the player uses this weapon

		if(self.weapon_type == "ranged"):
			self.current_ammo -= 1;

		# Decrease condition of weapon
		if(self.name != "Fists"):
			self.condition -= random.randrange(round(self.wear_value / 2), round(self.wear_value * 1.5) + 1);
			self.check_condition(player)

	def attacked_as_enemy(self):
		self.condition -= random.choice([1,2])
		self.current_ammo -= 1;

		if(self.current_ammo <= 0):
			self.current_ammo == self.magazine_capacity;


	def check_condition(self, player):
		# Check if weapon is broken
		if(self.condition <= 0):
			# Get all weapons in the player's inventory
			item_inventory = list(player.weapon_inventory.keys())
			current_index = 0
			# Find location of weapon in player's inventory
			for item in item_inventory:
				if(self == item):
					item_index = current_index;
					
				current_index += 1;
			# Drop the item from the player's inventory
			player.drop_item(True, item_index)
			# Inform the player that their active weapon has broken
			player.broken_weapon();


	def reload(self, action_window, NORMAL, DISABLED, END, player_character):
		# Play reload sound
		self.current_ammo = self.magazine_capacity;
		self.ready = False;
		# Partially reload action frame
		action_window.player_description_text.configure(state = NORMAL)
		action_window.player_description_text.delete(0.0, END)
		playerTextToInsert = player_character.name + ":\nHealth = " + str(player_character.health) + "\nArmour: " + str(player_character.armour) + "\nWEAPON: " + player_character.equipped_weapon.name + "\nMagazine: " + str(player_character.equipped_weapon.magazine_capacity) + "/" + str(player_character.equipped_weapon.magazine_capacity) #Player name from SPECIAL screen
		action_window.player_description_text.insert(END, playerTextToInsert)
		action_window.player_description_text.configure(state = DISABLED)
		action_window.attack_button.configure(text = "Engage")


	def generate_fire_sound(self):
		# Due to the way i have handled creating weapon objects (from an external module) pygame mixer sound objects don't like to behave themselves, as such i will need to assign sound objects the long way :/
		# Initialise variables to know where to look for audio files
		script_dir = os.path.dirname(__file__) #<-- absolute directory this file is in
		target_path = "AudioFiles"
		audio_folder = os.path.join(script_dir, target_path) # Create path for the audio folder and store as variable 'audio_folder'
		desired_sub_folder = "Sound_Effects";
	
		# Ranged weapon
		if("laser" in self.name.lower() or "particle" in self.name.lower() or "fusion" in self.name.lower()):
			tertiary_folder = "Hit_Laser"
		elif("bow" in self.name.lower() or "slingshot" in self.name.lower()):
			tertiary_folder = "Hit_Bow"
		elif("rotary" in self.name.lower()):
			tertiary_folder = "Hit_Rotary_Cannon"
		else:
			tertiary_folder = "Hit_Ballistic"

		return [tertiary_folder, random.choice(os.listdir(audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder)).replace(".wav", "")]




class Armour:
	def __init__(self, description, name, protection, weight, tier, value):
		self.description = description
		self.name = name
		self.protection = protection
		self.weight = weight
		self.tier = tier
		self.value = value;


class Item:

	def __init__(self, item):
		if(item == "stimpak"):
			self.Stimpak()
		elif(item == "gene_synthesiser"):
			self.Gene_synthesiser()
		elif(item == "Armour Piercing Rounds"):
			self.armour_piercing_rounds()
		elif(item == "Concussion Rounds"):
			self.concussion_rounds()

	def Stimpak(self):
		self.name = "Stimpak"
		self.amount = 10
		self.weight = 0.5
		self.variation = "consumable"
		self.affector = "health"
		self.value = 8;

	def Gene_synthesiser(self):
		self.name = "Gene-synthesiser"
		self.amount = 1
		self.weight = 0.5
		self.variation = "consumable"
		self.affector = "player_stats"
		self.value = 15;

	def armour_piercing_rounds(self):
		self.name = "AP rounds"
		self.variation = "ammo"
		self.amount = 1;
		self.weight = 0.1;
		self.affector = "ammo"
		self.value = 10

	def concussion_rounds(self):
		self.name = "Concussion rounds"
		self.variation = "ammo"
		self.amount = 1;
		self.weight = 0.1;
		self.affector = "ammo"
		self.value = 20;

	def consume(self, obj_effector):
		if(self.affector == "health"):
			obj_effector.heal(self.amount)

		elif(self.affector == "player_stats"):
			stat_choice = random.choice([0,1,2,3,4])
			if(stat_choice == 0):
				obj_effector.strength += 1;
			elif(stat_choice == 1):
				obj_effector.insight += 1;
			elif(stat_choice == 2):
				obj_effector.fortune += 1;
			elif(stat_choice == 3):
				obj_effector.charisma += 1;
			else:
				obj_effector.agility += 1;
			obj_effector.update_stats();



class ActionWindow():

	def __init__(self, root):
		# Initialisation of action widgets
		self.title = Label(action_frame, text='ACTION',  font=("Courier", round(14 * game_res_scale)), bg="#D3D3D3")
		self.action_button = Button(action_frame, text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",state = DISABLED, bg="#D3D3D3",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(action_frame, text='Map', fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:loadMapFrame())
		self.inventory_button = Button(action_frame, text='Inventory', fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:loadInventoryFrame())
		self.stats_button = Button(action_frame, text="Stats", fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:load_stats_frame())
		self.enemy_description_text = Text(action_frame, height = round(10), width = round(23), font=("Courier", math.ceil(12 * game_res_scale)), bg="#D3D3D3")
		
		self.clear_textbox_button = Button(action_frame, text = "Clear", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:self.clear_main_textbox())	
		self.done_looting_button = Button(action_frame, text="Done", width = round(36 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command=lambda:self.done_looting())
		self.pickup_button = Button(action_frame, text="Pick-up", width = round(36 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command=lambda:player_character.pick_up_item())

		# Create buttons for handling game progression
		self.forward_button = Button(action_frame, text = "Forward", width = round(    22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:change_location(+1))
		self.backward_button = Button(action_frame, text = "Backward", width = round(  22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:change_location(-1))
		self.left_at_fork_button = Button(action_frame, text = "Left", width = round(  22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:change_location(+1, "left"))
		self.right_at_fork_button = Button(action_frame, text = "Right", width = round(22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:change_location(+1, "right"))
		self.open_chest_button = Button(action_frame, text = "Open", width = round(    22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:chest_control(True))
		self.leave_chest_button = Button(action_frame, text = "Leave", width = round(  22 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:chest_control(False))
		
		self.merchant_button = Button(action_frame, text = "Merchant", width = round(18 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:enter_merchant())
		self.goto_gamble_button = Button(action_frame, text = "Gamble", width = round(18 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:enter_gamble())

		# Gambling related widgets
		self.gamble_wager = 0;
		self.gamble_heads_button = Button(action_frame, text = "HEADS", width = round(18 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:confirm_gamble("h"))
		self.gamble_tails_button = Button(action_frame, text = "TAILS", width = round(18 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:confirm_gamble("t"))
		self.gamble_equal_button = Button(action_frame, text = "EQUAL", width = round(18 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:confirm_gamble("e"))
		self.gamble_wager_increase_button = Button(action_frame, text = ">", width = round(1 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:wager_change(True))
		self.gamble_wager_decrease_button = Button(action_frame, text = "<", width = round(1 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:wager_change(False))
		self.gamble_wager_display = Label(action_frame, text = str(self.gamble_wager), width = round(4 * game_res_scale), height = round(1 * game_res_scale), bg="#D3D3D3")
		self.gamble_wager_title = Label(action_frame, text = "WAGER", width = round(10 * game_res_scale), font=("Courier", round(14)), height = round(1 * game_res_scale), bg="#333")
		self.dealer_image = ImageHandling.get_location_sprite("Dealer", game_res_scale)
		self.gamble_result_image = Label(action_frame, image = self.dealer_image)
		self.exit_from_gamble_button = Button(action_frame, text = "Exit", fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:exit_sub_town("gamble"))

		# Merchant related widgets
		self.loiter_flag = True;
		self.exit_from_merchant_button = Button(action_frame, text = "Exit", fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = lambda:exit_sub_town("merchant"))
		self.buy_button = Button(action_frame, text = "Buy", width = round(60 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = buy_item)
		self.sell_button = Button(action_frame, text = "Sell", width = round(60 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", bg="#D3D3D3", command = sell_item)
		
		self.player_inventory = Listbox(action_frame, height = round(17 * game_res_scale) , width = round(39 * game_res_scale), bg="#D3D3D3", font=("Courier", round(14)))
		self.player_scrollbar = Scrollbar(self.player_inventory, orient="vertical", bg="#D3D3D3")

		self.merchant_inventory = Listbox(action_frame, height = round(17 * game_res_scale) , width = round(39 * game_res_scale), bg="#D3D3D3", font=("Courier", round(14)))
		self.merchant_scrollbar = Scrollbar(self.merchant_inventory, orient="vertical", bg="#D3D3D3")
		self.player_baguettes_quantity_display = Label(action_frame, text = str(player_character.baguettes), fg = "#C5B358", bg="#333",  font=("Courier", round(16 * game_res_scale)))
		self.merchant_baguettes_quantity_display = Label(action_frame, text = "UNINIT", fg = "#C5B358", bg="#333",  font=("Courier", round(16 * game_res_scale)))
		self.baguette_image = ImageHandling.get_UI_sprite("baguette_icon", game_res_scale)
		self.baguettes_icon_1 = Label(action_frame, image = self.baguette_image, bg="#333") # For player baguettes
		self.baguettes_icon_2 = Label(action_frame, image = self.baguette_image, bg="#333") # For merchant baguettes
		self.merchant_baguette_title = Label(action_frame, text = "Merchant", font = ("Courier", 16),  bg="#333")
		self.player_baguette_title = Label(action_frame, text = "You", font = ("Courier", 16), bg="#333")

		# Initialise flag for tracking if loot window is drawn
		self.looting = False;
		# Initialise flag for tracking if the player is actively engaged in combat
		self.in_combat = False;
		
		#Load image
		try:
			self.context_image = Label(action_frame, image = Adversary.sprite)
		except:
			self.context_image = Label(action_frame, image = noEnemyIMG)

		self.player_description_text = Text(action_frame, height = round(10), width = round(23), font=("Courier", math.ceil(12 * game_res_scale)), bg="#D3D3D3")

		self.Gun_Icon = ImageHandling.get_UI_sprite("gun_icon", game_res_scale)
		self.Sword_Icon = ImageHandling.get_UI_sprite("sword_icon", game_res_scale)

		self.attack_target = None;
		self.target_head_button = Button(action_frame, text = "Head", command = lambda:self.attack_location(self.target_head_button['text'], self.target_head_button))
		self.target_torso_button = Button(action_frame, text = "Torso", command = lambda:self.attack_location(self.target_torso_button['text'], self.target_torso_button))
		self.target_arm_left_button = Button(action_frame, text = "Left arm", command = lambda:self.attack_location(self.target_arm_left_button['text'], self.target_arm_left_button))
		self.target_arm_right_button = Button(action_frame, text = "Right arm", command = lambda:self.attack_location(self.target_arm_right_button['text'], self.target_arm_right_button))
		self.target_leg_left_button = Button(action_frame, text = "Left leg", command = lambda:self.attack_location(self.target_leg_left_button['text'], self.target_leg_left_button))
		self.target_leg_right_button = Button(action_frame, text = "Right leg", command = lambda:self.attack_location(self.target_leg_right_button['text'], self.target_leg_right_button))
		self.attack_button = Button(action_frame, text = "Engage", image = self.Gun_Icon, compound = "left", state = DISABLED, command = lambda:confirm_attack(self.attack_target, True)) #IF GOON.name == "none" then disable button

		self.run_button = Button(action_frame,   width = round(    22 * game_res_scale), height = round(2 * game_res_scale), text = "RUN", command = lambda:run_option())
		self.fight_button = Button(action_frame, width = round(    22 * game_res_scale), height = round(2 * game_res_scale), text = "FIGHT", command = lambda:fight_option())
		self.current_enemy = None;

		self.selected_ammo = StringVar(root)
		self.selected_ammo.set("Normal")
		self.ammo_selector = OptionMenu(action_frame, self.selected_ammo, "Normal")

		self.ammo_selector_child = self.ammo_selector.children['menu']

		self.main_textbox = Text(action_frame, height = 10, width = 65, font=("Courier", math.ceil(10 * game_res_scale)), bg="#D3D3D3")
		self.scrollbar = Scrollbar(self.main_textbox, orient="vertical", bg="#D3D3D3")
		self.main_textbox.config(yscrollcommand=self.scrollbar.set, state = DISABLED)
		
		self.draw_standard_action_layout();
		# Place progression buttons
		self.draw_progression_buttons();

		self.loot_window = Listbox(action_frame, height = 18, width = 52, font=("Courier", math.ceil(12 * game_res_scale))) #Perform last as to draw it over context image 
		if("1280" in game_resolution):
			self.loot_window.configure(width = 54)

	def pre_fight_options_show(self):
		output_to_action_text("An enemy stands in your path, what would you like to do?", True)
		self.disable_navigation()
		self.fight_button.place(x =  (585 * game_res_scale), y = 365 * game_res_scale)
		self.run_button.place(x = (275 * game_res_scale), y = 365 * game_res_scale)
		if(player_character.current_town_index == 8):
			self.run_button.configure(state = DISABLED)
		else:
			self.run_button.configure(state = NORMAL)

	def pre_fight_options_hide(self):
		self.fight_button.place_forget()
		self.run_button.place_forget()

	def enable_navigation(self):
		self.action_button.configure(state = NORMAL)
		self.inventory_button.configure(state = NORMAL)
		self.map_button.configure(state = NORMAL)
		self.stats_button.configure(state = NORMAL)

	def disable_navigation(self):
		self.action_button.configure(state = DISABLED)
		self.inventory_button.configure(state = DISABLED)
		self.map_button.configure(state = DISABLED)
		self.stats_button.configure(state = DISABLED)

	def done_looting(self):
		self.done_looting_button.place_forget() # When the player hits the DONE button, hide all looting related widgets
		self.loot_window.place_forget()
		self.pickup_button.place_forget()
		self.loot_window.delete(0, END) # Delete contents of loot window to prevent doubling up of items
		self.title.place_forget()
		self.title.config(text = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].name) #Change title from loot to action
		self.title.place(x = (500 - len(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].name) * 5) * game_res_scale, y = -3)
		self.clear_textbox_button.place(x = (480 * game_res_scale), y = 364 * game_res_scale) # Replace clear textbox button
		self.looting = False;

		# Place progression buttons
		self.draw_progression_buttons();
		loadActionFrame(Adversary)


	def clear_main_textbox(self): # Clear text box when button is pressed
		self.main_textbox.configure(state = NORMAL)
		self.main_textbox.delete(1.0, END)
		self.main_textbox.configure(state = DISABLED)
		loadActionFrame(Adversary)

	def draw_progression_buttons(self):
		# Place progression buttons
		self.forward_button.configure(width = round(22 * game_res_scale))
		if(player_character.picked_starting_location == True and self.in_combat == False):
			if(player_character.current_town_index != 8):
				self.forward_button.place(x = (585 * game_res_scale), y = 365 * game_res_scale)
			if(player_character.current_town_index != 0 or player_character.current_location_index > 0):
				self.backward_button.place(x = (275 * game_res_scale), y = 365 * game_res_scale)
		else:
			self.forward_button.place_forget()
			self.backward_button.place_forget()

		encounter_active = False;

	def draw_town_buttons(self):
		# place all buttons that allow for interaction with town elements on screen
		self.forward_button.configure(width = round(18 * game_res_scale))
		self.forward_button.place(x = (642 * game_res_scale), y = 365 * game_res_scale)
		self.goto_gamble_button.place(x = (450 * game_res_scale), y = 365 * game_res_scale)
		self.merchant_button.place(x = (250 * game_res_scale), y = 365 * game_res_scale)

	def remove_town_buttons(self):
		# Remove all buttons that integrate with town elements
		self.forward_button.place_forget()
		self.goto_gamble_button.place_forget()
		self.merchant_button.place_forget()
		

	def chest_buttons_flash(self):
		self.open_chest_button.flash()
		self.leave_chest_button.flash()

	def fork_buttons_flash(self):
		self.left_at_fork_button.flash()
		self.right_at_fork_button.flash()

	def attack_location(self, location, button_obj):
		self.attack_target = location;
		self.attack_button.configure(state = NORMAL)
		button_obj.configure(bg = "gold")
		other_buttons = Conventions.remove_values_from_list([self.target_head_button,self.target_torso_button,self.target_arm_left_button,self.target_arm_right_button,self.target_leg_left_button,self.target_leg_right_button], button_obj)
		for button in other_buttons:
			button.configure(bg = "light grey")
	def draw_standard_action_layout(self):
		self.scrollbar.place(x = 505 * game_res_scale, y = 0)
		# Placement of action buttons
		self.title.place(x= (500 * game_res_scale) - 20, y = -3)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.enemy_description_text.place(x = 5* game_res_scale, y = 50 * game_res_scale)
		self.context_image.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale) 
		self.player_description_text.place(x = 785* game_res_scale, y = 50* game_res_scale)

		self.attack_button.place(x = 810 * game_res_scale, y = 235 * game_res_scale)

		self.ammo_selector.place(x = 810 * game_res_scale, y = 265 * game_res_scale)
		self.main_textbox.place(x = (window_width / 4) - (5 * game_res_scale), y = 405 * game_res_scale)
		self.clear_textbox_button.place(x = (480 * game_res_scale), y = 365 * game_res_scale)

	def erase_standard_action_layout(self): 
		self.scrollbar.place_forget()
		# Placement of action buttons
		self.title.place_forget()
		self.action_button.place_forget()
		self.inventory_button.place_forget()
		self.map_button.place_forget()
		self.stats_button.place_forget()
		self.enemy_description_text.place_forget()
		self.context_image.place_forget()
		self.player_description_text.place_forget()

		self.attack_button.place_forget()
		self.target_head_button.place_forget()
		self.target_torso_button.place_forget()
		self.target_arm_left_button.place_forget()
		self.target_arm_right_button.place_forget()
		self.target_leg_left_button.place_forget()
		self.target_leg_right_button.place_forget()

		self.ammo_selector.place_forget()
		self.main_textbox.place_forget()
		self.clear_textbox_button.place_forget()


	def draw_gamble_screen(self):
		self.title.configure(text = "Two-Up")
		self.title.place(x= (500 * game_res_scale) - 20, y = -3)
		self.gamble_heads_button.place(x = 590 * game_res_scale, y = 365 * game_res_scale)
		self.gamble_tails_button.place(x = 270 * game_res_scale, y = 365 * game_res_scale)
		self.gamble_equal_button.place(x = 430 * game_res_scale, y = 365 * game_res_scale)
		self.gamble_wager_title.place(x = 440 * game_res_scale, y = 440 * game_res_scale)
		self.gamble_wager_decrease_button.place(x = 455 * game_res_scale, y = 470 * game_res_scale)
		self.gamble_wager_display.place(x = 480 * game_res_scale, y = 472 * game_res_scale)
		self.gamble_wager_increase_button.place(x = 525 * game_res_scale, y = 470 * game_res_scale)
		self.gamble_result_image.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale)
		self.exit_from_gamble_button.place(x = 963 * game_res_scale, y = 0)

	def erase_gamble_screen(self):
		self.title.place_forget()
		self.gamble_heads_button.place_forget()
		self.gamble_tails_button.place_forget()
		self.gamble_equal_button.place_forget()
		self.gamble_wager_title.place_forget()
		self.gamble_wager_decrease_button.place_forget()
		self.gamble_wager_display.place_forget()
		self.gamble_wager_increase_button.place_forget()
		self.gamble_result_image.place_forget()
		self.exit_from_gamble_button.place_forget()


	def draw_merchant_screen(self):
		self.title.configure(text = "Merchant")

		self.exit_from_merchant_button.place(x = 963 * game_res_scale, y = 0)
		self.buy_button.place(x = 67 * game_res_scale, y = 480 * game_res_scale)
		self.sell_button.place(x = 512 * game_res_scale, y = 480 * game_res_scale)
		self.player_inventory.place(x = 510 * game_res_scale, y = 100 * game_res_scale)
		self.merchant_inventory.place(x = 65 * game_res_scale, y = 100 * game_res_scale)
		# Baguette (Currency) display
		self.player_baguette_title.place(x = 705 * game_res_scale, y = 512 * game_res_scale)
		self.player_baguettes_quantity_display.place(x = 705 * game_res_scale + ((len(str(player_character.baguettes)) - 1 ) * 10) * game_res_scale, y = 540 * game_res_scale)
		self.baguettes_icon_1.place(x = 685 * game_res_scale, y = 538 * game_res_scale)
		
		self.merchant_baguette_title.place(x = 220 * game_res_scale, y = 512 * game_res_scale)
		self.merchant_baguettes_quantity_display.place(x = 254 * game_res_scale + ((len(str(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].my_merchant.baguettes)) - 1) * 10) * game_res_scale, y = 540 * game_res_scale)
		self.baguettes_icon_2.place(x = 234 * game_res_scale, y = 538 * game_res_scale)

		self.repopulate_player_inventory()

		# Create array of merchant objects that store inventory items, grab corresponding merchant using player_character's current town location

	def repopulate_player_inventory(self):
		self.player_inventory.delete(0, END)

		inventory_listbox_width = self.player_inventory['width']
		# Draw Players inventory contents
		# Populate with weapons 
		self.player_inventory.insert(END, insert_inventory_divider("weapon", inventory_listbox_width))
		# Update play baguettes quantity display 
		self.player_baguettes_quantity_display.configure(text = str(player_character.baguettes))
		current_index = 1;
		for weapon in player_character.weapon_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(weapon)

			#Label equipped weapons with a ">" prefix
			if(weapon == player_character.equipped_weapon):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""
			# Verify that the whole weapon name will fit in the list box
			if(len(equippedIndicator) + len(weapon.name) + 1 < inventory_listbox_width - len(str(weapon.value))):
				self.player_inventory.insert(END, equippedIndicator + " " + weapon.name + " " * (inventory_listbox_width - len(equippedIndicator) - len(weapon.name) - 1 - len(str(weapon.value))) + str(weapon.value)) # Add value 
			else:
				# If not, clip off end of it and add elipses 
				self.player_inventory.insert(END, equippedIndicator + " " + weapon.name[:inventory_listbox_width - len(equippedIndicator) - 5 - len(str(weapon.value))] + "... " + weapon_comparison_indicator + " " + str(weapon.value)) # Add value 

			# Colour text in relation to weapon tier
			self.player_inventory.itemconfig(current_index , fg=relevant_colour)
			current_index += 1;

		# Insert inventory divider that starts "ARMOUR" 
		self.player_inventory.insert(END, insert_inventory_divider("armour", inventory_listbox_width))
		current_index += 1;

		# Add all armour in inventory to inventory contents
		for armour_piece in player_character.armour_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(armour_piece)
			#Label equipped armour with a ">" prefix
			if(armour_piece in player_character.equipped_armour):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""

			# Verify that the whole weapon name will fit in the list box
			if(len(equippedIndicator) + len(armour_piece.name) + 1 < inventory_listbox_width - len(str(armour_piece.value))):
				self.player_inventory.insert(END, equippedIndicator + " " + armour_piece.name + " " * (inventory_listbox_width - len(equippedIndicator) - len(armour_piece.name) - 1 - len(str(armour_piece.value))) + str(armour_piece.value)) # Add value 
			else: # If it doesn't, cut it off a few characters before so that an ellipses and value can be added 
				self.player_inventory.insert(END, equippedIndicator + " " + armour_piece.name[:inventory_listbox_width - len(equippedIndicator) - 5 - len(str(armour_piece.value))] + "... " + str(armour_piece.value)) # Add value 

			# Colour text in relation to armour tier
			self.player_inventory.itemconfig(current_index , fg=relevant_colour)
			current_index += 1;

		# Insert inventory divider that starts "ITEMS" 
		self.player_inventory.insert(END, insert_inventory_divider("item", inventory_listbox_width))
		#Add all items in inventory to inventory contents
		for item in player_character.item_inventory:
			self.player_inventory.insert(END, item.name + " (" + str(player_character.item_inventory[item]) + ")" + " " * (inventory_listbox_width  - len(item.name) - 3 - len(str(player_character.item_inventory[item])) - len(str(item.value))) + str(item.value))


		# Delete existing merchant inventory
		self.merchant_inventory.delete(0, END)
		# Draw Merchants inventory contents
		self.current_merchant = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].my_merchant;
		self.merchant_inventory.insert(END, insert_inventory_divider("weapon", inventory_listbox_width))
		# Update merchant baguette quantities
		self.merchant_baguettes_quantity_display.configure(text = str(self.current_merchant.baguettes))
		current_index = 1;
		for weapon in self.current_merchant.weapon_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(weapon)

			# Verify that the whole weapon name will fit in the list box
			weapon_comparison_indicator = get_sign_as_string( ((weapon.damage * weapon.shots_per_turn * (weapon.accuracy / 100)) * (1 + weapon.critical_chance / 50) ) - ((player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100)) * (1 + player_character.equipped_weapon.critical_chance / 50)))
			if(weapon_comparison_indicator == ""):
				weapon_comparison_indicator = " "

			if(len(weapon.name) + 1 < inventory_listbox_width - len(str(weapon.value))):
				self.merchant_inventory.insert(END, weapon.name + " " + weapon_comparison_indicator + " " * (inventory_listbox_width - len(weapon.name) - 2 - len(str(weapon.value))) + str(weapon.value))
			else:
				# If not, clip off the end and add elipses 
				self.merchant_inventory.insert(END, weapon.name[:inventory_listbox_width - 7 - len(str(weapon.value))] + " " + weapon_comparison_indicator + " " + "... " + str(weapon.value))

			# Colour text in relation to weapon tier
			self.merchant_inventory.itemconfig(current_index , fg=relevant_colour)
			current_index += 1;

		self.merchant_inventory.insert(END, insert_inventory_divider("armour", inventory_listbox_width))
		current_index += 1;

		# Add all armour in inventory to inventory contents
		for armour_piece in self.current_merchant.armour_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(armour_piece)

			# Transform type of armour into index
			if(armour_piece.description == "helmet"):
				armour_description_id = 0;
			elif(armour_piece.description == "chest_piece"):
				armour_description_id = 1;
			elif(armour_piece.description == "left_arm"):
				armour_description_id = 2;
			elif(armour_piece.description == "right_arm"):
				armour_description_id = 3;
			elif(armour_piece.description == "left_leg"):
				armour_description_id = 4;
			else:
				armour_description_id = 5;

			armour_comparison_indicator = get_sign_as_string(armour_piece.protection - player_character.equipped_armour[armour_description_id].protection)
			if(armour_comparison_indicator == ""):
				armour_comparison_indicator = " "

			# Verify that the whole weapon name will fit in the list box
			if(len(armour_piece.name) + 1 < inventory_listbox_width - len(str(armour_piece.value))):
				self.merchant_inventory.insert(END, armour_piece.name + " " + armour_comparison_indicator + " " * (inventory_listbox_width - 2 - len(armour_piece.name) - len(str(armour_piece.value))) + str(armour_piece.value)) # Add value 
			else: # If it doesn't, cut it off a few characters before so that an ellipses and value can be added 
				self.merchant_inventory.insert(END, armour_piece.name[:inventory_listbox_width - 7 - len(str(armour_piece.value))] + " " + armour_comparison_indicator + " " + "... " + str(armour_piece.value)) # Add value 

			# Colour text in relation to armour tier
			self.merchant_inventory.itemconfig(current_index , fg=relevant_colour)
			current_index += 1;

		self.merchant_inventory.insert(END, insert_inventory_divider("item", inventory_listbox_width))
		current_index += 1;

		#Add all items in inventory to inventory contents
		for item in self.current_merchant.item_inventory:
			self.merchant_inventory.insert(END, item.name + " (" + str(self.current_merchant.item_inventory[item]) + ")" + " " * (inventory_listbox_width  - len(item.name) - 3 - len(str(self.current_merchant.item_inventory[item])) - len(str(item.value))) + str(item.value))


	def erase_merchant_screen(self):
		self.title.place_forget()
		self.exit_from_merchant_button.place_forget();
		self.buy_button.place_forget();
		self.sell_button.place_forget();
		self.player_inventory.place_forget();
		self.merchant_inventory.place_forget();
		self.player_baguettes_quantity_display.place_forget();
		self.baguettes_icon_1.place_forget();
		self.merchant_baguettes_quantity_display.place_forget();
		self.baguettes_icon_2.place_forget();
		self.player_baguette_title.place_forget();
		self.merchant_baguette_title.place_forget();

	def enable_enemy_targeting(self):
		if(player_character.health > 0):
			self.target_head_button.configure(state = NORMAL, bg = "light grey")
			self.target_torso_button.configure(state = NORMAL, bg = "light grey")
			self.target_arm_left_button.configure(state = NORMAL, bg = "light grey")
			self.target_arm_right_button.configure(state = NORMAL, bg = "light grey")
			self.target_leg_left_button.configure(state = NORMAL, bg = "light grey")
			self.target_leg_right_button.configure(state = NORMAL, bg = "light grey")



class InventoryWindow():

	def __init__(self):

		# Initialisation of inventory widgets 
		self.title = Label(inventory_frame, text='INVENTORY', font=("Courier", round(14 * game_res_scale)), bg="#D3D3D3")
		self.action_button = Button(inventory_frame, fg="blue", text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(inventory_frame, fg="blue", text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:loadMapFrame())
		self.inventory_button = Button(inventory_frame, fg="blue", text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED, bg="#D3D3D3", relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(inventory_frame, fg="blue", text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", bg="#D3D3D3", command=lambda:load_stats_frame())
		self.scrollbar = Scrollbar(inventory_frame)
		self.scrollbar.pack(side=LEFT, fill=Y)
		self.inventory_contents = Listbox(inventory_frame, yscrollcommand=self.scrollbar.set, height = 18 , width = 52, bg="#D3D3D3", font=("Courier", math.ceil(14 * game_res_scale)))
		self.inventory_drop_button = Button(inventory_frame, text = "Drop", width = 40, height = 1, bg="#D3D3D3", font=("Courier", math.ceil(9 * game_res_scale)), command = lambda:player_character.drop_item())
		self.equip_item_button = Button(inventory_frame, text = "Equip", width = 40, height = 1, bg="#D3D3D3", font=("Courier", math.ceil(9 * game_res_scale)), command = lambda:player_character.equip_item() )
		self.scrollbar.config(command=self.inventory_contents.yview)
		self.item_description_graphic = Text(inventory_frame, height = 1, width = round(8 * (0.5 + game_res_scale / 2)),  relief = 'flat', bg="#D3D3D3", font=("Courier", round(10)) )
		self.item_description = Text(inventory_frame, height = 9, width = 32, relief = 'flat', bg="#D3D3D3", font=("Courier", math.ceil(10 * game_res_scale)) )
		self.carry_weight_indicator = Label(inventory_frame, fg="#C5B358", bg="#333", text = str(player_character.current_carry_weight) + "/" + str(player_character.max_carry_weight), font=("Courier", round(14 * game_res_scale)))
		self.player_baguettes_indicator = Label(inventory_frame,  text = str(player_character.baguettes), fg = "#C5B358", bg="#333",  font=("Courier", round(16 * game_res_scale)))
		self.baguette_image = ImageHandling.get_UI_sprite("baguette_icon", game_res_scale)
		self.carry_weight_image = ImageHandling.get_UI_sprite("weight_icon", game_res_scale)
		self.baguettes_icon = Label(inventory_frame, image = self.baguette_image, bg="#333")
		self.carry_weight_icon = Label(inventory_frame, image = self.carry_weight_image, bg="#333")


		# Customisation of inventory widgets 
		self.item_description_graphic.configure(state = DISABLED)
		
		# Placement of inventory widgets 
		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.inventory_contents.place(x =16 , y = 50 * game_res_scale)
		self.inventory_drop_button.place(x = 16, y = 448 * game_res_scale)
		self.equip_item_button.place(x = 16 + (286 * game_res_scale), y = 448 * game_res_scale)
		self.carry_weight_indicator.place(x = 62 * game_res_scale, y = 525 * game_res_scale)
		self.player_baguettes_indicator.place(x = 210 * game_res_scale, y = 524 * game_res_scale)
		self.baguettes_icon.place(x = 175 * game_res_scale, y = 523 * game_res_scale)
		self.carry_weight_icon.place(x = 32 * game_res_scale, y = 522 * game_res_scale)

		# Used as a temporary store of selected item
		self.last_selected_item = None;
		self.last_selected_item_index = 0;

		if("1280" in game_resolution):
			self.inventory_contents.configure(width = 54)


class MapWindow():

	def __init__(self):
		# Initialisation of map widgets 
		self.title = Label(map_frame, text='MAP', bg = "#D3D3D3", font=("Courier", round(14 * game_res_scale)))
		self.action_button = Button(map_frame, text='Action', fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(map_frame, text='Map', fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED, relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(map_frame, text='Inventory', fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(map_frame, text="Stats", fg="blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:load_stats_frame())
		self.zoom_button = Button(map_frame, text="Zoom In", fg = "blue", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:self.change_zoom())
		self.zoom = "out";


		# Placement of map widgets
		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.zoom_button.place(x = 0, y = 0)

		# Disable teleporting to boss location
		game_map[1][8][0].my_button_container.button.configure(state = DISABLED)
		game_map[0][8][0].my_button_container.button.configure(state = DISABLED)


	def clear_all_button_locations(self):
		# Clear all previously placed buttons 
		for game_branch in game_map:
				for location_set in game_branch:
					for location in location_set:
						location.my_button_container.button.place_forget()

	def change_zoom(self):
		if(self.zoom == "out"):
			self.zoom = "in";
			self.zoom_button.configure(text = "Zoom Out")
		else:
			self.zoom = "out";
			self.zoom_button.configure(text = "Zoom In")

		self.clear_all_button_locations();
		loadMapFrame();


class StatsWindow():

	def __init__(self):
		# Initialisation of stats widgets
		self.title = Label(stats_frame, text="STATS", bg ="#D3D3D3", font=("Courier", round(14 * game_res_scale)))
		self.action_button = Button(stats_frame, fg="blue", text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(stats_frame, fg="blue", text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(stats_frame, fg="blue", text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(stats_frame, fg="blue", text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED, relief="ridge", command=lambda:load_stats_frame())
		self.player_stats_display = Text(stats_frame, height = round(19), width = round(23), font=("Courier", round(12 * game_res_scale)), bg="#D3D3D3", state = DISABLED)
		self.player_image, self.player_image_width, self.player_image_height, self.player_sprite_path = ImageHandling.get_random_player_sprite(player_character.gender, game_res_scale)
		self.player_image_label = Label(stats_frame, image = self.player_image)

		# Initialise buttons to handle allocating skillpoints
		self.skillpoints_label = Label(stats_frame, text = str(player_character.unspent_skillpoints) + " Unspent Skillpoint", font=("Courier", round(14 * game_res_scale)))

		self.fortune_skill_label = Label(stats_frame, text = "Fortune", font=("Courier", round(12 * game_res_scale)))
		self.insight_skill_label = Label(stats_frame, text = "Insight", font=("Courier", round(12 * game_res_scale)))
		self.charisma_skill_label = Label(stats_frame, text = "Charisma", font=("Courier", round(12 * game_res_scale)))
		self.agility_skill_label = Label(stats_frame, text = "Agility", font=("Courier", round(12 * game_res_scale)))
		self.strength_skill_label = Label(stats_frame, text = "Strength", font=("Courier", round(12 * game_res_scale)))

		self.fortune_skill_button = Button(stats_frame, fg = "blue", text="+", width = round(4 * game_res_scale), height = round(1 * game_res_scale), relief="ridge", command=lambda:player_character.upskill("fortune"))
		self.insight_skill_button = Button(stats_frame, fg = "blue", text="+", width = round(4 * game_res_scale), height = round(1 * game_res_scale), relief="ridge", command=lambda:player_character.upskill("insight"))
		self.charisma_skill_button = Button(stats_frame, fg = "blue", text="+", width = round(4 * game_res_scale), height = round(1 * game_res_scale), relief="ridge", command=lambda:player_character.upskill("charisma"))
		self.agility_skill_button = Button(stats_frame, fg = "blue", text="+", width = round(4 * game_res_scale), height = round(1 * game_res_scale), relief="ridge", command=lambda:player_character.upskill("agility"))
		self.strength_skill_button = Button(stats_frame, fg = "blue", text="+", width = round(4 * game_res_scale), height = round(1 * game_res_scale), relief="ridge", command=lambda:player_character.upskill("strength"))
		# Initialise EXP bar widgets
		self.player_exp_label = Label(stats_frame, text = "EXP", font=("Courier", round(12 * game_res_scale)))
		self.player_exp_bar = Progressbar(stats_frame, orient = HORIZONTAL, length = 340 * game_res_scale, maximum = 25, mode = 'determinate')

		# Placement of stats widgets
		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.player_image_label.place(x = 512 * game_res_scale - self.player_image_width / 2, y = 288 * game_res_scale - self.player_image_height / 2)
		self.player_stats_display.place(x = 518 * game_res_scale + self.player_image_width / 2, y = 288 * game_res_scale - self.player_image_height / 2)


class Enemy:
	def __init__(self, name, health, armour, current_weapon, sprite, weapon_inventory, armour_inventory, item_inventory, lootable_baguettes, button_locations, attack_priority, experience, insight = 1, agility = 1, strength = 1):
		self.name = name
		self.health = health
		self.armour = armour
		if(current_weapon != None):
			self.equipped_weapon = current_weapon
		else:
			self.equipped_weapon = None
		self.sprite = sprite

		self.weapon_inventory = weapon_inventory
		self.armour_inventory = armour_inventory
		self.item_inventory = item_inventory

		self.lootable_baguettes = lootable_baguettes # Currency
		self.attack_priority = attack_priority;
		self.button_locations = button_locations;
		self.can_attack = True;
		self.experience = experience;

		self.insight = insight - 0.01;
		self.agility = agility - 0.01;
		self.strength = strength - 0.01;

		self.head = limb(self, "head")
		self.torso = limb(self, "torso")
		self.left_arm = limb(self, "left arm")
		self.right_arm = limb(self, "right arm")
		self.left_leg = limb(self, "left leg")
		self.right_leg = limb(self, "right leg")


	def takeDamage(self, initial_damage, target,  special = "n"): # Initial damage is the damage before armour value is applied
		# Special defines if there are any additional modifiers to apply (e.g. concussion rounds delay the enemy for a turn)

		if(special == "c"):
			self.can_attack = False;

		if(self.armour > 400):
			self.armour = 400 #Cap at 400 otherwise protection amount will be > 1 resulting in attacks dealing negative damage (essentially healing you)

		protection_amount = ((math.log2(self.armour + 64) / 3) * 100 - 200)	
		
		damage_dealt = random.randrange(round(initial_damage * 0.8), round(initial_damage * 1.2)) * (1-protection_amount/100)
		if(special == "ap"):
			damage_dealt *= 1.5;

		if(damage_dealt < 0):
			damage_dealt = 0;
		else:
			damage_dealt = round(damage_dealt)
		self.health = self.health - damage_dealt;

		if(target == "head"):
			self.head.take_damage(damage_dealt)
		elif(target == "leftarm"):
			self.left_arm.take_damage(damage_dealt)
		elif(target == "rightarm"):
			self.right_arm.take_damage(damage_dealt)
		elif(target == "leftleg"):
			self.left_leg.take_damage(damage_dealt)
		elif(target == "rightleg"):
			self.right_leg.take_damage(damage_dealt)


		action_window.main_textbox.config(state=NORMAL) #Allow writing to main text box
		output_to_action_text(" " + str(damage_dealt) + " damage", True)
		action_window.main_textbox.yview(END) #Auto scroll main text box when new text is added
		action_window.main_textbox.config(state=DISABLED) #Disable player being able to manipulate text in main text box


		if(self.health <= 0):
			self.die()

	def deal_damage(self):
		
		if(self.health > 0):
			for i in range(0, self.equipped_weapon.shots_per_turn):
				action_window.main_textbox.config(state=NORMAL)
				player_attack_hit = random.randrange(1, 101) <= (self.equipped_weapon.accuracy - (player_character.agility / 2)) * self.insight #Calculate if attack hit based on players current weapon accuracy
				if(player_attack_hit == True): 
					if(player_character.health > 0):
						if(self.equipped_weapon.weapon_type == "ranged"):
							action_frame.after(random.randrange(350, 500), lambda:audio_handler.play_sound_effect(0.6, self.equipped_weapon.attack_file_data[0], self.equipped_weapon.attack_file_data[1]))
						else:
							if("chainsaw" in self.equipped_weapon.name.lower()):
								action_frame.after(random.randrange(350, 500), lambda:audio_handler.play_sound_effect(0.5, "Hit_Chainsaw"))
							else:
								action_frame.after(random.randrange(350, 500), lambda:audio_handler.play_sound_effect(0.9, "Hit_Melee"))
						if(random.randrange(1, 101) <= self.equipped_weapon.critical_chance): #Hit did crit
							output_to_action_text(self.name.split(" ")[0] + " crit you for", False) 

							if(self.equipped_weapon.weapon_type == "ranged"):
								player_character.take_damage(self.equipped_weapon.damage * 1.5) #Apply damage * 2 due to crit
							else:
								player_character.take_damage(self.equipped_weapon.damage * 1.5 * self.strength) #Apply damage * 2 due to crit
						else:

							output_to_action_text(self.name.split(" ")[0] + " hit you for", False)
							if(self.equipped_weapon.weapon_type == "ranged"):
								player_character.take_damage(self.equipped_weapon.damage * 0.6 ) #Apply standard weapon damage 
							else:
								player_character.take_damage(self.equipped_weapon.damage * 0.6 * self.strength) #Apply standard weapon damage 
				else:
					action_frame.after(random.randrange(350, 500), lambda:audio_handler.play_sound_effect(1, "Miss"))
					#Hit missed
					output_to_action_text(self.name.split(" ")[0] + " missed", True)
			self.equipped_weapon.attacked_as_enemy();
			action_window.main_textbox.config(state=DISABLED)
		loadActionFrame(Adversary)

	def die(self):
		
		# Output text that enemy has died, randomised from file in gamedata
		script_dir = os.path.dirname(__file__)
		death_text = FileInterface.line_from_file(script_dir + "\\GameData\\death_text.txt", random.randrange(0, FileInterface.length_of_file(script_dir + "\\GameData\\death_text.txt")))
		output_to_action_text(death_text[0] + " " + self.name, True)
		output_to_action_text("+" + str(self.experience) + " EXP", True)
		# Play random death sound  
		action_frame.after(random.randrange(400, 450), lambda:audio_handler.play_dialogue(0.8, "Death"))
		# Give player XP
		player_character.add_experience(self.experience)


		# Change Window back to no enemy state
		self.name = ""
		self.health = 0
		self.damage = 0
		self.sprite = noEnemyIMG

		# Progress player each time they kill an enemy
		player_character.game_progression += 1;
		# Initiate looting of enemy
		time_before_looting = random.randrange(1000,2000)
		action_frame.after(time_before_looting, lambda:loot_enemy(self.weapon_inventory, self.armour_inventory, self.item_inventory, self.lootable_baguettes))
		action_frame.after(time_before_looting, lambda:action_window.enable_navigation())

	def drop_item(self, index):
		item_to_drop_index = action_window.loot_window.curselection() #Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" also counts as an index)
		try:
			item_to_drop_index = item_to_drop_index[0]
		except Exception as e:
			return

		item_to_drop = self.get_item_in_inventory(item_to_drop_index)

		if(item_to_drop != None):
			#Delete Item and then check if it was the currently equipped weapon/armour by the player
			if(item_to_drop[1] == "weapon"):
				#Drop weapon
				if(self.weapon_inventory[item_to_drop[0]] == 1):
					del self.weapon_inventory[item_to_drop[0]]
				else:
					self.weapon_inventory[item_to_drop[0]] -= 1

			if(item_to_drop[1] == "armour"):
				if(self.armour_inventory[item_to_drop[0]] == 1):
					del self.armour_inventory[item_to_drop[0]]
				else:
					self.armour_inventory[item_to_drop[0]] -= 1

			if(item_to_drop[1] == "item"):
				if(self.item_inventory[item_to_drop[0]] == 1):
					del self.item_inventory[item_to_drop[0]]
				else:
					self.item_inventory[item_to_drop[0]] -= 1


	def get_item_in_inventory(self, index):
		item_iterator = index + 1
		if(self.weapon_inventory != None):
			weapon_inv_length = len(self.weapon_inventory)
		else:
			weapon_inv_length = 0;
		if(self.armour_inventory != None):
			armour_inv_length = len(self.armour_inventory)
		else:
			armour_inv_length = 0;
		if(self.item_inventory != None):
			item_inv_length = len(self.item_inventory)
		else:
			item_inv_length = 0;


		item_iterator -= 1
		index -= 1


		if(item_iterator > weapon_inv_length): #Item is not in weapons inventory
			item_iterator -= weapon_inv_length + 1 #Add one because of the divider we have in the text box
			index -= weapon_inv_length + 1 #Add one because of the divider we have in the text box

			if(item_iterator > armour_inv_length): #Item is not in armour inventory
				item_iterator -= armour_inv_length + 1 #Add one because of the divider we have in the text box
				index -= armour_inv_length + 1 #Add one because of the divider we have in the text box

				#Item must be in items inventory
				i = 0
				for key in self.item_inventory:
					if(i == index):
						return [list(self.item_inventory.keys())[i], "item" ]
					i += 1

			else: #Item is in armour inventory
				i = 0
				for key in self.armour_inventory:
					if(i == index):
						return [list(self.armour_inventory.keys())[i], "armour"]
					i += 1

		else: #Item is in weapons inventory
			i = 0
			for key in self.weapon_inventory:
				if(i == index):
					return [list(self.weapon_inventory.keys())[i], "weapon"]
				i += 1

class limb:
	def __init__(self, parent, limb_name):
		self.parent = parent;
		self.limb_id = limb_name;
		health_factor = 3/5;
		self.health = round(parent.health * health_factor) + random.randrange(round(-(parent.health /5)), round((parent.health /5) + 1));
		self.status = "Healthy";

	def take_damage(self, damage):
		self.health -= damage;

		if(self.health <= 0):
			action_frame.after(1000, lambda:self.cripple())
		

	def cripple(self):
		if(self.parent.health > 0 and self.status == "Healthy"):
			self.status = "Crippled"
			output_to_action_text("You have crippled " + self.parent.name + "'s " + self.limb_id + ".", True)

			# For each type of limb that can be crippled, reduce corresponding stat by a random amount
			if(self.limb_id == "head"):
				reduction_value = random.randrange(12, 38) / 100
				self.parent.insight -= reduction_value;
				output_to_action_text(self.parent.name.split(" ")[0] + "'s insight has been reduced by " + str(round(reduction_value * 100)) + "%", True)
			elif(self.limb_id == "left arm" or self.limb_id == "right arm"):
				reduction_value = random.randrange(12, 38) / 100
				self.parent.strength -= reduction_value;
				output_to_action_text(self.parent.name.split(" ")[0] + "'s strength has been reduced by " + str(round(reduction_value * 100)) + "%", True)
			elif(self.limb_id == "left leg" or self.limb_id == "right leg"):
				reduction_value = random.randrange(12, 38) / 100
				self.parent.agility -= reduction_value;
				output_to_action_text(self.parent.name.split(" ")[0] + "'s agility has been reduced by " + str(round(reduction_value * 100)) + "%", True)



class AudioHandler:

	def __init__(self):
		# initialize the mixer module
		mixer.init()
		# Reserve audio channel 0,1,2 for important events/ Sound effects
		mixer.set_reserved(0)
		mixer.set_reserved(1)
		mixer.set_reserved(2)
		# Reserve audio channel 3 for dialogue 
		mixer.set_reserved(3)
		# Reserve audio channel 6,7,8 for Music 
		mixer.set_reserved(6)
		mixer.set_reserved(7)
		mixer.set_reserved(8)

		# Initialise variables to know where to look for audio files
		self.script_dir = os.path.dirname(__file__) #<-- absolute directory this file is in
		self.target_path = "AudioFiles"
		self.audio_folder = os.path.join(self.script_dir, self.target_path) # Create path for the audio folder and store as variable 'audio_folder'


	def play_sound_effect(self, volume, tertiary_folder, file_name=None, quaternary_folder = None):
		desired_sub_folder = "Sound_Effects"
		# If a particular file is specified, get that file from appropriate directory 
		if(file_name != None):
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + file_name + ".wav" # Locate path of desired file to play
		else: # If no file is specified, play random file from that directory
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + random.choice(os.listdir(self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder))

		try:
			# Check to see which channel is not busy and assign new audio to that
			if(mixer.Channel(0).get_busy() == False):
				mixer.Channel(0).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(0).set_volume(volume)	# Modify audio to correct levels 
			elif(mixer.Channel(1).get_busy() == False):
				mixer.Channel(1).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(1).set_volume(volume)	# Modify audio to correct levels 
			elif(mixer.Channel(2).get_busy() == False):
				mixer.Channel(2).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(2).set_volume(volume)	# Modify audio to correct levels 
			else:
				#If all channels are taken, queue audio to a random audio channel
				random_channel = random.choice([0,1,2])
				mixer.Channel(random_channel).queue(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(random_channel).set_volume(volume) # Modify audio to correct levels 

		except Exception as exc:
			print("Failed", exc)
			return "Failed: ", exc
		print("Success")
		return "Success"

	def play_dialogue(self, volume, tertiary_folder, file_name=None, quaternary_folder = None):
		desired_sub_folder = "Dialogue"
		# If a particular file is specified, get that file from appropriate directory 
		if(file_name != None):
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + file_name + ".wav" # Locate path of desired file to play
		else: # If no file is specified, play random file from that directory
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + random.choice(os.listdir(self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder))
		try:
			# Check to see which channel is not busy and assign new audio to that
			if(mixer.Channel(3).get_busy() == False):
				mixer.Channel(3).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel	
				mixer.Channel(3).set_volume(volume)	# Modify audio to correct levels 
			else:
				#If all channels are taken, queue audio to a random audio channel
				mixer.Channel(3).queue(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(3).set_volume(volume) # Modify audio to correct levels 
		except Exception as exc:
			return "Failed ", exc
		return "Success"

	def play_music(self, volume, tertiary_folder, file_name=None, quaternary_folder = None):
		desired_sub_folder = "Music"
		# If a particular file is specified, get that file from appropriate directory 
		if(file_name != None):
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + file_name + ".wav" # Locate path of desired file to play
		else: # If no file is specified, play random file from that directory
			file_to_play = self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder + "\\" + random.choice(os.listdir(self.audio_folder + "\\" + desired_sub_folder + "\\" + tertiary_folder))
		
		try:
			# Check to see which channel is not busy and assign new audio to that
			if(mixer.Channel(6).get_busy() == False):
				mixer.Channel(6).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel	
				mixer.Channel(6).set_volume(volume)	# Modify audio to correct levels 
			elif(mixer.Channel(7).get_busy() == False):
				mixer.Channel(7).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel	
				mixer.Channel(7).set_volume(volume)	# Modify audio to correct levels 
			elif(mixer.Channel(8).get_busy() == False):
				mixer.Channel(8).play(mixer.Sound(file_to_play)) # Play sound on respective audio channel	
				mixer.Channel(8).set_volume(volume)	# Modify audio to correct levels
			else:
				#If all channels are taken, queue audio to a random audio channel
				random_channel = random.choice([6,7,8])
				mixer.Channel(random_channel).queue(mixer.Sound(file_to_play)) # Play sound on respective audio channel
				mixer.Channel(random_channel).set_volume(volume) # Modify audio to correct levels 
		except Exception as exc:
			return "Failed ", exc
		return "Success"

	def set_volume(channel, volume):
		channel = channel.lower()
		if(channel == "SE"): # Sound effects channel
			mixer.Channel(0).set_volume(volume)
			mixer.Channel(1).set_volume(volume)
			mixer.Channel(2).set_volume(volume)
		if(channel == "D"): # Dialogue channel
			mixer.Channel(3).set_volume(volume)
			mixer.Channel(4).set_volume(volume)
			mixer.Channel(5).set_volume(volume)
		if(channel == "M"): # Music channel
			mixer.Channel(6).set_volume(volume)
			mixer.Channel(7).set_volume(volume)
			mixer.Channel(8).set_volume(volume)



if __name__ == "__main__":
	from Conventions import * # Import all of my quick conventions
	import os, random, time, schedule, math, sys, pickle
	import MyDictionary, eGraphh, TkinterResolution, ElapsedTime, ImageHandling, CharacterSetup, ObjectHandling, WADInitialiser, FileInterface # My own modules 
	from tkinter import * # GUI 
	from PIL import ImageTk, Image # Handling images
	from pygame import mixer  # Handling audio
	from tkinter.messagebox import showinfo

	# Enable multi-threaded computing by creating a class to instantiate a new thread
	# Had to move this inside of __main__ to avoid multi-threaded instability issues with tkinter 
	class new_thread(threading.Thread):
		def __init__(self):
			# Initialise thread 
			threading.Thread.__init__(self) 
			self.setDaemon(True)
			self.start()

		#def callback(self):
		#	global root
		#	root.quit()  # callback, since without this the program exits with an error when the Tkinter window is closed by the user.

		def run(self):
			while True:
				if("normal" == root.state() and self.running == True): # Check if python root window is open
					schedule.run_pending() # Update schedule tasks
				if("normal" != root.state()):
					sys.exit() # Otherwise, exit self
					print("Closed")
				

	game_resolution = TkinterResolution.get_user_resolution("1024x576", "1280x720", "1920x1080", "2560x1440") # Get  the desired resolution for the game window 
	game_res_axes = game_resolution.split("x") # Get the horizontal and vertical pixels of the window
	game_res_scale = int(game_res_axes[0]) / 1024 # Used to scale all widgets in window

	player_stats = CharacterSetup.get_character_customisation(); # Get player's custom character
	#player_image = 

	WADInitialiser.initialise_wads(); # Intialise wads

	ElapsedTime.initialise_elapsed_time() # Start tracking elapsed time
	audio_handler = AudioHandler()        # Create audio handling object 
	item_description_schedule_created = False;
	char_q = []

	class merchant():
		def __init__(self, name, tier, index):

			self.name = name;
			self.baguettes = 50 * tier * (1 + ((tier > 2) * index)) + random.randrange(1, 26 * tier)
			self.weapon_inventory, self.armour_inventory, self.item_inventory, baguettes = ObjectHandling.generate_loot(random.randrange(2,7), random.randrange(2,7), random.randrange(2,7), tier * 2 * index, 30, tier, True)

		def initialise(self):
			# Lower prices based upon players' charisma stat
			for weapon in self.weapon_inventory:
				weapon.value = round( weapon.value * (1-(player_character.charisma * 1.5 / 100)) )
				if(weapon.value <= 0):
					weapon.value = 1;
			for armour_piece in self.armour_inventory:
				armour_piece.value = round( armour_piece.value * (1-(player_character.charisma*1.5 / 100)) )
				if(armour_piece.value <= 0):
					armour_piece.value = 1;


	class town():
		def __init__(self, my_button_container, name, tier, index):
			self.boss = False
			script_dir = os.path.dirname(__file__)
			self.button_x = 0;
			self.button_y = 0;
			self.name = FileInterface.line_from_file(script_dir + "\\GameData\\location_names.txt", random.randrange(0, FileInterface.length_of_file(script_dir+"\\GameData\\location_names.txt")))[0];
			self.cleared = False;
			self.my_button_container = my_button_container;
			self.starting_location = False;
			self.my_merchant = merchant(MyDictionary.get_name("male", True, False, False), tier, index)

			# Assign an image to this location
			self.image = random.choice(town_images)



	class map_button_container():
		def __init__(self, button, location):
			# Initialise x and y co-ords as 0 as they will be set shortly after instantiation
			self.x = 0;
			self.y = 0;
			self.button = button;
			self.location = location;

			self.button.configure(command = lambda:fast_travel(self.location))


	class point_of_interest():
		def __init__(self, my_button_container, name, text, encounter_type = "enemy", encounter_tier = 1, starting_location = False, boss = False):
			self.boss = boss
			script_dir = os.path.dirname(__file__)
			if(not boss):
				self.name = FileInterface.line_from_file(script_dir + "\\GameData\\location_names.txt", random.randrange(0, FileInterface.length_of_file(script_dir+"\\GameData\\location_names.txt")))[0];
				self.image = None;
			else:
				# Set the last town (before the boss fight) to the end_image sprite
				self.name = "The Masters dojo"
				self.ending_location = True
				self.image = end_image;

			self.text = text;
			self.encounter_type = encounter_type;
			self.encounter_tier = encounter_tier;
			self.cleared = False;
			self.my_button_container = my_button_container;
			self.starting_location = starting_location;

			# Assign an image to this location
			if(self.image == None):
				self.image = random.choice(location_images)




		def generate_encounter(self, game_resolution, player_character, boss = False):
			
			if(self.encounter_type.lower() == "enemy"):
				if(not boss):
					# Standard enemy encounter
					enemy_data =  ObjectHandling.create_enemy(game_res_scale, player_character.game_progression, player_character.towns_discovered, player_character.fortune, None, self.encounter_tier)
					self.encounter = Enemy(enemy_data[0], enemy_data[1], enemy_data[2], enemy_data[3], enemy_data[7], enemy_data[4], enemy_data[5], enemy_data[6], enemy_data[8], enemy_data[10], False, random.randrange(5 + player_character.game_progression, 13 + player_character.game_progression * 2 + self.encounter_tier ** 2))
				else:
					script_dir = os.path.dirname(__file__)
					# Boss encounter
					if(FileInterface.length_of_file(script_dir + "\\GameData\\CharacterData\\player_data.txt") > 6):
						# Most likely to contain relevant data to construct a player (if it hasnt been tampered with!)
						enemy_data = FileInterface.file_data(script_dir + "\\GameData\\CharacterData\\player_data.txt", return_type = "list", file_type = "lbl") # Pull data from text file and return a list of line-by-line values
						with open(script_dir + "\\GameData\\CharacterData\\weapon_data.txt", 'rb') as weapon_data_file:
							enemy_weapon = pickle.load(weapon_data_file) # Extract the weapon object from the text file
						enemy_sprite = ImageHandling.get_player_sprite(script_dir + enemy_data[3][0], game_res_scale) # Extract enemy sprite from text file

						enemy_button_locations = enemy_data[4][0].split(';') # Extract location of buttons from text file
						for i in range(0, len(enemy_button_locations)):
							enemy_button_locations[i] = enemy_button_locations[i].split(',') 
							enemy_button_locations[i][0] = int(enemy_button_locations[i][0])
							enemy_button_locations[i][1] = int(enemy_button_locations[i][1])
						self.encounter = Enemy(enemy_data[0][0], int(enemy_data[1][0]), int(enemy_data[2][0]), enemy_weapon, enemy_sprite, None, None, None, 999, enemy_button_locations, False, 99, insight = 1 + int(enemy_data[5][0]) / 100, agility = 1 + int(enemy_data[6][0]) / 100, strength = 1 + int(enemy_data[7][0]) / 100)
						#name, health, armour, current_weapon, sprite, weapon_inventory, armour_inventory, item_inventory, lootable_baguettes, button_locations, attack_priority, experience):

					else:
						# If no relevant data, just generate a random encounter - most likely first playthrough
						enemy_data =  ObjectHandling.create_enemy(game_res_scale, player_character.game_progression + 20, player_character.towns_discovered, player_character.fortune, None, self.encounter_tier)
						self.encounter = Enemy(enemy_data[0], enemy_data[1], enemy_data[2], enemy_data[3], enemy_data[7], enemy_data[4], enemy_data[5], enemy_data[6], enemy_data[8], enemy_data[10], False, random.randrange(5 + player_character.game_progression, 13 + player_character.game_progression * 2 + self.encounter_tier ** 2))

			elif(self.encounter_type.lower() == "ambush"):
				# Enemy encounter where the enemy attacks first 
				enemy_data =  ObjectHandling.create_enemy(game_res_scale, player_character.game_progression, player_character.towns_discovered, player_character.fortune, None, self.encounter_tier)
				self.encounter = Enemy(enemy_data[0], enemy_data[1], enemy_data[2], enemy_data[3 ], enemy_data[7], enemy_data[4], enemy_data[5], enemy_data[6], enemy_data[8], enemy_data[10], True, random.randrange(5 + player_character.game_progression, 13 + player_character.game_progression * 2 + self.encounter_tier ** 2))
			elif(self.encounter_type.lower() == "loot"):
				# Tell player scenario
				script_dir = os.path.dirname(__file__) #<-- absolute directory this file is in
				scenario_text_index = random.randrange(0, FileInterface.length_of_file(script_dir + "\\GameData\\encounters_loot.txt"), True)
				scenario_text = FileInterface.line_from_file(script_dir + "\\GameData\\encounters_loot.txt", scenario_text_index)#random.randrange(0, FileInterface.length_of_file(script_dir + "\\GameData\\encounters_loot.txt") + 1, True))
				if("service station" in scenario_text[0]):
					self.image = service_station_image;
				output_to_action_text("You " + scenario_text[0], True)
				current_tier = self.encounter_tier;


	
	def calculate_path_iterations(x, middle, branch_id, direction, d_middle, d_edge_left, d_edge_right):

		max_path_iterations = 0

		if(branch_id == 0):
			if("right" in direction):
				if("heavy" in direction):
					max_path_iterations = d_middle / 30;  # Change this if path is going outside boundaries
				elif("moderate" in direction):
					max_path_iterations = d_middle / 18;  # Change this if path is going outside boundaries
				else:
					max_path_iterations = d_middle / 12;  # Change this if path is going outside boundaries
			elif("left" in direction):
				if("heavy" in direction):
					max_path_iterations = d_edge_left / 30;  # Change this if path is going outside boundaries
				elif("moderate" in direction):
					max_path_iterations = d_edge_left / 18;  # Change this if path is going outside boundaries
				else:
					max_path_iterations = d_edge_left / 12;  # Change this if path is going outside boundaries
			else:
				# Straight
				max_path_iterations = 12;
		else:
			if("right" in direction):
				if("heavy" in direction):
					max_path_iterations = d_edge_right / 30;  # Change this if path is going outside boundaries
				elif("moderate" in direction):
					max_path_iterations = d_edge_right / 18;  # Change this if path is going outside boundaries
				else:
					max_path_iterations = d_edge_right / 12;  # Change this if path is going outside boundaries
			elif("left" in direction):
				if("heavy" in direction):
					max_path_iterations = d_middle / 30;  # Change this if path is going outside boundaries
				elif("moderate" in direction):
					max_path_iterations = d_middle / 18;  # Change this if path is going outside boundaries
				else:
					max_path_iterations = d_middle / 12;  # Change this if path is going outside boundaries
			else:
				# Straight
				max_path_iterations = 12;

		# Add rounding to iterations
		max_path_iterations = int(round(max_path_iterations))

		return max_path_iterations

	
	def get_path_trend(middle, current_x, current_y, branch_id):
		path_trends_left = ["heavy_left", "moderate_left", "gentle_left"]
		path_trends_right = ["heavy_right", "moderate_right", "gentle_right"]
		path_trends_other = ["straight"]

		distance_to_middle = abs(middle - current_x);
		distance_to_edge_left = abs(current_x - 0)
		distance_to_edge_right = abs(current_x - int(game_res_axes[0]))
		normalised_middle_score = distance_to_middle / game_res_scale;
		
		path_options_weighted = []
		# Make these intelligently randomised

		if(branch_id == 0): # Left branch
			weighting_to_middle = int(abs(middle - normalised_middle_score) / (middle / 100))
			weighting_to_edge_left = int(100 - weighting_to_middle);

			# Populate a list of all possible options for the path with weighting (130 in total)
			for x in range(0, 30):
				# Populate with 30 straight options
				path_options_weighted.append(path_trends_other[0])
			for x in range(0, weighting_to_edge_left):
				# Populate with right options to steer away from edge of wall
				path_options_weighted.append(random.choice(path_trends_right))
			for x in range(0, weighting_to_middle):
				# Populate with right options to steer away from middle (left)
				path_options_weighted.append(random.choice(path_trends_left))


		else: # Right branch
			weighting_to_middle = int(abs(middle - normalised_middle_score) / (middle / 100))
			weighting_to_edge_right = int(100 - weighting_to_middle);

			# Populate a list of all possible options for the path with weighting (130 in total)
			for x in range(0, 30):
				# Populate with 30 straight options
				path_options_weighted.append(path_trends_other[0])
			for x in range(0, weighting_to_edge_right):
				# Populate with left options to steer away from edge of frame
				path_options_weighted.append(random.choice(path_trends_left))
			for x in range(0, weighting_to_middle):
				# Populate with right options to steer away from middle (right)
				path_options_weighted.append(random.choice(path_trends_right))


		# Get path shape and iterations for path to last for
		path_shape = random.choice(path_options_weighted)
		max_path_iterations = calculate_path_iterations(current_x, middle, branch_id, path_shape, distance_to_middle, distance_to_edge_left, distance_to_edge_right)

		# Ensure a path that can span for more than 3 locations is selected
		while(max_path_iterations <= 3):
			path_shape = random.choice(path_options_weighted)
			max_path_iterations = calculate_path_iterations(current_x, middle, branch_id, path_shape, distance_to_middle, distance_to_edge_left, distance_to_edge_right)

		if(max_path_iterations < 20):
			path_iterations = random.randrange(4, max_path_iterations + 1)
		else:
			path_iterations = random.randrange(4, 20)

		return path_shape, path_iterations;


	def generate_map(town_count, branch_id):
		# Initialise game_map array
		game_map = [];

		# Define scaling of difficulty
		towns_required_for_tier_2 = 2
		towns_required_for_tier_3 = 5

		size = 0;

		# Define encounter chances
		chance_for_enemy = 65;
		chance_for_loot = 15;
		chance_for_ambush = 15;
		chance_for_fork = 5;


		# Define array for all possible encounters 
		encounters = []
		# Populate encounter array 
		for x in range(0, chance_for_enemy):
			encounters.append("enemy")
		for x in range(0, chance_for_loot):
			encounters.append("loot")
		for x in range(0, chance_for_ambush):
			encounters.append("ambush")
		for x in range(0, chance_for_fork):
			encounters.append("fork")

		# Populate array with sub-arrays correlating to the amount of towns to create
		for i in range(0, town_count):
			game_map.append([])

			# Scramble array to further enhance randomness
			random.shuffle(encounters)
			
			# Get the current tier for all encounters after this town
			if (i + 1 > towns_required_for_tier_3):
				current_tier = 3;
			elif(i + 1 > towns_required_for_tier_2):
				current_tier = 2;
			else:
				current_tier = 1;
			for j in range(0, random.randrange(2 + math.floor(i/3), 3 + i)):

				# Randomise chance for each encounter type 
				if(i == 0 and j == 0):
					# Make the first location always an enemy encounter
					this_encounter = "enemy"
				else:
					this_encounter = random.choice(encounters)

				# Define location within game map of each location
				current_location = (branch_id, i, j)
				# Create button and point of interest
				this_location_button = Button(map_frame, width = round(game_res_scale + 0.4 + math.floor(game_res_scale / 1.5)), height = round(game_res_scale), text = this_encounter[0].upper(), command = lambda:fast_travel(-1))  
				this_button_container = map_button_container(this_location_button, current_location)

				this_POI = point_of_interest(this_button_container, "ENCOUNTER", "This is an enemy", this_encounter, current_tier)

				
				game_map[i].append(this_POI) # Place random encounters between towns
				size += 1; # Increment size by one

			current_location = (branch_id, i, j)
			
			this_town_button = Button(map_frame, width = round(game_res_scale + 0.4 + math.floor(game_res_scale / 1.5)), height = round(game_res_scale), text = "T" + str(i + 1), command = lambda:fast_travel(current_location))
		
			this_button_container = map_button_container(this_town_button, current_location)
			game_map[i].append(town(this_button_container, "Town %s" % i, current_tier, i)); # Place Towns in Map
			size += 1; # Increment size by one

		# Add in final showdown/boss location manually

		# Define location within game map of each location
		current_location = (branch_id, i + 1, 0)
		# Create button and point of interest
		this_location_button = Button(map_frame, width = round(game_res_scale + 0.4 + math.floor(game_res_scale / 1.5)), height = round(game_res_scale), text = "B", command = lambda:fast_travel(-1))  
		this_button_container = map_button_container(this_location_button, current_location)
		boss_battle = point_of_interest(this_button_container, "ENCOUNTER", "This is an enemy", "enemy", current_tier, boss = True)
		game_map.append([boss_battle])

		
		# Handle setup required for drawing locations discovered to map frame

		vertical_pixels = int(game_res_axes[1])
		horizontal_pixels = int(game_res_axes[0])

		# Define screen-space variables for defining locations
		screen_middle = horizontal_pixels / 2;
		horizontal_shift_max = math.floor(8 * game_res_scale)
		y_buffer = 25 * game_res_scale; # Size (in pixels) between the bottom of the map frame and the first location, as well as between the top of the map frame and the last town (picture a vertical branch)
		y_base_location = 0;
		if(branch_id == 0):
			# Left path is being created this call
			x_base_location = 2/9 * horizontal_pixels; # Defining the starting x co-ordinates of the first location in the branch
		
		else:
			x_base_location = 7/9 * horizontal_pixels;# Defining the starting x co-ordinates of the first location in the branch

		x_location = x_base_location;
		x_location_previous = x_location;

		distance_between_locations = math.floor((vertical_pixels - 2 * y_buffer) / size)

		current_path, current_path_iterations = get_path_trend(screen_middle, x_location, y_base_location, branch_id) 

		# Define two first locations as starting locations so that they will appear on map at startup and the player can pick which path to take 
		game_map[0][0].starting_location = True;
		game_map[0][0].my_button_container.button.configure(text = "?")

		current_iteration = 1;
		# Loop through game_map and assign each location's button a x and y coordinate
		for location_set in game_map:
			for location in location_set:
				# Assign button a varying x location to simulate a path
				#Calculate distance to middle of screen 
				distance_to_middle = abs(screen_middle - x_base_location)

				# Get the absolute postion of y incrementally increasing without variance for paths
				normal_y = vertical_pixels - y_buffer - (y_base_location + distance_between_locations * current_iteration)

				if("straight" in current_path):
					# Get random amount to add
					x_change = random.randrange(-horizontal_shift_max, horizontal_shift_max) / 2;
					# Increase y by the most due to going in a straight line
					y_bonus = random.randrange(int(10 * game_res_scale), int(22 * game_res_scale))
					# Increase y only if it isnt a starting location
					y_change = (y_bonus * int(not location.starting_location))

					# Conglomerate x and y locations
					x_location += x_change;
					y_location = normal_y - y_change;

				elif("left" in current_path):
					if("gentle" in current_path):
						# Random angle in degrees between 10-25 due to a desiring a 'gentle' curve
						angle = random.randrange(10,25)
						# Convert angle to radians
						angle = math.radians(angle)

					elif("moderate" in current_path):
						# Random angle in degrees between 15-45 to achieve a 'moderate' curve
						angle = random.randrange(15, 45)
						# Convert angle to radians
						angle = math.radians(angle)
					else:
						# Random angle in degrees between 30-70 to achieve a 'large' curve
						angle = random.randrange(30, 70)
						# Convert angle to radians
						angle = math.radians(angle)

					# Increase y
					y_bonus = random.randrange(int(8 * game_res_scale), int(20 * game_res_scale))
					y_change = (y_bonus * int(not location.starting_location))
					x_change = y_change * math.tan(angle)
					# Flip x_change so that its going left instead of right
					x_change = - x_change;

					# Conglomerate x and y locations
					x_location += x_change;
					y_location = normal_y - y_change;


				elif("right" in current_path):
					if("gentle" in current_path):
						# Random angle in degrees between 10-25 due to a desiring a 'gentle' curve
						angle = random.randrange(10,25)
						# Convert angle to radians
						angle = math.radians(angle)

					elif("moderate" in current_path):
						# Random angle in degrees between 15-45 to achieve a 'moderate' curve
						angle = random.randrange(15, 45)
						# Convert angle to radians
						angle = math.radians(angle)
					else:
						# Random angle in degrees between 30-70 to achieve a 'large' curve
						angle = random.randrange(30, 70)
						# Convert angle to radians
						angle = math.radians(angle)

					# Increase y
					y_bonus = random.randrange(int(8 * game_res_scale), int(20 * game_res_scale))

					y_change = (y_bonus * int(not location.starting_location))

					x_change = y_change * math.tan(angle)
					


					# Conglomerate x and y locations
					x_location += x_change;
					y_location = normal_y - y_change;

				# Update location
				location.my_button_container.x = x_location;
				location.my_button_container.y = y_location;
				# Ensure x and y co-ordinates of locations stay within map screen
				if(location.my_button_container.x < 0):
					location.my_button_container.x = 0;
				elif(location.my_button_container.x > int(game_res_axes[0])):
					location.my_button_container.x = int(game_res_axes[0]);

				if(location.my_button_container.x == 0 ):
					location.my_button_container.x == 0;
				# Iterate over loop
				current_iteration += 1;
				current_path_iterations -= 1;

				if(current_path_iterations <= 0):
					current_path, current_path_iterations = get_path_trend(screen_middle, x_location, y_location, branch_id) 

				# Keep track of previous x
				x_location_previous = x_location;

		return game_map;  



	def confirm_attack(attack_target, attack_button_pressed = False): # Attack target is the location of the enemy to attack along with the accuracy
		action_window.attack_button.configure(state = DISABLED)
		action_window.target_head_button.configure(state = DISABLED, bg = "grey")
		action_window.target_torso_button.configure(state = DISABLED, bg = "grey")
		action_window.target_arm_left_button.configure(state = DISABLED, bg = "grey")
		action_window.target_arm_right_button.configure(state = DISABLED, bg = "grey")
		action_window.target_leg_left_button.configure(state = DISABLED, bg = "grey")
		action_window.target_leg_right_button.configure(state = DISABLED, bg = "grey")

		def player_reload():
			# Reload players weapon
			output_to_action_text("You reload your weapon...", True)
			audio_handler.play_sound_effect(0.6, "Reload")
			player_character.equipped_weapon.reload(action_window, NORMAL, DISABLED, END, player_character);
			action_window.attack_button.configure(state = DISABLED)

		
		if (attack_target != None):
			# Target selected and attack button is pressed
			if(player_character.equipped_weapon.current_ammo > 0 or player_character.equipped_weapon.weapon_type == "melee" or player_character.equipped_weapon.magazine_capacity == 0):
				attack_target = attack_target.lower().replace(" ","").split("-")

				player_character.deal_damage(target = attack_target[0], accuracy = int(attack_target[1]))

				if(Adversary.can_attack == True):
					Adversary.deal_damage()# Take damage
				else:	
					output_to_action_text(Adversary.name + " is concussed and couldn't attack", True)
			elif(player_character.equipped_weapon.current_ammo <= 0 and player_character.equipped_weapon.magazine_capacity != 0):
				# Take damage
				if(Adversary.can_attack == True):
					Adversary.deal_damage()
				else:
					output_to_action_text(Adversary.name + " is concussed and couldn't attack", True)

				player_reload()


		else:
			# Enemy has priority
			Adversary.deal_damage()
			if(attack_button_pressed):
				player_reload();

		
		action_window.attack_target = None;
		Adversary.can_attack = True;
		action_frame.after(random.randrange(500, 1200) + 400 * Adversary.equipped_weapon.shots_per_turn, lambda:action_window.enable_enemy_targeting())


	#Functions for handling frames###########################################################################
	def get_colour_tier(item):
		if(item.tier == 1):
			return "black"
		elif(item.tier == 2):
			return "green"
		else:
			return "purple"


	def insert_inventory_divider(item_type, width = None, separator = "-"):

		if(item_type == "weapon"):
			if(width != None):
				dashes = width - 7; # 7 for the length of "weapons"
				prefix_dashes = math.floor(dashes / 2) * separator
				suffix_dashes = math.ceil(dashes / 2) * separator
				return prefix_dashes + "Weapons" + suffix_dashes
			else:
				return "-" * 23 + "Weapons" + "-" * round(100 * game_res_scale)

		elif(item_type == "armour"):
			if(width != None):
				dashes = width - 6; # 6 for the length of "armour"
				prefix_dashes = math.floor(dashes / 2) * separator
				suffix_dashes = math.ceil(dashes / 2) * separator
				return prefix_dashes + "Armour" + suffix_dashes
			else:
				return "-" * 23 + "Armour" + "-" * round(100 * game_res_scale)
		else:
			if(width != None):
				dashes = width - 5; # 6 for the length of "items"
				prefix_dashes = math.floor(dashes / 2) * separator
				suffix_dashes = math.ceil(dashes / 2) * separator
				return prefix_dashes + "Items" + suffix_dashes
			else:
				return "-" * 23 + "Items" + "-" * round(100 * game_res_scale)


	def raise_frame(frame):
		frame.tkraise()

	def loadActionFrame(enemyOBJ):
		global active_frame;

		raise_frame(action_frame)
		active_frame = action_frame

		# Remove enemy targeting buttons
		action_window.target_head_button.place_forget()
		action_window.target_torso_button.place_forget()
		action_window.target_arm_left_button.place_forget()
		action_window.target_arm_right_button.place_forget()
		action_window.target_leg_left_button.place_forget()
		action_window.target_leg_right_button.place_forget()

		# Change the attack button's image to a gun if a ranged weapon is equipped and a sword if a melee weapon is equipped
		if(player_character.equipped_weapon.weapon_type == "ranged"):
			if(player_character.equipped_weapon.current_ammo == 0):
				action_window.attack_button.configure(text = "Reload")
				action_window.attack_button.configure(state = NORMAL)

			else:
				action_window.attack_button.configure(text = "Engage")
			action_window.attack_button.configure(image = action_window.Gun_Icon)
			action_window.ammo_selector.configure(state = NORMAL)

			ammo_types_available = player_character.get_ammo_types()
			ammo_names = []
			for ammo in ammo_types_available:
				ammo_names.append(str(ammo[0]) + " (" + str(ammo[1]) + ")")	
		else:
			action_window.attack_button.configure(text = "Engage")
			action_window.attack_button.configure(image = action_window.Sword_Icon)
			action_window.ammo_selector.configure(state = DISABLED)
			ammo_types_available = [["None", 0]]
			ammo_names = ["None (0)"]


		# Delete all choices in ammo selection
		action_window.ammo_selector.children['menu'].delete(0, END)
		
		# Add new ammo choices to the list
		for choice in ammo_types_available:
			this_ammo_name = str(choice[0]) + " (" + str(choice[1]) + ")"
			action_window.ammo_selector.children['menu'].add_command(label = this_ammo_name, command = lambda am=this_ammo_name: action_window.selected_ammo.set(am))
		# Set default option for ammo 

		action_window.selected_ammo.set(ammo_names[0]) 

		action_window.enemy_description_text.configure(state = NORMAL)
		action_window.enemy_description_text.delete(1.0, END)

		action_window.player_description_text.configure(state = NORMAL)
		action_window.player_description_text.delete(1.0, END)

		if(enemyOBJ.name != ""):
			textToInsert = "ENEMY: " + enemyOBJ.name + "\nHealth = " + str(enemyOBJ.health) + "\nArmour = " + str(enemyOBJ.armour) + "\nDamage = " + str(enemyOBJ.equipped_weapon.damage)
			action_window.enemy_description_text.insert(END, textToInsert)
			action_window.context_image.configure(image = enemyOBJ.sprite)
		else:
			action_window.attack_button.configure(state = DISABLED)
			try:
				if(player_character.current_location_index == -1):
					action_window.context_image.configure(image = start_image)
				else:
					action_window.context_image.configure(image = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].image)
			except:
				action_window.context_image.configure(image = random.choice(location_images))

		if(player_character.equipped_weapon.weapon_type == "ranged"):
			playerTextToInsert = player_character.name + ":\nHealth = " + str(player_character.health) + "\nArmour: " + str(player_character.armour) + "\nWEAPON: " + player_character.equipped_weapon.name + "\nMagazine: " + str(clamp(player_character.equipped_weapon.current_ammo, 0, player_character.equipped_weapon.magazine_capacity)) + "/" + str(player_character.equipped_weapon.magazine_capacity) #Player name from SPECIAL screen
			action_window.ammo_selector.configure(state=NORMAL)
		else:
			action_window.ammo_selector.configure(state=DISABLED)
			playerTextToInsert = player_character.name + ":\nHealth = " + str(player_character.health) + "\nArmour: " + str(player_character.armour) + "\nWEAPON: " + player_character.equipped_weapon.name #Player name from SPECIAL screen
		action_window.player_description_text.insert(END, playerTextToInsert)

		action_window.enemy_description_text.configure(state = DISABLED)
		action_window.player_description_text.configure(state = DISABLED)

		# Only draw clear textbox button to screen if the first character in the textbox is a character 
		if(ord(action_window.main_textbox.get(0.0)) != 10 and action_window.looting == False and action_window.in_combat == False and isinstance(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index], town) == False):
			action_window.clear_textbox_button.place(x = (480 * game_res_scale), y = 364 * game_res_scale)
		else:
			action_window.clear_textbox_button.place_forget()

		
		action_window.context_image.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale)

		# Only place enemy targeting buttons if an enemy object exists
		if(enemyOBJ.name != ""):
			action_window.target_head_button.configure(text = "Head - "  +           str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight  / 50) * 0.85 ) * (2 - Adversary.agility), 0, 100) ))  )
			action_window.target_torso_button.configure(text = "Torso - "  +         str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight / 50) * 1.1 ) * (2 - Adversary.agility), 0, 100) ))    )
			action_window.target_arm_left_button.configure(text = "Left arm - "  +   str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight / 50)) * (2 - Adversary.agility), 0, 100) ))           )
			action_window.target_arm_right_button.configure( text = "Right arm - "  + str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight / 50)) * (2 - Adversary.agility), 0, 100) ))           )
			action_window.target_leg_left_button.configure( text = "Left leg - "  +   str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight / 50)) * (2 - Adversary.agility), 0, 100) ))           )
			action_window.target_leg_right_button.configure( text = "Right leg - "  + str( int(clamp( round( (player_character.equipped_weapon.accuracy - random.randrange(-5,25)) * (1 + player_character.insight / 50)) * (2 - Adversary.agility), 0, 100) ))          )

			action_window.target_head_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[0][0] * game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[0][1]* game_res_scale)
			action_window.target_torso_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[1][0]* game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[1][1]* game_res_scale)
			action_window.target_arm_left_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[2][0]* game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[2][1]* game_res_scale)
			action_window.target_arm_right_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[3][0]* game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[3][1]* game_res_scale)
			action_window.target_leg_left_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[4][0]* game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[4][1]* game_res_scale)
			action_window.target_leg_right_button.place(x = (window_width / 2) - (262 * game_res_scale) + enemyOBJ.button_locations[5][0]* game_res_scale, y = 20 * game_res_scale + enemyOBJ.button_locations[5][1]* game_res_scale)


		action_window.main_textbox.configure(yscrollcommand=action_window.scrollbar.set)
		action_window.scrollbar.config(command=action_window.main_textbox.yview)

		schedule_thread.running = False; # Stop updating inventory window item descriptions to save resources

		# Delete memory of items to display the description of
		inventory_window.last_selected_item = None;
		inventory_window.last_selected_item_index = 0;
		game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].my_button_container.button.configure(bg = "white")

		
	def loadInventoryFrame():
		global item_description_schedule_created, active_frame;
		raise_frame(inventory_frame)
		active_frame = inventory_frame;

		schedule_thread.running = True; # Stop updating inventory window item descriptions to save CPU cycles

		if(item_description_schedule_created == False):
			# Initialise a schedule to check every 0.1 seconds what item the player has selected  
			my_schedule = schedule.every(0.15).seconds.do(update_item_description)
			item_description_schedule_created = True

		player_character.update_carry_weight()
		# Update display of how much player is carrying
		inventory_window.carry_weight_indicator.configure(text = str(player_character.current_carry_weight) + "/" + str(player_character.max_carry_weight))
		# Update baguette display
		inventory_window.player_baguettes_indicator.configure(text = str(player_character.baguettes))

		inventory_window.inventory_contents.configure(state = NORMAL) # Allowing writes to text 
		inventory_window.inventory_contents.delete(0, END) # Delete all contents
		
		# Insert inventory divider that starts "WEAPONS" 
		position_in_items = 0;
		inventory_window.inventory_contents.insert(END, insert_inventory_divider("weapon"))
		position_in_items += 1;
		#Add all weapons in inventory to inventory contents
		
		for i in player_character.weapon_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(i)

			#Label equipped weapons with a ">" prefix
			if(i == player_character.equipped_weapon):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""

			# Display item to inventory contents text box 
			if(player_character.weapon_inventory[i] > 1):
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " (" + str(player_character.weapon_inventory[i]) + ") " + get_sign_as_string( ((i.damage * i.shots_per_turn * (i.accuracy / 100)) * (1 + i.critical_chance / 50) ) - ((player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100)) * (1 + player_character.equipped_weapon.critical_chance / 50)) ) * int(abs(math.floor(((i.damage * i.shots_per_turn * (i.accuracy / 100) * (1 + i.critical_chance / 50)) - player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100) * (1 + player_character.equipped_weapon.critical_chance / 50)) / 5) )))			
			else:
				# Not only display weapon, but also calculate how much better it is compared to the currently equipped weapon and display a respective quantity of +'s or -'s
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " " + get_sign_as_string( ((i.damage * i.shots_per_turn * (i.accuracy / 100)) * (1 + i.critical_chance / 50) ) - ((player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100)) * (1 + player_character.equipped_weapon.critical_chance / 50)) ) * int(abs(math.floor(((i.damage * i.shots_per_turn * (i.accuracy / 100) * (1 + i.critical_chance / 50)) - player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100) * (1 + player_character.equipped_weapon.critical_chance / 50)) / 5) ))) 
			# Colour text in relation to weapon tier
			inventory_window.inventory_contents.itemconfig(position_in_items , fg=relevant_colour)
			position_in_items += 1;

		# Insert inventory divider that starts "ARMOUR" 
		inventory_window.inventory_contents.insert(END, insert_inventory_divider("armour"))
		position_in_items += 1;
		# Add all armour in inventory to inventory contents
		
		for i in player_character.armour_inventory:
			# Get respective colour of item based off of tier
			relevant_colour = get_colour_tier(i)
			#Label equipped armour with a ">" prefix
			if(i in player_character.equipped_armour):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""

			# Transform type of armour into index
			if(i.description == "helmet"):
				armour_description_id = 0;
			elif(i.description == "chest_piece"):
				armour_description_id = 1;
			elif(i.description == "left_arm"):
				armour_description_id = 2;
			elif(i.description == "right_arm"):
				armour_description_id = 3;
			elif(i.description == "left_leg"):
				armour_description_id = 4;
			else:
				armour_description_id = 5;

			# Display item to inventory contents text box 
			if(player_character.armour_inventory[i] > 1):
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " (" + str(player_character.armour_inventory[i]) + ") " + get_sign_as_string(i.protection - player_character.equipped_armour[armour_description_id].protection) * int(abs(math.floor(i.protection - player_character.equipped_armour[armour_description_id].protection) / 2)))
			else:
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " " + get_sign_as_string(i.protection - player_character.equipped_armour[armour_description_id].protection) * int(abs(math.floor(i.protection - player_character.equipped_armour[armour_description_id].protection) / 2)) )
			# Colour text in relation to armour tier
			inventory_window.inventory_contents.itemconfig(position_in_items , fg=relevant_colour)
			position_in_items += 1;

		# Insert inventory divider that starts "ITEMS" 
		inventory_window.inventory_contents.insert(END, insert_inventory_divider("item"))
		#Add all items in inventory to inventory contents
		for i in player_character.item_inventory:
			inventory_window.inventory_contents.insert(END, i.name + " (" + str(player_character.item_inventory[i]) + ")")

		inventory_window.inventory_contents.configure(yscrollcommand=inventory_window.scrollbar.set)
		inventory_window.scrollbar.config(command=inventory_window.inventory_contents.yview)

		game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].my_button_container.button.configure(bg = "white")
		 
		#inventory_window.inventory_contents.configure(state = DISABLED) #Disallow writes to text 


	def update_item_description(): # This function runs every 0.15 seconds on a separate thread
		# Remove previously displayed text windows as position could change if new item was selected in the last 0.2 seconds
		inventory_window.item_description_graphic.place_forget() 
		inventory_window.item_description.place_forget()
		# Remove previous text held within item description
		inventory_window.item_description.delete(1.0, END)

		selected_item_index = inventory_window.inventory_contents.curselection();
		try:
			# Attempt to get the item at the location 
			selected_item_index = selected_item_index[0]
			selected_item_array = player_character.get_item_in_inventory(selected_item_index) # Get array of item and item type
		except Exception as e:
			# However, if no item is selected, gather previous item instead
			selected_item_array = inventory_window.last_selected_item;
			selected_item_index = inventory_window.last_selected_item_index;

		# If the item selected isn't an inventory divider, draw text boxes at location 
		if(selected_item_array != None): 
			# Extract data from array returned from player
			selected_item_type = selected_item_array[1]
			selected_item = selected_item_array[0]

			absolute_item_index = selected_item_index + 1;
			scrollbar_position = inventory_window.scrollbar.get()[0] # Gets how close to the bottom the scroll bar is (as a value from 0-1)
		
			if(scrollbar_position == 0.0 and absolute_item_index <= 18 and game_resolution == "1024x576"):
				inventory_window.item_description_graphic.place(x = 590 * game_res_scale - ((game_res_scale - 1) * 12), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
				inventory_window.item_description.place(x = 658 * game_res_scale - ((game_res_scale - 1) * 43), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
			elif(scrollbar_position == 0.0 and absolute_item_index <= 22 and game_resolution == "1280x720"):
				inventory_window.item_description_graphic.place(x = 590 * game_res_scale - ((game_res_scale - 1) * 12), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
				inventory_window.item_description.place(x = 656 * game_res_scale - ((game_res_scale - 1) * 43), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
			elif(scrollbar_position == 0.0 and absolute_item_index <= 34 and game_resolution == "1920x1080"):
				inventory_window.item_description_graphic.place(x = 590 * game_res_scale - ((game_res_scale - 1) * 12), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
				inventory_window.item_description.place(x = 658 * game_res_scale - ((game_res_scale - 1) * 43), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
			elif(scrollbar_position == 0.0 and absolute_item_index <= 45 and game_resolution == "2560x1440"):
				inventory_window.item_description_graphic.place(x = 590 * game_res_scale - ((game_res_scale - 1) * 12), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
				inventory_window.item_description.place(x = 658 * game_res_scale - ((game_res_scale - 1) * 43), y = (52 * game_res_scale + (selected_item_index * 22.1)) )
			else:
				#inventory_window.item_description_graphic.place(x = 590 * game_res_scale - ((game_res_scale - 1) * 12), y =yPos)# (52 * game_res_scale + (selected_item_index * 22.1)) )
				inventory_window.item_description.place(x = 658 * game_res_scale - ((game_res_scale - 1) * 43), y = 100 * game_res_scale)#(52 * game_res_scale + (selected_item_index * 22.1)) )


			
			#Fill description box with relevant information
			if(selected_item_type == "weapon"):
				# Modify action button to represent how the player can interact with the selected item
				if(selected_item == player_character.equipped_weapon):
					inventory_window.equip_item_button.configure(text = "Unequip")
					inventory_window.equip_item_button.configure(state = NORMAL)
				else:
					inventory_window.equip_item_button.configure(text = "Equip")
					inventory_window.equip_item_button.configure(state = NORMAL)
				# Fill with relevant weapon information - If a new item is selected, progressively scroll text into text box, however upon refresh, if the same item is selected as last refresh, don't scroll text
				if(selected_item_array != inventory_window.last_selected_item):
					output_to_item_description(selected_item.name + "\n" + selected_item.weapon_type.capitalize() + "\nDamage: " + str(selected_item.damage) + "\nCrit chance: " + str(selected_item.critical_chance) + "\nAccuracy: " + str(selected_item.accuracy) + "\nMagazine capacity: " + str(selected_item.magazine_capacity) + "\nShots per turn: " + str(selected_item.shots_per_turn) + "\nCondition: " + str(selected_item.condition) + "\nWeight: " + str(selected_item.weight)  )
				else:
					inventory_window.item_description.insert(END, selected_item.name + "\n" + selected_item.weapon_type.capitalize() + "\nDamage: " + str(selected_item.damage) + "\nCrit chance: " + str(selected_item.critical_chance) + "\nAccuracy: " + str(selected_item.accuracy) + "\nMagazine capacity: " + str(selected_item.magazine_capacity) + "\nShots per turn: " + str(selected_item.shots_per_turn) + "\nCondition: " + str(selected_item.condition) + "\nWeight: " + str(selected_item.weight)  )
			
			elif(selected_item_type == "armour"):
				# Modify action button to represent how the player can interact with the selected item
				if(selected_item in player_character.equipped_armour):
					inventory_window.equip_item_button.configure(text = "Unequip")
					inventory_window.equip_item_button.configure(state = NORMAL)
				else:
					inventory_window.equip_item_button.configure(text = "Equip")
					inventory_window.equip_item_button.configure(state = NORMAL)
				# Fill with relevant armour information - If a new item is selected, progressively scroll text into text box, however upon refresh, if the same item is selected as last refresh, don't scroll text
				if(selected_item_array != inventory_window.last_selected_item):
					output_to_item_description(selected_item.name + "\nPiece: " + selected_item.description.replace("_", " ").capitalize() + "\nProtection: " + str(selected_item.protection) + "\nWeight: " + str(selected_item.weight) )
				else:
					inventory_window.item_description.insert(END, selected_item.name + "\nPiece: " + selected_item.description.replace("_", " ").capitalize() + "\nProtection: " + str(selected_item.protection) + "\nWeight: " + str(selected_item.weight) )
			
			elif(selected_item_type == "item"):
				# Modify action button to represent how the player can interact with the selected item
				if(selected_item.name == "AP rounds" or selected_item.name == "Concussion rounds"):
					inventory_window.equip_item_button.configure(text = "")
					inventory_window.equip_item_button.configure(state = DISABLED)
				else:
					inventory_window.equip_item_button.configure(text = "Consume")
					inventory_window.equip_item_button.configure(state = NORMAL)
				
				# Fill with relevant item information - If a new item is selected, progressively scroll text into text box, however upon refresh, if the same item is selected as last refresh, don't scroll text
				if(selected_item_array != inventory_window.last_selected_item):
					output_to_item_description(selected_item.name + "\n" + selected_item.variation + "\nAffects: " + selected_item.affector.replace("_", " ").capitalize() + " by " + str(selected_item.amount) + "\nWeight: " + str(selected_item.weight) )
				else:
					inventory_window.item_description.insert(END, selected_item.name + "\n" + selected_item.variation + "\nAffects: " + selected_item.affector.replace("_", " ").capitalize() + " by " + str(selected_item.amount) + "\nWeight: " + str(selected_item.weight) )


			# Update store of last selected item to currently selected item
			inventory_window.last_selected_item = selected_item_array;
			inventory_window.last_selected_item_index = selected_item_index;


	def loadMapFrame():
		global active_frame, map_button_pressed
		# Stop the guide from running because player has clicked on the map button
		map_button_pressed = True;

		raise_frame(map_frame)
		active_frame = map_frame;
		schedule_thread.running = False; # Stop updating inventory window item descriptions to save resources
		# Delete memory of items to display the description of
		inventory_window.last_selected_item = None;
		inventory_window.last_selected_item_index = 0;


		if(map_window.zoom == "out"):
			# Loop through game_map and display all location buttons that have been flagged as cleared
			for game_branch in game_map:
				for location_set in game_branch:
					for location in location_set:
						# Only place the button if the corresponding location has been discovered
						if(location.cleared == True or location.starting_location == True or location.boss == True):
							# Place the child button object assigned to each location, x,y co-ordinates don't need to be scaled to game resolution
							location.my_button_container.button.place(x = location.my_button_container.x, y = location.my_button_container.y)

						# Set colour of current location button to gold 
						if(location == game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index]):
							location.my_button_container.button.configure(bg = "gold")

		else:
			map_window.clear_all_button_locations()
			for game_branch in game_map:
				zoomed_y_pos = 30 # Initiate buffer 
				zoomed_y_distance = int(game_res_axes[1]) - (2 * zoomed_y_pos)
				for location in game_branch[player_character.current_town_index]:
					if(location.cleared == True or location.starting_location == True or location.boss == True):
						zoomed_y_step = zoomed_y_distance / len(game_branch[player_character.current_town_index])
						location.my_button_container.button.place(x = location.my_button_container.x, y = int(game_res_axes[1]) - zoomed_y_pos)
					else:
						zoomed_y_step = 0;
					zoomed_y_pos += zoomed_y_step;

					# Set colour of current location button to gold 
					if(location == game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index]):
						location.my_button_container.button.configure(bg = "gold")

		if(player_character.current_location_index == -1):
			# Run the second step of the guide
			run_guide(1)




	def load_stats_frame():
		global active_frame
		raise_frame(stats_frame)
		active_frame = stats_frame;
		schedule_thread.running = False; # Stop updating inventory window item descriptions to save resources
		# Delete memory of items to display the description of
		inventory_window.last_selected_item = None;
		inventory_window.last_selected_item_index = 0;

		stats_window.player_stats_display.configure(state = NORMAL)
		stats_window.player_stats_display.delete(0.0, END)
		player_stats_text = player_character.name + "  LVL " + str(player_character.level) + "\n\nFortune: " + str(player_character.fortune) + "\nInsight: " + str(player_character.insight) + "\nCharisma: " + str(player_character.charisma) + "\nAgility: " + str(player_character.agility) + "\nStrength: " + str(player_character.strength)
		stats_window.player_stats_display.insert(END, player_stats_text)

		stats_window.player_exp_label.place(x= int(game_res_axes[0]) / 2 - 10, y = 465 * game_res_scale)
		stats_window.player_exp_bar.place(x = (int(game_res_axes[0]) / 2) - (340 * game_res_scale/2), y = 490 * game_res_scale)

		stats_window.player_stats_display.configure(state = DISABLED)
		game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].my_button_container.button.configure(bg = "white")

		if(player_character.unspent_skillpoints > 0): 
			# Ensure correct plural is used for skillpoint allocation title
			if(player_character.unspent_skillpoints == 1):
				stats_window.skillpoints_label.configure(text = "1 Unspent Skillpoint")
			else:
				stats_window.skillpoints_label.configure(text = str(player_character.unspent_skillpoints) + " Unspent Skillpoints")
			# Draw widgets to enable allocating skill points
			stats_window.skillpoints_label.place(x = 103 * game_res_scale, y = 117 * game_res_scale)
			stats_window.fortune_skill_label.place(x = 140 * game_res_scale, y = 155 * game_res_scale)
			stats_window.fortune_skill_button.place(x = 302 * game_res_scale, y = 155 * game_res_scale)
			stats_window.insight_skill_label.place(x = 140 * game_res_scale, y = 225.5 * game_res_scale)
			stats_window.insight_skill_button.place(x = 302 * game_res_scale, y = 225.5 * game_res_scale)
			stats_window.charisma_skill_label.place(x = 140 * game_res_scale, y = 296 * game_res_scale)
			stats_window.charisma_skill_button.place(x = 302 * game_res_scale, y = 296 * game_res_scale)
			stats_window.agility_skill_label.place(x = 140 * game_res_scale, y = 366.5 * game_res_scale)
			stats_window.agility_skill_button.place(x = 302 * game_res_scale, y = 366.5 * game_res_scale)
			stats_window.strength_skill_label.place(x = 140 * game_res_scale, y = 437 * game_res_scale)
			stats_window.strength_skill_button.place(x = 302 * game_res_scale, y = 437 * game_res_scale)


		else: # check if one is drawn, if so, undraw all - Optimisation
			# No skill point widgets should be drawn
			if(stats_window.skillpoints_label.place_info() != {}): # Check to see if a skillpoint widget has been drawn
				# Undraw all drawn widgets
				stats_window.skillpoints_label.place_forget()
				stats_window.fortune_skill_label.place_forget()
				stats_window.fortune_skill_button.place_forget()
				stats_window.insight_skill_label.place_forget()
				stats_window.insight_skill_button.place_forget()
				stats_window.charisma_skill_label.place_forget()
				stats_window.charisma_skill_button.place_forget()
				stats_window.agility_skill_label.place_forget()
				stats_window.agility_skill_button.place_forget()
				stats_window.strength_skill_label.place_forget()
				stats_window.strength_skill_button.place_forget()
				

	def enter_merchant():
		action_window.exit_from_merchant_button.configure(state = NORMAL)
		action_window.buy_button.configure(state = NORMAL)
		action_window.sell_button.configure(state = NORMAL)
		audio_handler.play_sound_effect(1, "Door_Open")
		action_frame.after(2000, lambda:audio_handler.play_dialogue(1, "Merchant_Welcome_" + player_character.gender.capitalize()))
		action_window.remove_town_buttons()
		action_window.erase_standard_action_layout()
		action_window.draw_merchant_screen();
		action_frame.after(15000, lambda:check_for_loiter(12000))

	def check_for_loiter(polling_interval):
		# Check if merchant window still open, if it is, call poll again in 12 seconds
		if(action_window.buy_button.place_info() != {}):
			# Still open
			if(action_window.loiter_flag):
				# Loitering detected
				audio_handler.play_dialogue(1, "Merchant_Loiter_" + player_character.gender.capitalize())
				polling_interval += 2500;

			action_window.loiter_flag = True
			action_frame.after(polling_interval, lambda:check_for_loiter(polling_interval)) 
			return;
		else:
			# Merchant window has been closed
			return;

	def buy_item():
		audio_handler.play_sound_effect(1, "Exchange")
		action_window.loiter_flag = False

		# Find which item the player clicked on to buy
		item_index = action_window.merchant_inventory.curselection()[0]
		#Ensure item index isn't on an inventory divider
		weapons_length = len(action_window.current_merchant.weapon_inventory)
		armour_length = len(action_window.current_merchant.armour_inventory)
		items_length = len(action_window.current_merchant.item_inventory)

		# Verify that the player isn't trying to sell an inventory divider text
		if(item_index != 0 and item_index != weapons_length + 1 and item_index != weapons_length + armour_length + 2 ):
			# Translate item index into item from merchant 
			if(item_index <= weapons_length):
				weapons = list(action_window.current_merchant.weapon_inventory.keys())
				purchase_item = weapons[item_index - 1]
				purchase_item_type = "w" # Weapon
			elif(item_index <=weapons_length + armour_length + 1):
				armour = list(action_window.current_merchant.armour_inventory.keys())
				purchase_item = armour[item_index - weapons_length - 2]
				purchase_item_type = "a" # Armour
			else:
				items = list(action_window.current_merchant.item_inventory.keys())
				purchase_item = items[item_index - weapons_length - armour_length - 3]
				purchase_item_type = "i" # Item
			
			# Verify that the player has enough money and room for selected item
			if(purchase_item.value <= player_character.baguettes and player_character.current_carry_weight + purchase_item.weight <= player_character.max_carry_weight):

				# Play sound effect
				action_frame.after(750, lambda:audio_handler.play_dialogue(1, "Merchant_Buy"))

				# Remove the money from the player
				player_character.baguettes -= purchase_item.value;
				action_window.current_merchant.baguettes += purchase_item.value;

				# Give player item and remove item from merchant 
				if(purchase_item_type == "w"):		
					# Delete item from merchant's inventory
					del action_window.current_merchant.weapon_inventory[purchase_item]
					# Devalue the item
					purchase_item.value = round(purchase_item.value / 2)
					# Add item to players inventory
					player_character.add_item(purchase_item, 1)
				elif(purchase_item_type == "a"):
					# Delete item from merchant's inventory
					del action_window.current_merchant.armour_inventory[purchase_item]
					# Devalue the item
					purchase_item.value = round(purchase_item.value / 2)
					# Add item to players inventory
					player_character.add_item(purchase_item, 1)

				else:
					
					# Check how many copies of this item are in the merchants inventory
					copies = action_window.current_merchant.item_inventory[purchase_item]
					if(copies == 1):
						# Delete item from merchant's inventory
						del action_window.current_merchant.item_inventory[purchase_item]
					else:
						# More than one copy
						del action_window.current_merchant.item_inventory[purchase_item]
						action_window.current_merchant.item_inventory.update({purchase_item:copies-1})
					# Add item to players inventory
					player_character.add_item(purchase_item, 1)

				player_character.update_carry_weight();
				action_window.repopulate_player_inventory();
				

			else:
				#Insufficient funds or inventory space
				return;

		else:
			return;
		
	def sell_item():
		audio_handler.play_sound_effect(1, "Click")
		action_window.loiter_flag = False

		# Find which item the player clicked on to sell
		item_index = action_window.player_inventory.curselection()[0]
		#Ensure item index isn't on an inventory divider
		weapons_length = len(player_character.weapon_inventory)
		armour_length = len(player_character.armour_inventory)
		items_length = len(player_character.item_inventory)

		if(item_index != 0 and item_index != weapons_length + 1 and item_index != weapons_length + armour_length + 2 ):
			# Translate item index into item from merchant 
			if(item_index <= weapons_length):
				weapons = list(player_character.weapon_inventory.keys())
				sell_item = weapons[item_index - 1]
				purchase_item_type = "w" # Weapon
			elif(item_index <=weapons_length + armour_length + 1):
				armour = list(player_character.armour_inventory.keys())
				sell_item = armour[item_index - weapons_length - 2]
				purchase_item_type = "a" # Armour
			else:
				items = list(player_character.item_inventory.keys())
				sell_item = items[item_index - weapons_length - armour_length - 3]
				purchase_item_type = "i" # Item

			# Verify that merchant has enough money to buy item from player
			if(sell_item.value <= action_window.current_merchant.baguettes):
				action_frame.after(500, lambda:audio_handler.play_sound_effect(1, "Exchange"))
				# Merchant is wealthy enough
				action_window.current_merchant.baguettes -= sell_item.value;
				player_character.baguettes += sell_item.value
				# Only play dialogue roughly every second time an item is sold to avoid spamming the user
				if(random.choice([True, False])):
					action_frame.after(1100, lambda:audio_handler.play_dialogue(1, "Merchant_Sell"))


				# Give merchant item and remove item from player 
				if(purchase_item_type == "w"):		

					if(sell_item == player_character.equipped_weapon):
						# Remove armour from players equipped armour and replace with an alternative
						for weapon in player_character.weapon_inventory:
							if(weapon != sell_item):
								# Have a suitable replacement
								player_character.equipped_weapon = weapon;
								# Delete item from player's inventory
								del player_character.weapon_inventory[sell_item]
								break;

						# Item didn't get replaced
						if(sell_item == player_character.equipped_weapon):
							# Replace with default weapon
							player_character.equipped_weapon = default_weapon;
							# Delete original weapon from inventory
							del player_character.weapon_inventory[sell_item];
					else:
						# Delete item from player's inventory
						del player_character.weapon_inventory[sell_item]
					# Add item to merchant's inventory
					sell_item.value *= 2;
					action_window.current_merchant.weapon_inventory.update({sell_item:1})
				elif(purchase_item_type == "a"):
					if(sell_item in player_character.equipped_armour):
						# Remove armour from players equipped armour and replace with an alternative
						for armour_item in player_character.armour_inventory:
							if(armour_item != sell_item and sell_item.description == armour_item.description):
								# Have a suitable replacement
								player_character.equipped_armour[player_character.equipped_armour.index(sell_item)] = armour_item;
								# Delete item from player's inventory
								del player_character.armour_inventory[sell_item]
								break;

						# Item didn't get replaced
						if(sell_item in player_character.armour_inventory):
							player_character.equipped_armour[player_character.equipped_armour.index(sell_item)] = default_armour;
							del player_character.armour_inventory[sell_item];
					else:
						# Not an equipped item
						del player_character.armour_inventory[sell_item];

					player_character.update_armour_total();
					
					# Add item to merchant's inventory
					sell_item.value *= 2;
					action_window.current_merchant.armour_inventory.update({sell_item:1})
				else:
					# Check how many copies of this item are in the merchants inventory
					copies = player_character.item_inventory[sell_item]
					if(copies == 1):
						# Delete item from merchant's inventory
						del player_character.item_inventory[sell_item]
					else:
						# More than one copy
						del player_character.item_inventory[sell_item]
						player_character.item_inventory.update({sell_item:copies-1})

					# Add item to merchant's inventory
					try:
						# Add an extra one if merchant already has one
						merchant_copies = action_window.current_merchant.item_inventory[sell_item]
						del action_window.current_merchant.item_inventory[sell_item]
						action_window.current_merchant.item_inventory.update({sell_item:merchant_copies + 1})
					except:
						action_window.current_merchant.item_inventory.update({sell_item:1})

				player_character.update_carry_weight();
				action_window.repopulate_player_inventory();


			else:
				# Merchant doesn't have enough wealth
				audio_handler.play_dialogue(1, "Merchant_Broke")

			

	def enter_gamble():
		# Set wager display for convenience of user
		reset_auto_wager();
		audio_handler.play_sound_effect(1, "Door_Open")
		action_window.remove_town_buttons()
		action_window.erase_standard_action_layout()
		action_window.draw_gamble_screen();

	def wager_change(polarity):
		wager_step = 10;
		if(polarity): # Positive change
			if(action_window.gamble_wager + wager_step <= player_character.baguettes): # Check to ensure the player isn't trying to bet more than they have 
				action_window.gamble_wager += wager_step;
		else: # Negative Change
			if(action_window.gamble_wager - wager_step >= 1): # Check to ensure a positive wager is made
				action_window.gamble_wager -= wager_step;
		# Update GUI
		action_window.gamble_wager_display.configure(text = str(action_window.gamble_wager))

	def confirm_gamble(choice):
		if(action_window.gamble_wager > 0):
			player_character.coin_choice = choice;
			audio_handler.play_dialogue(1, "Coin_Narration")
			action_frame.after(random.randrange(2000, 3000), lambda:audio_handler.play_sound_effect(1,"Coin_Toss"))
			action_frame.after(7000, lambda:two_up_result()) # Tune this time to the length of audio queue
			# Remove choice and wager buttons
			action_window.gamble_equal_button.place_forget();
			action_window.gamble_heads_button.place_forget();
			action_window.gamble_tails_button.place_forget();
			action_window.gamble_wager_display.place_forget();
			action_window.gamble_wager_increase_button.place_forget()
			action_window.gamble_wager_decrease_button.place_forget();
			action_window.gamble_wager_title.place_forget()
			action_window.exit_from_gamble_button.configure(state = DISABLED)

	def two_up_result():

		# Determine result while factoring in player's fortune stat as a small bias
		chance_player_was_right = 0.33 + clamp(player_character.fortune, 0, 50) / 100;

		if(random.random() <= chance_player_was_right):
			result = random.choice(player_character.coin_choice)
		else:
			result = random.choice(remove_values_from_list(["h", "t", "e"], player_character.coin_choice))


		if(result ==  "h"):
			# Display Two-Up Heads image
			pass;
		elif(result == "t"):
			# Display Two-Up Tails image
			pass;
		else:
			# Display Two-Up equals image
			pass;

		action_frame.after(300,reset_gamble)
		if(result == player_character.coin_choice):
			# Player gambled correctly
			action_frame.after(255, lambda:audio_handler.play_dialogue(1, "Coin_Victory"))
			player_character.baguettes += action_window.gamble_wager;
			showinfo("Victory!", "You won " + str(action_window.gamble_wager) + " baguettes")
			

		else:
			# Player gambled incorrectly
			action_frame.after(255, lambda:audio_handler.play_dialogue(1, "Coin_Defeat"))
			player_character.baguettes -= action_window.gamble_wager;
			showinfo("Defeat!", "You lost " + str(action_window.gamble_wager) + " baguettes")
				
	def reset_auto_wager(): # Set wager display for convenience of user
		if(player_character.baguettes > 20):
			action_window.gamble_wager = math.floor(player_character.baguettes / (10 * (len(str(player_character.baguettes)) - 1))) * 10; # Halve and round to nearest ten
		else:
			action_window.gamble_wager = 0;

		action_window.gamble_wager_display.configure(text = str(action_window.gamble_wager))
 
	def reset_gamble():
		# Set wager display for convenience of user
		reset_auto_wager();
		action_window.exit_from_gamble_button.configure(state = NORMAL)
		# Check if the player hasn't exited as to avoid drawing gamble screen over default action window
		if(action_window.enemy_description_text.place_info() == {}):
			action_window.gamble_result_image.place_forget();
			action_window.draw_gamble_screen();
			action_window.gamble_heads_button.place(x = 590 * game_res_scale, y = 365 * game_res_scale)
			action_window.gamble_tails_button.place(x = 270 * game_res_scale, y = 365 * game_res_scale)
			action_window.gamble_equal_button.place(x = 430 * game_res_scale, y = 365 * game_res_scale)
			action_window.gamble_wager_title.place(x = 440 * game_res_scale, y = 440 * game_res_scale)
			action_window.gamble_wager_decrease_button.place(x = 455 * game_res_scale, y = 470 * game_res_scale)
			action_window.gamble_wager_display.place(x = 480 * game_res_scale, y = 472 * game_res_scale)
			action_window.gamble_wager_increase_button.place(x = 525 * game_res_scale, y = 470 * game_res_scale)
			action_window.gamble_result_image.configure(image = action_window.dealer_image)
		else:
			return;

	def exit_sub_town(sub_town): # Called from Exit button in merchant or gamble

		if(sub_town == "gamble"):
			# Exiting from gabling
			action_window.title.configure(text = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].name)
			audio_handler.play_sound_effect(1, "Door_Close")
			action_window.erase_gamble_screen();
			action_window.draw_standard_action_layout();
			action_window.draw_town_buttons();
		else:
			# Exiting from Merchant
			action_window.exit_from_merchant_button.configure(state = DISABLED)
			action_window.title.configure(text = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].name)
			audio_handler.play_dialogue(1, "Merchant_Goodbye_" + player_character.gender.capitalize())
			action_window.buy_button.configure(state = DISABLED)
			action_window.sell_button.configure(state = DISABLED)
			action_frame.after(2000, lambda:audio_handler.play_sound_effect(1, "Door_Close"))
			action_frame.after(2100, lambda:action_window.erase_merchant_screen())
			action_frame.after(2200, lambda:action_window.exit_from_merchant_button.configure(state = DISABLED))
			action_frame.after(2400, lambda:action_window.draw_standard_action_layout())
			action_frame.after(2700, lambda:action_window.draw_town_buttons())
			action_frame.after(2750, lambda:loadActionFrame(Adversary))



	def fast_travel(new_location): # Receives 3D array of new location 
		# Remove all possible buttons that could persist after fast travelling
		if(action_window.loot_window.place_info != {}):
			action_window.done_looting();
		action_window.disable_navigation();
		if(action_window.goto_gamble_button.place_info != {}):
			action_window.remove_town_buttons();
		if(action_window.left_at_fork_button.place_info != {}):
			action_window.left_at_fork_button.place_forget();
			action_window.right_at_fork_button.place_forget();

		if(new_location[1] == 0):
			# Once the player has picked a location to start at, reveal both of the location's encounters and hide the not-selected one
			player_character.picked_starting_location = True;
			game_map[0][0][0].my_button_container.button.configure(text = "E")
			game_map[1][0][0].my_button_container.button.configure(text = "E")
			if(new_location[0] == 0):
				game_map[1][0][0].starting_location = False;
				game_map[1][0][0].my_button_container.button.place_forget()
			else:
				game_map[0][0][0].starting_location = False;
				game_map[0][0][0].my_button_container.button.place_forget()


		# Map the player's location data to the new_location data specified
		player_character.current_map_index = new_location[0]
		player_character.current_town_index = new_location[1]
		player_character.current_location_index = new_location[2]

		# Add a delay of 1 second before tele-porting player to new location
		inventory_frame.after(1000, loadActionFrame(Adversary))

		# Call the new location's event to occur
		interpret_location(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index])


	def change_location(direction, path_change = None):

		action_window.remove_town_buttons()
		if(direction > 0):
			# Positive change, going forward

			# Check if player has not reached a new town, if they haven't, progress them 1 further towards the next town
			# If they are at the end however, move them to the next town
			if(player_character.current_location_index < len(game_map[player_character.current_map_index][player_character.current_town_index]) - 1):
				# Advance player
				player_character.current_location_index += 1;
				# Remove buttons to move
				action_window.forward_button.place_forget()
				action_window.backward_button.place_forget()
			else:
				# Check that player is not at the end of the game
				if(player_character.current_town_index < len(game_map[player_character.current_map_index])):
					# Advance player
					player_character.current_town_index += 1;
					player_character.current_location_index = 0;
					# Remove buttons to move
					action_window.forward_button.place_forget()
					action_window.backward_button.place_forget()
				else:
					output_to_action_text("You win?.", True)

		elif(direction < 0):
			# Negative change, going backwards
			# Check if player has not reached a previous town, if they havent, progress them 1 backwards towards the previous town
			# If they are at the start however, move them to the next town
			if(player_character.current_location_index > 0):
				player_character.current_location_index -= 1;

				action_window.forward_button.place_forget()
				action_window.backward_button.place_forget()
			else:
				# Check that player is not at the start of the game
				if(player_character.current_town_index > 0):
					player_character.current_town_index -= 1;
					player_character.current_location_index = len(game_map[player_character.current_map_index][player_character.current_town_index]) - 1;

					action_window.forward_button.place_forget()
					action_window.backward_button.place_forget()
				else:
					output_to_action_text("You cannot go back any further.", True)

		if(path_change != None):
			# Remove left/right options 
			action_window.left_at_fork_button.place_forget();
			action_window.right_at_fork_button.place_forget();

			# Switch paths
			switch_paths()

		print(str(player_character.current_map_index) + ":" + str(player_character.current_town_index) + ":" + str(player_character.current_location_index))
		interpret_location(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index])


	def switch_paths():
		# Switch paths
		# Investigate placing player at start of next town set instead of start of current 
		player_character.current_map_index = (player_character.current_map_index + 1) % 2;
		try: 
			# Check if current location on other path exists
			test_data = game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index]
			print(test_data.name)
			# Path does exist, nothing further to be done
			#return;
		except Exception as exc:
			# Current location doesn't exist, thus place player at start of current town index

			player_character.current_location_index = 0;
			player_character.current_town_index += 1;
		

	def interpret_location(location):
		encounter_active = True;
		# Function that sets up the action frame for the current point of interest. 
	
		evoke_location(location)

		# Check to see if POI object is from the town or POI class
		if(isinstance(location, town)):
			player_character.at_town = True;

			if(location.cleared == False):
				player_character.towns_discovered += 1;
			# Change values of items based on charisma only if the location has never been visited by the player, or if the players charisma has changed since last visiting
			if(not location.cleared or location.charisma_memory != player_character.charisma):
				location.my_merchant.initialise();
				location.cleared = True;
				location.charisma_memory = player_character.charisma;
			# Display buttons
			action_window.draw_town_buttons();

		elif(isinstance(location, point_of_interest)):
			player_character.at_town = False;
			if(location.cleared == False):
				# Player has not visited this area 
				# Call the POI to run its code for this location
				location.generate_encounter(game_res_scale, player_character, boss = location.boss)
				location.cleared = True;
				if(location.encounter_type == "enemy"):
					action_window.current_enemy = location.encounter;
					pre_combat_sequence()
					
				elif(location.encounter_type == "loot"):
					
					output_to_action_text("After a little searching, a chest comes into view, what would you like to do? " , True)
					# Open chest/crypt button
					action_window.open_chest_button.place(x = (615 * game_res_scale), y = 364 * game_res_scale)
					action_window.leave_chest_button.place(x = (250 * game_res_scale), y = 364 * game_res_scale)
					action_frame.after(300, action_window.chest_buttons_flash)
					
				elif(location.encounter_type == "ambush"):
					output_to_action_text("You have been ambushed!", True)
					combat_sequence(location.encounter)
					confirm_attack(None)
				elif(location.encounter_type == "fork"):
					
					output_to_action_text("You arrive at a fork in the road, which way would you like to go?", True)
					# Flash new buttons to grab attention of user
					action_window.left_at_fork_button.place(x = (250 * game_res_scale), y = 364 * game_res_scale)
					action_window.right_at_fork_button.place(x = (615 * game_res_scale), y = 364 * game_res_scale)
					action_frame.after(300, action_window.fork_buttons_flash)
					
			else:
				# Player has already visited this area
				output_to_action_text("You have already cleared this area.", True)
				action_window.draw_progression_buttons();
				action_window.enable_navigation();

		loadActionFrame(Adversary)


	def evoke_location(location):
		landing_text_option = ["You have arrived at", "You now find yourself at", "You have landed upon"]
		output_to_action_text(random.choice(landing_text_option) + " " + location.name, True)
		# Change title of action window to current location
		action_window.title.place_forget()
		action_window.title.config(text = location.name)
		action_window.title.place(x = (500 - len(game_map[player_character.current_map_index][player_character.current_town_index][player_character.current_location_index].name) * 5) * game_res_scale, y = -3)
		
		
	def pre_combat_sequence():
		global allow_ft_flag
		allow_ft_flag = False;
		action_window.pre_fight_options_show()

	def run_option():
		allow_ft_flag = True;
		action_window.pre_fight_options_hide()
		output_to_action_text("You attempt to run from the enemy", True)
		action_frame.after(1800, run_determine)


	def run_determine():
		# Calculate chance to escape enemy based off a flat 15% + players agility stat 
		if(15 + player_character.agility >= random.randrange(0, 101)):
			output_to_action_text("Your evasion attempt succeeded.", True)
			action_window.enable_navigation()
			action_window.draw_progression_buttons()
		else:
			output_to_action_text("Your evasion attempt failed, the enemy strikes first.", True)
			enemy_object = action_window.current_enemy;
			combat_sequence(enemy_object)
			confirm_attack(None)


	def fight_option():
		allow_ft_flag = True;
		enemy_object = action_window.current_enemy;
		action_window.pre_fight_options_hide()
		combat_sequence(enemy_object)


	def combat_sequence(enemy_object): 
		global Adversary
		# Flag combat in progress
		action_window.in_combat = True;
		Adversary = enemy_object;
		#
		# Draw enemy body part targeting buttons
		#
		loadActionFrame(Adversary)
		action_window.disable_navigation();


	def end_game(player_won = False):
		if(player_won):
			action_window.disable_navigation()

			# Define text file path 
			script_dir = os.path.dirname(__file__)
			player_data_file_path = script_dir + "\\GameData\\CharacterData\\player_data.txt"
			weapon_data_file_path = script_dir + "\\GameData\\CharacterData\\weapon_data.txt"

			output_to_action_text("Congratulations, you have defeated Master " + FileInterface.line_from_file(player_data_file_path, 0)[0], True)
			
			# Clear text files to prepare for wiring data
			FileInterface.clear_contents(player_data_file_path)
			FileInterface.clear_contents(weapon_data_file_path)

			# Dump data to text file
			FileInterface.append_data(player_data_file_path, player_character.name, False)      # Name
			FileInterface.append_data(player_data_file_path, player_character.health_max, True) # Health
			FileInterface.append_data(player_data_file_path, player_character.armour, True)		# Armour amount (int)
			with(open(weapon_data_file_path, 'wb')) as weapon_data_file:
				pickle.dump(player_character.equipped_weapon, weapon_data_file)					# current weapon

			# Assemble abosulte sprite path into a relational sprite path (not pc dependant that way)
			relevant_sprite_path = stats_window.player_sprite_path.split("\\")
			relevant_sprite_path = relevant_sprite_path[relevant_sprite_path.index("Sprites"):]
			new_sprite_path = []
			for directory in relevant_sprite_path:
				new_sprite_path.append("\\" + directory)

			new_sprite_path = "".join(new_sprite_path)

			# Append rest of the data to the text file
			FileInterface.append_data(player_data_file_path, new_sprite_path)	# Sprite of player
			FileInterface.append_data(player_data_file_path, "220,50;220,240;30,210;410,210;30,320;410,320", True) # Button locations	

			FileInterface.append_data(player_data_file_path, player_character.insight, True) # Insight	
			FileInterface.append_data(player_data_file_path, player_character.agility, True) # Agility	
			FileInterface.append_data(player_data_file_path, player_character.strength, True) # Strength	

			action_frame.after(4000, lambda:output_to_action_text("However... ", False))
			action_frame.after(5000, lambda:output_to_action_text("In doing so you have become the master for the next play through!", True))

			action_frame.after(9000, lambda:output_to_action_text("Exit whenever you're ready, or go back and explore the rest of the map.", True))


		else:
			action_window.disable_navigation()
			output_to_action_text("You have failed. ", False)
			action_frame.after(3000, lambda:output_to_action_text("Master " + FileInterface.line_from_file(os.path.dirname(__file__) + "\\GameData\\CharacterData\\player_data.txt", 0)[0] + " continues to reign supreme... ", True))
			action_frame.after(5000, lambda:output_to_action_text("Until next time.", True))
			action_frame.after(7000, lambda:output_to_action_text("<exit when ready>.", False))


	def chest_control(chest_state):
		action_window.open_chest_button.place_forget()
		action_window.leave_chest_button.place_forget()
		if(chest_state == False):
			# Player decided to leave chest alone
			output_to_action_text("You don't want to find out what was in that chest eh? Suit yourself.", True)
			action_window.draw_progression_buttons()
		else:
			# Player wishes to open chest

			# Determine chance for chest to be either real loot or a curse
			chance_for_curse = 18;
			loot_roll = random.randrange(0, 101)

			if(loot_roll <= chance_for_curse):
				# Flag a curse to occur if chest is opened
				encounter_type_special = "curse"
			else:
				# Flag loot to spwn if chest is opened
				encounter_type_special = "loot"
				# Generate loot 
				weapon_loot, armour_loot, items_loot, lootable_baguettes = ObjectHandling.generate_loot(random.randrange(1,3),random.randrange(0,2),random.randrange(1,4), game_progression = player_character.game_progression, fortune = player_character.fortune, tier=current_tier)

			if(encounter_type_special == "loot"):
				output_to_action_text("Your greed has paid dividends, enjoy the splendour.", True)
				Adversary.weapon_inventory = weapon_loot;
				Adversary.armour_inventory = armour_loot;
				Adversary.item_inventory = items_loot;
				loot_enemy(weapon_loot, armour_loot, items_loot, lootable_baguettes)
				


			elif(encounter_type_special == "curse"):
				output_to_action_text("Your greed has resulted in your downfall, you have been cursed!", True)

				# Determine which stats can be cursed (as long as the stats have enough points i.e. cant give player negative stats)
				if(player_character.health_max > 15):
					possible_curses = ["health"]
				else:
					possible_curses = []
				if(player_character.strength > 1):
					possible_curses.append("strength")
				if(player_character.fortune > 1):
					possible_curses.append("fortune")
				if(player_character.insight > 1):
					possible_curses.append("insight")
				if(player_character.charisma > 1):
					possible_curses.append("charisma")
				if(player_character.agility > 1):
					possible_curses.append("agility")

				try:
					cursed_object = random.choice(possible_curses)
				except Exception as exc:
					# If all stats are too low, we cant curse the player anymore
					output_to_action_text("It appears there is nothing left to curse! Good luck on your travels.", True)

				if(cursed_object == "health"):
					
					cursed_amount = random.randrange(7,16)

					# Update player's health
					player_character.health_max -= cursed_amount;
					# Ensure that players health isn't above new limit
					if(player_character.health > player_character.health_max):
						player_character.health = player_character.health_max;

				elif(cursed_object == "fortune"):
					if(player_character.fortune > 4):
						cursed_amount = random.randrange(1, 4)
					elif(player_character.fortune > 1):
						cursed_amount = random.randrange(1, player_character.fortune)

					# Deduct a small amount from respective stat as a ""curse"
					player_character.fortune -= cursed_amount;

				elif(cursed_object == "insight"):
					if(player_character.insight > 4):
						cursed_amount = random.randrange(1, 4)
					elif(player_character.insight > 1):
						cursed_amount = random.randrange(1, player_character.insight)

					# Deduct a small amount from respective stat as a ""curse"
					player_character.insight -= cursed_amount;

				elif(cursed_object == "charisma"):
					if(player_character.charisma > 4):
						cursed_amount = random.randrange(1, 4)
					elif(player_character.charisma > 1):
						cursed_amount = random.randrange(1, player_character.charisma)

					# Deduct a small amount from respective stat as a ""curse"
					player_character.charisma -= cursed_amount;

				elif(cursed_object == "agility"):
					if(player_character.agility > 4):
						cursed_amount = random.randrange(1, 4)
					elif(player_character.agility > 1):
						cursed_amount = random.randrange(1, player_character.agility)

					# Deduct a small amount from respective stat as a ""curse"
					player_character.agility -= cursed_amount;

				elif(cursed_object == "strength"):
					if(player_character.strength > 4):
						cursed_amount = random.randrange(1, 4)
					elif(player_character.strength > 1):
						cursed_amount = random.randrange(1, player_character.strength)

					# Deduct a small amount from respective stat as a ""curse"
					player_character.strength -= cursed_amount;
					

				output_to_action_text("Your " + cursed_object +" has been decreased by " + str(cursed_amount), True)
				action_window.draw_progression_buttons()

		player_character.update_stats()
		action_window.open_chest_button.place_forget()
		action_window.leave_chest_button.place_forget()
		action_window.enable_navigation()
		

	def loot_enemy(weapons, armour, items, baguettes): #After enemy is killed, display looting window and supply enemies' loot as arguments

		if(weapons != None and player_character.current_town_index != 8):
			output_to_action_text("You looted " + str(baguettes) + " baguettes.", True)
			player_character.baguettes += baguettes;
			action_window.looting = True;
			action_window.in_combat = False;
			action_window.context_image.place_forget()

			action_window.title.place_forget()
			action_window.title.config(text = "LOOT") # Change title to represent what is happening under "Action"
			action_window.title.place(x = 480 * game_res_scale, y = -3)

			# Place all required buttons and widgets required to loot
			action_window.loot_window.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale) 
			action_window.pickup_button.place(x = (250 * game_res_scale), y = 367 * game_res_scale)
			action_window.done_looting_button.place(x = (517 * game_res_scale), y = 367 * game_res_scale)

			# Remove clear text button as it will be in the way
			action_window.clear_textbox_button.place_forget()

			#Add all weapons in enemies' inventory to the lootable contents
			position_in_items = 0;
			action_window.loot_window.insert(END, insert_inventory_divider("weapon"))
			position_in_items += 1
			if(weapons != None):
				for i in weapons:
					# Get respective colour of item based off of tier
					relevant_colour = get_colour_tier(i)
					if(weapons[i] > 1):
						action_window.loot_window.insert(END,i.name + " (" + str(weapons[i]) + ") " +  get_sign_as_string( ((i.damage * i.shots_per_turn * (i.accuracy / 100)) * (1 + i.critical_chance / 50) ) - ((player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100)) * (1 + player_character.equipped_weapon.critical_chance / 50)) ) * int(abs(math.floor(((i.damage * i.shots_per_turn * (i.accuracy / 100) * (1 + i.critical_chance / 50)) - player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100) * (1 + player_character.equipped_weapon.critical_chance / 50)) / 5) )))
					else:
						action_window.loot_window.insert(END, i.name + " " + get_sign_as_string( ((i.damage * i.shots_per_turn * (i.accuracy / 100)) * (1 + i.critical_chance / 50) ) - ((player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100)) * (1 + player_character.equipped_weapon.critical_chance / 50)) ) * int(abs(math.floor(((i.damage * i.shots_per_turn * (i.accuracy / 100) * (1 + i.critical_chance / 50)) - player_character.equipped_weapon.damage * player_character.equipped_weapon.shots_per_turn * (player_character.equipped_weapon.accuracy / 100) * (1 + player_character.equipped_weapon.critical_chance / 50)) / 5) ))) 

					# Colour text in relation to weapon tier
					action_window.loot_window.itemconfig(position_in_items, fg=relevant_colour)
					position_in_items += 1
			
			#Add all armour in enemies' inventory to the lootable contents
			action_window.loot_window.insert(END, insert_inventory_divider("armour"))
			position_in_items += 1
			if(armour != None):
				for i in armour:
					relevant_colour = get_colour_tier(i)
					# Transform type of armour into index
					if(i.description == "helmet"):
						armour_description_id = 0;
					elif(i.description == "chest_piece"):
						armour_description_id = 1;
					elif(i.description == "left_arm"):
						armour_description_id = 2;
					elif(i.description == "right_arm"):
						armour_description_id = 3;
					elif(i.description == "left_leg"):
						armour_description_id = 4;
					else:
						armour_description_id = 5;

					if(armour[i] > 1):
						action_window.loot_window.insert(END, i.name + " (" + str(armour[i]) + ") " + get_sign_as_string(i.protection - player_character.equipped_armour[armour_description_id].protection) * int(abs(math.floor(i.protection - player_character.equipped_armour[armour_description_id].protection) / 2)))
					else:
						action_window.loot_window.insert(END, i.name  + " " + get_sign_as_string(i.protection - player_character.equipped_armour[armour_description_id].protection) * int(abs(math.floor(i.protection - player_character.equipped_armour[armour_description_id].protection) / 2)))
					action_window.loot_window.itemconfig(position_in_items, fg=relevant_colour)
					position_in_items += 1

			action_window.loot_window.insert(END, insert_inventory_divider("item"))
			if(items != None):
				if(len(items) > 0):
					#Add all items in enemies' inventory to the loot-able contents
					for i in items:
						action_window.loot_window.insert(END, i.name + " (" + str(items[i]) + ")")
		
		else:
			# Must be the end of the game
			end_game(True)


	def output_to_action_text(text, new_line): #Display to command window inside action sequence, new_line parameter for appending a newline after the message
		
		upper_threshold = 0.1;
		lower_threshold = 0.02;
		time_per_character = lower_threshold - (len(text) / (10 * 100))  

		time_per_character = clamp(time_per_character, lower_threshold, upper_threshold)

		# If new_line is flagged as true, insert a special character ("@") symbol to end of string, this will then be read and converted to a new line symbol when displaying to text box
		if(new_line == True):
			text = list(text);
			text.append("@")
			new_text = ""
			text = new_text.join(text)

		time_step = 1
		for character in text:
			char_q.append(character)
			action_window.main_textbox.after(len(char_q) * 25, lambda:next_char())
			time_step += int(time_per_character * 1000)

		action_window.main_textbox.config(state=DISABLED)

	def next_char(): # Writes the next character in the char_q array to the main action window text box
		action_window.main_textbox.config(state=NORMAL)
		if(char_q[0] == "@"):
			action_window.main_textbox.insert(END, "\n")
			char_q.pop(0)
		else:
			action_window.main_textbox.insert(END, char_q.pop(0))
		action_window.main_textbox.yview(END)
		action_window.main_textbox.config(state=DISABLED)

	def output_to_item_description(text): # Writes text information to highlighted inventory item display
		for character in text:
			inventory_window.item_description.insert(END, character)


	###############################################################################################

	#INITIALIZATION OF GUI WINDOW##################################### 
	def quit_program():
		root.quit()
		root.destroy()
		os._exit(1)

	def run_guide(stage): # Draw players attention to map button

		if(not map_button_pressed and stage == 0):
			action_window.map_button.flash()
			action_window.map_button.flash()
			action_window.map_button.flash()
			action_frame.after(4000, lambda:run_guide(0))
		if(stage == 1 and player_character.picked_starting_location == False):
			if(active_frame == map_frame):
				# Change the active background colour of the buttons so that the flash is very noticeable
				game_map[0][0][0].my_button_container.button.configure(activebackground="brown")
				game_map[1][0][0].my_button_container.button.configure(activebackground="brown")
				# Flash the buttons multiple times
				for i in range(0, 2):
					game_map[0][0][0].my_button_container.button.flash()
					game_map[1][0][0].my_button_container.button.flash()
				game_map[0][0][0].my_button_container.button.configure(activebackground="white")
				game_map[1][0][0].my_button_container.button.configure(activebackground="white")
			action_frame.after(4000, lambda:run_guide(1))


	root = Tk() # Create root program
	
	# Define window parameters 
	window_width = int(game_resolution.split("x")[0])
	window_height = int(game_resolution.split("x")[1])
	action_frame = Frame(root, width = window_width, height = window_height, bg="#333") #Decide on colour scheme
	inventory_frame = Frame(root, width = window_width, height = window_height, bg="#333") # Dark slate blue/grey = #708090
	map_frame = Frame(root, width = window_width, height = window_height, bg="#333")
	stats_frame = Frame(root, width = window_width, height = window_height, bg="#333") 

	# Customise applications
	root.title("Full Metal Baguette")
	root.geometry(game_resolution)  
	root.resizable(False, False)
	# Get screen parameters
	screen_width = root.winfo_screenwidth() 
	screen_height = root.winfo_screenheight()
	action_frame.pack()
	# Keep track of active frame
	active_frame = action_frame;


	# Create an array of all sprites to be used for each point of interest
	location_images = []
	location_images_in_folder = (len(next(os.walk(os.path.dirname(__file__) + "\\Sprites\\Locations"))[2])) - 3; # Minus 3 due to circumstantial images

	for i in range(1, location_images_in_folder + 1):
		if(i < 10):
			i = "0" + str(i)
		else:
			i = str(i)
		
		location_images.append(ImageHandling.get_location_sprite("Location" + i, game_res_scale))

	# Create an array of all sprites to be used for each town
	town_images = []
	town_images_in_folder = (len(next(os.walk(os.path.dirname(__file__) + "\\Sprites\\Towns"))[2])) - 1; # Minus 1 due to circumstantial image;

	for i in range(1, town_images_in_folder + 1):
		if(i < 10):
			i = "0" + str(i)
		else:
			i = str(i)
		
		town_images.append(ImageHandling.get_location_sprite("Town" + i, game_res_scale))

	# Define cicumstantial images
	start_image = ImageHandling.get_location_sprite("Location_Start", game_res_scale)
	end_image = ImageHandling.get_location_sprite("Town_End", game_res_scale)
	service_station_image = ImageHandling.get_location_sprite("Location_Loot", game_res_scale)


	# Create two different, randomly-generated parallel game worlds so that switching between two maps can occur
	game_map_1 = generate_map(8, 0)
	game_map_2 = generate_map(8, 1)
	game_map = [game_map_1, game_map_2]

	for frame in (action_frame, inventory_frame, map_frame, stats_frame):
		frame.grid(row=0, column=0, sticky='news')

	noEnemyIMG = ImageHandling.get_enemy_sprite("NoEnemy", game_res_scale)


	schedule_thread = new_thread(); # Create new thread after GUI is initialised 
	#Defining Starting inventory items
	default_weapon = Weapon("Fists", "melee", 3, 25, 99, 0, 1, 0, 1, 0, "Fist", 0) #Default weapon if you drop all of your weapons
	default_armour = Armour("all", "Bare Skin", 0, 0, 1, 0) # Default armour that will be equipped if you drop all of your armour

	leather_helmet = Armour("helmet", "Leather Helmet", 2, 3, 1, 2)
	starting_armour = Armour("chest_piece", "Cotton Shirt", 3, 4, 1, 2)
	wool_left_arm = Armour("left_arm", "Wool Left Arm", 1, 2, 1, 2)
	wool_right_arm = Armour("right_arm", "Wool Right Arm", 1, 2, 1, 2)
	wool_left_leg = Armour("left_leg", "Wool Left Leg", 2, 2, 1, 2)
	wool_right_leg = Armour("right_leg", "Wool Right Leg", 2, 2, 1, 2)

	starting_weapon = Weapon("Baguette Blaster", "ranged", 10, 15, 70, 7, 1, 3, 1, 6, "9mm", 5)

	# Create player 
	player_character = Player(player_stats[0], 100, [leather_helmet, starting_armour, wool_left_arm, wool_right_arm, wool_left_leg, wool_right_leg], starting_weapon, player_stats[1], player_stats[2])

	player_character.add_item(starting_weapon, 1)
	player_character.add_item(leather_helmet, 1)
	player_character.add_item(starting_armour, 1)
	player_character.add_item(wool_left_arm, 1)
	player_character.add_item(wool_right_arm, 1)
	player_character.add_item(wool_left_leg, 1)
	player_character.add_item(wool_right_leg, 1)
	
	# Define an empty enemy
	Adversary = Enemy("", 0, 0, None, noEnemyIMG, None, None, None, 0, [0], False, 0)
	
	encounter_active = False;
	current_tier = 1;

	action_window = ActionWindow(root)
	inventory_window = InventoryWindow()
	map_window = MapWindow()
	stats_window = StatsWindow()

	loadActionFrame(Adversary)

	# Alert player to map button
	map_button_pressed = False;
	run_guide(0)

	# Define protocol to ensure program knows how to close correctly
	root.protocol("WM_DELETE_WINDOW", quit_program)

	root.mainloop()
 