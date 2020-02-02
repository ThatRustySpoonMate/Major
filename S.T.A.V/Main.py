from Conventions import *
import os, random, time, schedule
import Inventory, MyDictionary, eGraphh, TkinterResolution
from tkinter import *
from PIL import ImageTk, Image

game_resolution = TkinterResolution.getUserResolution("1024x576", "1280x720", "1920x1080", "2560x1440")

game_res_scale = int(game_resolution.split("x")[0]) / 1024
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

initial_time = time.time()

#Functions for handling frames###########################################################################
def raise_frame(frame):
    frame.tkraise()

def loadActionFrame(enemyOBJ, weaponObj):
	ActionFrame.tkraise()
	EnemyDescriptionText.configure(state = NORMAL)
	EnemyDescriptionText.delete(1.0, END)

	PlayerDescriptionText.configure(state = NORMAL)
	PlayerDescriptionText.delete(1.0, END)

	if(enemyOBJ.name != ""):
		textToInsert = "ENEMY: " + enemyOBJ.name + "\nHealth = " + str(enemyOBJ.health) + "\nArmour = " + str(enemyOBJ.armour) + "\nDamage = " + str(enemyOBJ.damage)
		EnemyDescriptionText.insert(END, textToInsert)
		FireButton.configure(state = NORMAL)
	else:
		FireButton.configure(state = DISABLED)

	playerTextToInsert = "YOU:\nHealth = " + str(MainCharacter.health) + "\nARMOUR = " + str(MainCharacter.armour.name) + "\nProtection = " + str(MainCharacter.armour.protection) + "\nWEAPON: " + equippedWeapon.name + "\nDamage = " + str(equippedWeapon.damage) + "\nAccuracy = " + str(equippedWeapon.accuracy)
	PlayerDescriptionText.insert(END, playerTextToInsert)

	EnemyDescriptionText.configure(state = DISABLED)
	PlayerDescriptionText.configure(state = DISABLED)

	EnemySprite = Label(ActionFrame, image = enemyOBJ.sprite)
	EnemySprite.grid(column = 4, row = 1, columnspan = 8, rowspan = 5)
	
	
def loadInventoryFrame():
	InventoryFrame.tkraise()
	InventoryContents.configure(state = NORMAL) #Allowing writes to text 
	InventoryContents.delete(1.0, END)
	AllWeaponsLi = Inventory.RetrieveItemsFromTab(1)
	AllArmourLi = Inventory.RetrieveItemsFromTab(3)
	AllItemsLi = Inventory.RetrieveItemsFromTab(2)
	AllWeapons = ""
	AllArmour = ""
	AllItems = ""

	WeaponSingleRun = True
	ArmourSingleRun = True
	ItemSingleRun = True
	for item in AllWeaponsLi:
		if(WeaponSingleRun):
			WeaponSingleRun = False
			AllWeapons = AllWeapons + item +  " - "
		else:
			AllWeapons = AllWeapons + item.name + ", "
	for item in AllArmourLi:
		if(ArmourSingleRun):
			ArmourSingleRun = False
			AllArmour = AllArmour + item +  " - "
		else:
			AllArmour = AllArmour + item.name + ", "
	for item in AllItemsLi:
		if(ItemSingleRun):
			ItemSingleRun = False
			AllItems = AllItems + item +  " - "
		else:
			AllItems = AllItems + item.name + ", "

	InventoryContentsToDisplay = AllWeapons + "\n" + AllArmour + "\n" + AllItems
	InventoryContents.insert(END, InventoryContentsToDisplay)

	InventoryContents.configure(state = DISABLED) #Disallowing writes to text 

def loadMapFrame():
	MapFrame.tkraise()

###############################################################################################

#Function For Handling Game###############################################################################################

def dealDamage():
	Adversary.takeDamage(MainCharacter.currentWeapon.damage)
	loadActionFrame(Adversary, MainCharacter.currentWeapon)

def combatSequence():#name, health, armour, damage, sprite):
	global Adversary 
	Adversary = Enemy("Test", 20, 3, 5, basicGoonIMG)
	#combatSequence(MyDictionary.GetName("male", True, False, False), 20, 3, 5, basicGoonIMG)
	loadActionFrame(Adversary, MainCharacter.currentWeapon)

def get_elapsed_time(initial_time):

    current_time = time.time()

    elapsed_time = current_time - initial_time
    return(round(elapsed_time))


#def output() #Display to command window inside action sequence



###############################################################################################

#INITIALIZATION OF GUI WINDOW##################################### 
root = Tk()
ActionFrame = Frame(root, width = "1024", height = "576")
InventoryFrame = Frame(root, width = "1024", height = "576")
MapFrame = Frame(root, width = "1024", height = "576")
f4 = Frame(root, width = "1024", height = "576")
root.title("S.T.A.V")
root.geometry(game_resolution)	
root.resizable(False, False)
ActionFrame.pack()

for frame in (ActionFrame, InventoryFrame, MapFrame, f4):
    frame.grid(row=0, column=0, sticky='news')
#INITIALIZATION OF GUI WINDOW 	#####################################

#CLASSES
class Player:
	def __init__(self, health, armour, currentWeapon):
		self.health = health
		self.armour = armour
		self.currentWeapon = currentWeapon

	def takeDamage(self, amount):
		protectionAmount = random.randrange(0, self.armour.protection)
		damageDealt = amount - protectionAmount
		if(damageDealt < 0):
			damageDealt = 0 
		self.health = self.health - damageDealt

	def restoreHealth(self, amount):
		self.health = self.health + amount

	def changeWeapon(self, weapon):
		self.currentWeapon = weapon

