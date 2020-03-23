class Player:
	def __init__(self, name, health, armour, currentWeapon, stats):
		self.name = name
		self.health = health
		self.equipped_armour = armour #[0] = Helmet [1] = Chest_Piece [2] = Left_Arm [3] = Right_Arm [4] = Left_Leg [5] = Right_Leg
		
		self.strength = stats[0]
		self.insight = stats[1]
		self.fortune = stats[2]
		self.charisma = stats[3]
		self.agility = stats[4]

		self.game_progression = 0
		self.towns_discovered = 0
		self.current_town = None
		self.max_carry_weight = 125

		self.update_armour_total()

		self.equipped_weapon = currentWeapon

		self.weapon_inventory = {
		
		}

		self.armour_inventory = {
			
		}

		self.item_inventory = {
			
		}

	def take_damage(self, amount):

		if(self.armour > 400):
			self.armour = 400 #Cap at 400 otherwise protection amount = > 1 meaning attacks will deal negative damage (essentially healing you)
			
		protectionAmount = ((math.log2(self.armour + 64) / 3) * 100 - 200)  / 100 #Given the amount of armour the player has, calculate percentage of damage to reduce

		damage_dealt = round((amount + random.randrange(round(-self.armour / 8), round(amount / 5))) *  (1 - protectionAmount))
		if(damage_dealt < 0):
			damage_dealt = 0 
		self.health = self.health - damage_dealt

		action_window.main_textbox.config(state=NORMAL)
		action_window.main_textbox.insert(END, " " + str(damage_dealt) + " damage\n")
		action_window.main_textbox.config(state=DISABLED)

	def deal_damage(self):
		action_window.main_textbox.config(state=NORMAL)
		player_attack_hit = random.randrange(1, 101) <= self.equipped_weapon.accuracy #Calculate if attack hit based on players current weapon accuracy
		if(player_attack_hit == True):
			if(random.randrange(1, 101) <= self.equipped_weapon.critical_chance): #Hit did crit
				action_window.main_textbox.insert(END, "Crit for")
				Adversary.takeDamage(self.equipped_weapon.damage * 2) #Apply damage * 2 due to crit
			else:
				action_window.main_textbox.insert(END, "Hit for")
				Adversary.takeDamage(self.equipped_weapon.damage) #Apply standard weapon damage 
		else:
			#Hit missed
			action_window.main_textbox.insert(END, "Missed\n")

		action_window.main_textbox.config(state=DISABLED)
		loadActionFrame(Adversary)
		
	def heal(self, amount):
		self.health = self.health + amount

	def update_armour_total(self):
		self.armour = 0
		for armour in self.equipped_armour:
			self.armour += armour.protection

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

	def drop_item(self, index=None):

		item_to_drop_index = inventory_window.inventory_contents.curselection() #Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" also counts as an index)
		try:
			item_to_drop_index = item_to_drop_index[0]
		except Exception as e:
			return

		item_to_drop = self.get_item_in_inventory(item_to_drop_index)

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
					if(armour_item.description == item_to_drop[0].description): #Check if any are matching types (e.g left arm = left arm)
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
			item_to_drop = self.get_item_in_inventory(item_to_drop_index)
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


		
		
		self.update_armour_total()
		loadInventoryFrame()

	def equip_item(self, given_item=None):
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
				self.drop_item(item_to_equip_index)

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
		item_to_pickup_index = action_window.loot_window.curselection() # Get the index of the item to pick up within the window (Keeping in mind that the "---Weapons---" also counts as an index)

		try:
			item_to_pickup_index = item_to_pickup_index[0]
		except Exception as ex:
			return

		item = Adversary.get_item_in_inventory(item_to_pickup_index) 

		if(item != None): # A valid object has been selected to pick-up
			self.add_item(item[0], 1) # Add item to your inventory
			Adversary.drop_item(item_to_pickup_index) # Remove item from adversary inventory
			
			text_to_pickup = action_window.loot_window.get(item_to_pickup_index)
			text_to_pickup_list = text_to_pickup.replace("(", "").replace(")", "")
			text_to_pickup_list = text_to_pickup_list.split(" ")
			
			try:
				quantity = int(text_to_pickup_list[len(text_to_pickup_list) - 1])
				action_window.loot_window.delete(item_to_pickup_index)
				if(quantity > 1):
					action_window.loot_window.insert(item_to_pickup_index, text_to_pickup[:len(text_to_pickup) - (2 + len(str(quantity)))] + "(" + str(quantity - 1) + ")")
				else:
					action_window.loot_window.delete(item_to_pickup_index)

			except Exception as ex:
				action_window.loot_window.delete(item_to_pickup_index) # Remove from avaliable loot
			



	def get_item_in_inventory(self, index):
		item_iterator = index + 1
		weapon_inv_length = len(self.weapon_inventory)
		armour_inv_length = len(self.armour_inventory)
		item_inv_length = len(self.item_inventory)

		item_iterator -= 1
		index -= 1


		if(item_iterator > weapon_inv_length): # Item is not in weapons inventory
			item_iterator -= weapon_inv_length + 1 # Add one becasue of the divider we have in the text box
			index -= weapon_inv_length + 1 # Add one becasue of the divider we have in the text box

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
	def __init__(self, name, weapon_type, damage, criticalChance, accuracy, magazine_capacity, shots_per_turn, weight):
		self.name = name
		self.damage = damage
		self.critical_chance = criticalChance
		self.accuracy = accuracy
		self.weapon_type = weapon_type
		self.magazine_capacity = magazine_capacity
		self.current_ammo = self.magazine_capacity
		self.shots_per_turn = shots_per_turn
		self.weight = weight