class NPC:
	def __init__(self, name):
		self.name = name

class Enemy:
	def __init__(self, name, health, armour, damage, sprite):
		self.name = name
		self.health = health
		self.armour = armour
		self.damage = damage
		self.sprite = sprite

	def takeDamage(self, amount):
		protectionAmount = random.randrange(0, self.armour)
		damageDealt = amount - protectionAmount
		if(damageDealt < 0):
			damageDealt = 0 
		self.health = self.health - damageDealt

		if(self.health <= 0):
			self.die()

	def die(self):
		self.name = ""
		self.health = 0
		self.damage = 0
		self.sprite = noEnemyIMG


class Weapon:
	def __init__(self, name, damage=5, criticalChance=10, accuracy=50):
		self.name = name
		self.damage = damage
		self.criticalChance = criticalChance
		self.accuracy = accuracy

class Armour:
	def __init__(self, name, protection):
		self.name = name
		self.protection = protection

class Item:
	def __init__(self, name, variant="consumable", affector="", amount=5):
		self.name = name
		self.variant = variant
		self.affector = affector
		self.amount = amount
##########################################
script_dir = os.path.dirname(__file__) #<-- absolute directory the script is in
rel_path = "EnemySprites\\GoonTest.png"
abs_file_path = os.path.join(script_dir, rel_path)
basicGoonIMG = ImageTk.PhotoImage(Image.open(abs_file_path))
rel_path = "EnemySprites\\NoEnemy.png"
abs_file_path = os.path.join(script_dir, rel_path)
noEnemyIMG = ImageTk.PhotoImage(Image.open(abs_file_path))


#PRE-BUTTON STUFF
startingArmour = Armour("Cloth armour", 2)
startingWeapon = Weapon("Rusty Handgun", 10, 15, 85)
equippedWeapon = startingWeapon
MainCharacter = Player(100, startingArmour, equippedWeapon)
Adversary = Enemy("", 0, 0, 0, noEnemyIMG)
healthPotion = Item("Health potion", "consumable", "health", 5)

#############################################

#Action Window
ActionLabel = Label(ActionFrame, text='ACTION')
ActionButton1 = Button(ActionFrame, text='Action', command=lambda:loadActionFrame())
MapButton1 = Button(ActionFrame, text='Map', command=lambda:loadMapFrame())
InventoryButton1 = Button(ActionFrame, text='Inventory', command=lambda:loadInventoryFrame())
EnemyDescriptionText = Text(ActionFrame, height = 7, width = 20)
try:
	EnemySprite = Label(ActionFrame, image = Adversary.sprite)
except:
	EnemySprite = Label(ActionFrame, image = noEnemyIMG)
PlayerDescriptionText = Text(ActionFrame, height = 7, width = 25)
FireButton = Button(ActionFrame, text = "FIRE", command = dealDamage) #IF GOON.name == "none" then disable button
mainTextBox = Text(ActionFrame, height = 11, width = 78)

ActionButton1.configure(state = DISABLED)
bugTestButton = Button(ActionFrame, text = "TEST", command=combatSequence)
FireButton.configure(state = DISABLED)


ActionLabel.place(x= 500, y = 5)
ActionButton1.place(x = 884, y = 0)
InventoryButton1.place(x = 929, y = 0)
MapButton1.place(x = 989, y = 0)
EnemyDescriptionText.grid(pady = 20)
EnemySprite.grid(column = 4, row = 1, columnspan = 8, rowspan = 5)
PlayerDescriptionText.grid(column = 14, pady = 20, row = 1, columnspan = 3)
FireButton.grid(column = 15, row = 2)
bugTestButton.grid(column = 14, row = 2)
mainTextBox.grid(column = 0, row = 21, columnspan = 17, rowspan = 16, padx = 5, pady = 8)



#Inventory Window
InventoryLabel = Label(InventoryFrame, text='INVENTORY')
ActionButton2 = Button(InventoryFrame, text='Action', command=lambda:loadActionFrame(Adversary, equippedWeapon))
InventoryButton2 = Button(InventoryFrame, text='Inventory', command=lambda:loadInventoryFrame())
MapButton2 = Button(InventoryFrame, text='Map', command=lambda:loadMapFrame())
InventoryContents = Text(InventoryFrame, height = Inventory.Size(), width = 50)
InventoryButton2.configure(state = DISABLED)

InventoryLabel.place(x = 500, y = 0)
ActionButton2.place(x = 884, y = 0)
InventoryButton2.place(x = 929, y = 0)
MapButton2.place(x = 989, y = 0)
InventoryContents.grid()

#Map Window
MapLabel = Label(MapFrame, text='MAP')
ActionButton3 = Button(MapFrame, text='Action', command=lambda:loadActionFrame(Adversary, equippedWeapon))
InventoryButton3 = Button(MapFrame, text='Inventory', command=lambda:loadInventoryFrame())
MapButton3 = Button(MapFrame, text='Map', command=lambda:loadMapFrame())
MapButton3.configure(state = DISABLED)

MapLabel.place(x = 500, y = 0)
ActionButton3.place(x = 884, y = 0)
InventoryButton3.place(x = 929, y = 0)
MapButton3.place(x = 989, y = 0)

loadActionFrame(Adversary, equippedWeapon)
root.mainloop()

##################################################

Inventory.Create("")
Inventory.AddTab("Weapons")
Inventory.AddTab("Items")
Inventory.AddTab("Armour")
Inventory.AddItem(1, startingWeapon) 
Inventory.AddItem(3, startingArmour)
Inventory.AddItem(2, healthPotion)

#Inventory.Display()


#while Adversary.health > 0:
	#Fighting enemy

#Enemy Killed