class Armour:
	def __init__(self, description, name, protection, weight):
		self.description = description
		self.name = name
		self.protection = protection
		self.weight = weight

class Item:		#Ensure classes remain consistent throughout modules (Object handling of primary concern)

	def __init__(self, item):
		if(item == "stimpak"):
			self.Stimpak()
		elif(item == "gene_synthesiser"):
			self.Gene_synthesiser()

	def Stimpak(self):
		self.name = "Stimpak"
		self.amount = 10
		self.weight = 0.5
		self.variation = "consumable"
		self.affector = "health"

	def Gene_synthesiser(self):
		self.name = "Gene-synthesiser"
		self.amount = 1
		self.weight = 0.5
		self.variation = "consumable"
		self.affector = "player_stats"

	def consume(self, obj_effector):
		obj_effector.health += self.amount # Update to add further variation 


#CLASSES
class ActionWindow():

	def __init__(self):
		self.title = Label(action_frame, text='ACTION', font=("Courier", 14), bg="#333")
		self.action_button = Button(action_frame, text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",state = DISABLED,  command=lambda:loadActionFrame())
		self.map_button = Button(action_frame, text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(action_frame, text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(action_frame, text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:load_stats_frame())
		self.enemy_description_text = Text(action_frame, height = round(10 * game_res_scale), width = round(23 * game_res_scale), font=("Courier", round(12)))
		
		self.done_looting_button = Button(action_frame, text="Done", width = round(36 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge", command=lambda:self.done_looting())
		self.pickup_button = Button(action_frame, text="Pick-up", width = round(36 * game_res_scale), height = round(1 * game_res_scale), relief = "ridge",command=lambda:player_character.pick_up_item())

		#Load image
		try:
			self.context_image = Label(action_frame, image = Adversary.sprite,)
		except:
			self.context_image = Label(action_frame, image = noEnemyIMG)

		
		self.player_description_text = Text(action_frame, height = round(10 * game_res_scale), width = round(23 * game_res_scale), font=("Courier", round(12)))
		self.attack_button = Button(action_frame, text = "ATTACK", state = DISABLED, command = player_character.deal_damage) #IF GOON.name == "none" then disable button

		self.main_textbox = Text(action_frame, height = round(10 * game_res_scale), width = round(65 * game_res_scale), font=("Courier", round(10)))
		self.scrollbar = Scrollbar(self.main_textbox, orient="vertical")
		self.main_textbox.config(yscrollcommand=self.scrollbar.set, state = DISABLED)
		self.scrollbar.place(x = 505 * game_res_scale, y = 0)

		self.bug_test_button = Button(action_frame, text = "TEST", command=combatSequence) 

		self.title.place(x= (500 * game_res_scale) - 20, y = -3)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.enemy_description_text.place(x = 5* game_res_scale, y = 50 * game_res_scale)
		self.context_image.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale) 
		self.player_description_text.place(x = 780* game_res_scale, y = 50* game_res_scale)
		self.attack_button.place(x = 790 * game_res_scale, y = 235* game_res_scale)
		self.bug_test_button.place(x = 0, y = 0)
		self.main_textbox.place(x = (window_width / 4) - (5 * game_res_scale), y = 405 * game_res_scale)

		self.loot_window = Listbox(action_frame, height = round(18 * game_res_scale), width = round(52 * game_res_scale), font=("Courier", round(12))) #Perform last as to draw it over image 


	def done_looting(self):
		self.done_looting_button.place_forget() #When the player hits the DONE button, hide all looting related widgets
		self.loot_window.place_forget()
		self.pickup_button.place_forget()
		self.loot_window.delete(0, END) #Delete contents of loot window to prevent doubling up of items
		self.title.config(text = "ACTION") #Change title from loot to action
 


class InventoryWindow():

	def __init__(self):
		self.title = Label(inventory_frame, text='INVENTORY', font=("Courier", 12))
		self.action_button = Button(inventory_frame, text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(inventory_frame, text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(inventory_frame, text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED , relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(inventory_frame, text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:load_stats_frame())
		self.scrollbar = Scrollbar(inventory_frame)
		self.scrollbar.pack(side=LEFT, fill=Y)
		self.inventory_contents = Listbox(inventory_frame, yscrollcommand=self.scrollbar.set, height = round(18 * game_res_scale) , width = round(52 * game_res_scale), font=("Courier", round(14)))
		self.inventory_drop_button = Button(inventory_frame, text = "Drop", width = round(40 * game_res_scale), height = round(1 * game_res_scale), command = lambda:player_character.drop_item())
		self.equip_item_button = Button(inventory_frame, text = "Equip", width = round(40 * game_res_scale), height = round(1 * game_res_scale), command = lambda:player_character.equip_item() )
		self.scrollbar.config(command=self.inventory_contents.yview)
		
		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)
		self.inventory_contents.place(x =16 , y = 50 * game_res_scale)
		self.inventory_drop_button.place(x = 16, y = 448 * game_res_scale)
		self.equip_item_button.place(x = 16 + (286 * game_res_scale), y = 448 * game_res_scale)


class MapWindow():

	def __init__(self):
		self.title = Label(map_frame, text='MAP', font=("Courier", 12))
		self.action_button = Button(map_frame, text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(map_frame, text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED, relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(map_frame, text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(map_frame, text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:load_stats_frame())

		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)


class StatsWindow():

	def __init__(self):
		self.title = Label(stats_frame, text="STATS", font=("Courier", 12))
		self.action_button = Button(stats_frame, text='Action', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge",  command=lambda:loadActionFrame(Adversary))
		self.map_button = Button(stats_frame, text='Map', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadMapFrame())
		self.inventory_button = Button(stats_frame, text='Inventory', width = round(7 * game_res_scale), height = round(2 * game_res_scale), relief="ridge", command=lambda:loadInventoryFrame())
		self.stats_button = Button(stats_frame, text="Stats", width = round(7 * game_res_scale), height = round(2 * game_res_scale), state = DISABLED, relief="ridge", command=lambda:load_stats_frame())

		self.title.place(x= (500 * game_res_scale) - 20, y = 0)
		self.action_button.place(x = 783 * game_res_scale, y = 0)
		self.inventory_button.place(x = 843 * game_res_scale, y = 0)
		self.map_button.place(x = 903 * game_res_scale, y = 0)
		self.stats_button.place(x = 963 * game_res_scale, y = 0)



class InventoryDivider:
	def __init__(self, text):
		self.text = text

class NPC:
	def __init__(self, name):
		self.name = name

class Enemy:
	def __init__(self, name, health, armour, current_weapon, sprite, weapon_inventory, armour_inventory, item_inventory):
		self.name = name
		self.health = health
		self.armour = armour
		if(current_weapon != None):
			self.current_weapon = current_weapon
			self.damage = current_weapon.damage
		else:
			damage = 0
			self.current_weapon = None
		self.sprite = sprite

		self.weapon_inventory = weapon_inventory

		self.armour_inventory = armour_inventory

		self.item_inventory = item_inventory

	def takeDamage(self, amount):

		if(self.armour > 400):
			self.armour = 400 #Cap at 400 otherwise protection amount = > 1 meaning attacks will deal negative damage (essentially healing you)

		protectionAmount = ((math.log2(self.armour + 64) / 3) * 100 - 200)  / 100 

		damage_dealt = round((amount + random.randrange(round(-self.armour / 8), round(amount / 5))) *  (1 - protectionAmount))
		if(damage_dealt < 0):
			damage_dealt = 0 
		self.health = self.health - damage_dealt

		if(self.health <= 0):
			self.die()

		action_window.main_textbox.config(state=NORMAL) #Allow writing to main text box
		action_window.main_textbox.insert(END, " " + str(damage_dealt) + " damage\n")
		action_window.main_textbox.yview(END) #Auto scroll main text box when new text is added
		action_window.main_textbox.config(state=DISABLED) #Disable player being able to manipulate text in main text box



	def die(self):

		self.name = ""
		self.health = 0
		self.damage = 0
		self.sprite = noEnemyIMG

		# Progress player each time they kill an enemy
		player_character.game_progression += 1;
		loot_enemy(self.weapon_inventory, self.armour_inventory, self.item_inventory)

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
		weapon_inv_length = len(self.weapon_inventory)
		armour_inv_length = len(self.armour_inventory)
		item_inv_length = len(self.item_inventory)

		item_iterator -= 1
		index -= 1


		if(item_iterator > weapon_inv_length): #Item is not in weapons inventory
			item_iterator -= weapon_inv_length + 1 #Add one becasue of the divider we have in the text box
			index -= weapon_inv_length + 1 #Add one becasue of the divider we have in the text box

			if(item_iterator > armour_inv_length): #Item is not in armour inventory
				item_iterator -= armour_inv_length + 1 #Add one becasue of the divider we have in the text box
				index -= armour_inv_length + 1 #Add one becasue of the divider we have in the text box

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











if __name__ == "__main__":
	from Conventions import *
	import os, random, time, schedule, math
	import Inventory, MyDictionary, eGraphh, TkinterResolution, ElapsedTime, ImageHandling, CharacterSetup, ObjectHandling #My own functions
	from tkinter import *
	from PIL import ImageTk, Image

	game_resolution = TkinterResolution.get_user_resolution("1024x576", "1280x720", "1920x1080", "2560x1440")
	ElapsedTime.initialise_elapsed_time()
	game_res_scale = int(game_resolution.split("x")[0]) / 1024 # Used to scale all widgets in window -

	player_stats = CharacterSetup.get_character_customisation()


	#Functions for handling frames###########################################################################
	def raise_frame(frame):
		frame.tkraise()

	def loadActionFrame(enemyOBJ):
		global Action_Window_Enemy_Sprite

		action_frame.tkraise() #Make Func of class
		action_window.enemy_description_text.configure(state = NORMAL)
		action_window.enemy_description_text.delete(1.0, END)

		action_window.player_description_text.configure(state = NORMAL)
		action_window.player_description_text.delete(1.0, END)

		if(enemyOBJ.name != ""):
			textToInsert = "ENEMY: " + enemyOBJ.name + "\nHealth = " + str(enemyOBJ.health) + "\nArmour = " + str(enemyOBJ.armour) + "\nDamage = " + str(enemyOBJ.damage)
			action_window.enemy_description_text.insert(END, textToInsert)
			action_window.attack_button.configure(state = NORMAL)
		else:
			action_window.attack_button.configure(state = DISABLED)

		playerTextToInsert = player_character.name + ":\nHealth = " + str(player_character.health) + "\nArmour: " + str(player_character.armour) + "\nWEAPON: " + player_character.equipped_weapon.name + "\nDamage = " + str(player_character.equipped_weapon.damage) + "\nAccuracy = " + str(player_character.equipped_weapon.accuracy) #Player name from SPECIAL screen
		action_window.player_description_text.insert(END, playerTextToInsert)

		action_window.enemy_description_text.configure(state = DISABLED)
		action_window.player_description_text.configure(state = DISABLED)

		action_window.context_image.configure(image = enemyOBJ.sprite)
		action_window.context_image.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale) 

		action_window.main_textbox.configure(yscrollcommand=action_window.scrollbar.set)
		action_window.scrollbar.config(command=action_window.main_textbox.yview)
		
		
	def loadInventoryFrame():
		inventory_frame.tkraise()
		inventory_window.inventory_contents.configure(state = NORMAL) #Allowing writes to text 
		inventory_window.inventory_contents.delete(0, END) #Delete all contents
		
		inventory_window.inventory_contents.insert(END, weapon_inventory_divider.text)
		#Add all weapons in inventory to inventory contents
		for i in player_character.weapon_inventory:
			#Label equipeed weapons with a ">" prefix
			if(i == player_character.equipped_weapon):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""

			if(player_character.weapon_inventory[i] > 1):
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " (" + str(player_character.weapon_inventory[i]) + ")")
			else:
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name)

		inventory_window.inventory_contents.insert(END, armour_inventory_divider.text)
		#Add all armour in inventory to inventory contents
		for i in player_character.armour_inventory:
			#Label equipeed armour with a ">" prefix
			if(i in player_character.equipped_armour):
				equippedIndicator = "> "
			else:
				equippedIndicator = ""

			if(player_character.armour_inventory[i] > 1):
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name + " (" + str(player_character.armour_inventory[i]) + ")")
			else:
				inventory_window.inventory_contents.insert(END, equippedIndicator + i.name)

		inventory_window.inventory_contents.insert(END, item_inventory_divider.text)
		#Add all items in inventory to inventory contents
		for i in player_character.item_inventory:
			inventory_window.inventory_contents.insert(END, i.name + " (" + str(player_character.item_inventory[i]) + ")")

		inventory_window.inventory_contents.configure(yscrollcommand=inventory_window.scrollbar.set)
		inventory_window.scrollbar.config(command=inventory_window.inventory_contents.yview)

		#inventory_window.inventory_contents.configure(state = DISABLED) #Disallowing writes to text 

	def loadMapFrame():
		map_frame.tkraise()

	def load_stats_frame():
		stats_frame.tkraise()



	###############################################################################################

	#Function For Handling Game###############################################################################################
		
	def combatSequence():#name, health, armour, damage, sprite):
		global Adversary 
		adversary_data = ObjectHandling.create_enemy(game_resolution, player_character.game_progression, player_character.towns_discovered, player_character.current_town, None, "GoonTest")
		Adversary = Enemy(adversary_data[0], adversary_data[1], adversary_data[2], adversary_data[3], adversary_data[7], adversary_data[4], adversary_data[5], adversary_data[6]) 
		#combatSequence(MyDictionary.GetName("male", True, False, False), 20, 3, 5, basicGoonIMG)
		loadActionFrame(Adversary)

	def loot_enemy(weapons, armour, items): #After enemy is killed, display looting window and supply enemies' loot as arguments
		action_window.context_image.place_forget()
		action_window.title.config(text = "LOOT")

		action_window.loot_window.place(x = (window_width / 2) - (262 * game_res_scale), y = 20 * game_res_scale) 
		action_window.pickup_button.place(x = (250 * game_res_scale), y = 367 * game_res_scale)
		action_window.done_looting_button.place(x = (517 * game_res_scale), y = 367 * game_res_scale)

		#Add all weapons in enemies' inventory to the lootable contents
		action_window.loot_window.insert(END, weapon_inventory_divider.text)
		for i in weapons:
			if(weapons[i] > 1):
				action_window.loot_window.insert(END,i.name + " (" + str(weapons[i]) + ")")
			else:
				action_window.loot_window.insert(END, i.name)

		action_window.loot_window.insert(END, armour_inventory_divider.text)
		#Add all armour in enemies' inventory to the lootable contents
		for i in armour:

			if(armour[i] > 1):
				action_window.loot_window.insert(END, i.name + " (" + str(armour[i]) + ")")
			else:
				action_window.loot_window.insert(END, i.name)

		action_window.loot_window.insert(END, item_inventory_divider.text)
		if(len(items) > 0):
			#Add all items in enemies' inventory to the lootable contents
			for i in items:
				action_window.loot_window.insert(END, i.name + " (" + str(items[i]) + ")")



	#def output() #Display to command window inside action sequence


	###############################################################################################

	#INITIALIZATION OF GUI WINDOW##################################### 
	root = Tk()
	window_width = int(game_resolution.split("x")[0])
	window_height = int(game_resolution.split("x")[1])
	action_frame = Frame(root, width = window_width, height = window_height, bg="#333") #Decide on colour scheme
	inventory_frame = Frame(root, width = window_width, height = window_height, bg="#333")
	map_frame = Frame(root, width = window_width, height = window_height, bg="#333")
	stats_frame = Frame(root, width = window_width, height = window_height, bg="#333") 

	root.title("S.T.A.V")
	root.geometry(game_resolution)  
	root.resizable(False, False)
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	action_frame.pack()


	for frame in (action_frame, inventory_frame, map_frame, stats_frame):
		frame.grid(row=0, column=0, sticky='news')


	basicGoonIMG = ImageHandling.get_sprite("GoonTest", game_resolution)
	noEnemyIMG = ImageHandling.get_sprite("NoEnemy", game_resolution)


	#Defining Starting inventory items
	default_weapon = Weapon("Fists", "melee", 3, 25, 99, 0, 1, 0) #Default weapon if you drop all of your weapons
	default_armour = Armour("all", "Bare Skin", 0, 0) #Default armour if you drop all of your armour

	leather_helmet = Armour("helmet", "Leather Helmet", 2, 3)
	starting_armour = Armour("chest_piece", "Cotton Shirt", 3, 4)
	wool_left_arm = Armour("left_arm", "Wool Left Arm", 1, 2)
	wool_right_arm = Armour("right_arm", "Wool Right Arm", 1, 2)
	wool_left_leg = Armour("left_leg", "Wool Left Leg", 2, 2)
	wool_right_leg = Armour("right_leg", "Wool Right Leg", 2, 2)

	starting_weapon = Weapon("Rusty Handgun", "ranged", 10, 15, 85, 7, 1, 3)

	player_character = Player(player_stats[0], 100, [leather_helmet, starting_armour, wool_left_arm, wool_right_arm, wool_left_leg, wool_right_leg], starting_weapon, player_stats[1])

	player_character.add_item(starting_weapon, 1)
	player_character.add_item(leather_helmet, 1)
	player_character.add_item(starting_armour, 1)
	player_character.add_item(wool_left_arm, 1)
	player_character.add_item(wool_right_arm, 1)
	player_character.add_item(wool_left_leg, 1)
	player_character.add_item(wool_right_leg, 1)
	player_character.add_item(Item("stimpak"), 2)


	Adversary = Enemy("", 0, 0, None, noEnemyIMG, None, None, None)


	#############################################


	weapon_inventory_divider = InventoryDivider("-" * (23 + round(1 + (game_res_scale - 1) * 24)) + "Weapons" + "-" * round(100 * game_res_scale)) #Create drividers for inventory contents label with scaling 
	armour_inventory_divider = InventoryDivider("-" * (23 + round(1 + (game_res_scale - 1) * 24)) + "Armour" + "-" * round(100 * game_res_scale)) #Create drividers for inventory contents label with scaling 
	item_inventory_divider = InventoryDivider("-" * (23 + round(1 + (game_res_scale - 1) * 24)) + "Items" + "-" * round(100 * game_res_scale)) #Create drividers for inventory contents label with scaling 


	action_window = ActionWindow()
	inventory_window = InventoryWindow()
	map_window = MapWindow()
	stats_window = StatsWindow()


	loadActionFrame(Adversary)
	root.mainloop()
