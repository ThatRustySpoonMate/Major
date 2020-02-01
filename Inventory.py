filePath = "InventoryFile2D.txt"


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
		self.type = variant
		self.affector = affector
		self.amount = amount

def GetItemsFromTextFile():
	file = open(filePath, "r")
	contents = file.readline()
	file.close()
	subInventoriesMax = contents.count("|") + 1

	tempinventory = []

	for i in range(subInventoriesMax):
		tempinventory.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

	
	contents = contents.split("|")

	subInvCount = 0
	while(subInvCount < len(contents)):
		wordCount = 0
		letterCount = 0
		word = ""
		while(letterCount < len(contents[subInvCount])):
			letterAtIndex = contents[subInvCount][letterCount]

			if(letterAtIndex != " " and letterAtIndex != ","):
				word = word + letterAtIndex
			if(letterAtIndex == " " and contents[subInvCount][letterCount - 1] != "," and contents[subInvCount][letterCount - 1] != "*" and contents[subInvCount][letterCount - 1] != "|" and contents[subInvCount][letterCount + 1] != "," and contents[subInvCount][letterCount + 1] != "*" and contents[subInvCount][letterCount + 1] != "|"):
				word = word + letterAtIndex
			if(letterAtIndex == ","):
				tempinventory[subInvCount][wordCount] = word
				word = ""
				wordCount = wordCount + 1
			letterCount = letterCount + 1


		subInvCount = subInvCount + 1

	count1 = 0
	for subInvs in tempinventory:
		count2 = 0
		while(count2 < len(subInvs)):
			items = tempinventory[count1][count2]
			if(isinstance(items, int)):
				del tempinventory[count1][count2]
			if(isinstance(items, str)):
				count2 = count2 + 1
				
		count1 = count1 + 1
	return tempinventory


def PushInventoryToTextFile(inventory):
	file = open(filePath, "w")
	InvI = 0
	inventoryToPush = ""
	while InvI < len(inventory):
		SubI = 0
		while SubI < len(inventory[InvI]):

			item = inventory[InvI][SubI]
			item = str(item)
			inventoryToPush = inventoryToPush +  item + ", "
			SubI = SubI + 1

		if(InvI != len(inventory) - 1):
			inventoryToPush = inventoryToPush + "| "

		InvI = InvI + 1

	file.write(inventoryToPush)

	file.close()



#######################################################################################################################################################
#IMPORTANT
#
#Tabs = sub-inventories (Interchangeable)
#
#ENTER INVENTORY IN CREATE FUNCTION AS CSV (comma separated values) with the first value of each sub-inventory being 
#an identifying word related to the sub-inventories contents, enclosed in asterixes "*. Every sub inventory has to be 
#seperated by a Vertical slash "|" and have an identifying word. EVERY item within the sub-inventories MUST have a 
#comma after it, even if it is the last item in a sub-inventory. Additionally, the amount of sub-inventories that you 
#can have is determined in the create function as the number of "|"'s + 1.
#
#Additional- All items and tabs START AT 1. They do not start at 0 like a normal array/list. Doing so will probably result in an error. (Probably)
#
#Functions:
#
#Create(String) - Creates the inventory and tabs given the items you want to start with
#Display(none) - Displays all of the items in the inventory
#DisplayTab(tabNum(int)) - Displays all items from a given tab
#DisplayItem(tabNum(int), itemIndex(int)) - Displays a certain item given the index (1-xxx) from the given tab (1-xxx)
#GetItemsFromTab()
#Size(none) - Returns the number of tabs in the inventory
#SizeTab(tabNum(int)) - Returns the number of items within an inventory tab excluding identifier
#Clear(none) - Clears the entire inventory 
#ClearTab(tabNum(int/string)) - Clears the specified tab given the index of the tab or the name of the identifier
#Sort(none) - Sorts all of the items within every populated tab alphabetically. Note: does not move tabs around
#SortTab(tabNum(int)) - Sorts all of the items within a specified tab alphabetically. 
#Retrieve(tabNum(int), itemNum(int)) - Returns the item name at a givin location in a given tab 
#ItemCount(tabNum(int), item(int/string)) - Returns quantity of specified item given index or name of item within an inventory tab
#ItemExists(tabNum(int), item(string, caseSens(Boolean)) - Returns boolean dependent on if string is in specified inventory tab, can toggle between case-sensitive and not given third argument
#FindItemPosition(tabNum(int), itemNum(string)) - Returns the index of where specified item is within inventory tab
#AddItem(tabNum(int), item(string)) - Appends an item onto end of specified inventory tab
#RemoveItem(tabNum(int), item(int/string), removeAll(Boolean)) - Removes either all (removeAll = true) or only first one ("removeAll = false") of item found within given inventory tab
#ReplaceItem(tabNum(int),itemToReplace(string), itemReplacing(string)) - Deletes specified item within inventory tab and inserts new item into exact same location.
#AddTab(identifier(string)) - creates a whole new inventory tab given the identifier (name) of the tab
#FindTabPosition(tabName(string)) - Returns the index of a specific tab within the whole inventory.
#######################################################################################################################################################

def Create(items):
	file = open(filePath, "w")
	file.write(str(items))
	file.close()

def DisplayItem(tab, itemNum):
	inventory = GetItemsFromTextFile()

	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	if(isinstance(itemNum, str)):
		print("Cannot take string, please enter index of item.")
		return None

	elif(isinstance(itemNum, int)):
		if(itemNum >= 1 and itemNum <= len(inventory)):
			print(inventory[subInv - 1][itemNum])
		else:
			subInv = FindTabIdentifier(subInv)
			print("There is no item at index " + str(itemNum) + " of the " + subInv + " tab.")

def DisplayTab(tab):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab
	if(TabExists(subInv)):
		subInventoryName = inventory[subInv - 1][0]
		subInventoryName = subInventoryName.strip("*")
		print(subInventoryName, end = " ", flush = True)
		print(inventory[subInv - 1][1:])
	else:
		print("Unable to find tab at index " + str(subInv) + " to display.")


def Display():
	inventory = GetItemsFromTextFile()
	subInvs = 0
	if(len(inventory[0]) != 0):
		while subInvs < len(inventory):
			subInventoryName = inventory[subInvs][0]
			subInventoryName = subInventoryName.strip("*")
			print(subInventoryName, end = " ", flush = True)
			item = inventory[subInvs][1:]
			print(item)

			subInvs = subInvs + 1
	else:
		print("Inventory is empty.")


def RetrieveItemsFromTab(tab):
	inventory = GetItemsFromTextFile()
	itemsToReturn = []
	if(tab == 1):
		itemsToReturn.append(inventory[tab - 1][0])
		numberOfItems = int((len(inventory[tab - 1]) - 1) / 4)
		iterator = 0
		for i in range(0, numberOfItems):
			iterations = i
			if(iterator > 0):
				iterations *= 4
			itemsToReturn.append(Weapon(inventory[tab - 1][iterations + 1], inventory[tab - 1][iterations + 2], inventory[tab - 1][iterations + 3], inventory[tab - 1][iterations + 4]))
			iterator += 1
	if(tab == 3):
		itemsToReturn.append(inventory[tab - 1][0])
		numberOfItems = int((len(inventory[tab - 1]) - 1) / 2)
		iterator = 0
		for i in range(0, numberOfItems):
			iterations = i
			if(iterator > 0):
				iterations *= 2
			itemsToReturn.append(Armour(inventory[tab - 1][iterations + 1], inventory[tab - 1][iterations + 2]))
			iterator += 1
	if(tab == 2):
		itemsToReturn.append(inventory[tab - 1][0])
		numberOfItems = int((len(inventory[tab - 1]) - 1) / 4)
		iterator = 0
		for i in range(0, numberOfItems):
			iterations = i
			if(iterator > 0):
				iterations *= 4
			itemsToReturn.append(Item(inventory[tab - 1][iterations + 1], inventory[tab - 1][iterations + 2], inventory[tab - 1][iterations + 3], inventory[tab - 1][iterations + 4]))
			iterator += 1


	return itemsToReturn


def Size():
	inventory = GetItemsFromTextFile()
	inventoryLength = len(inventory)
	return inventoryLength

def SizeTab(tab):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	if(TabExists(tab)):
		inventoryLength = len(inventory[subInv - 1])
		return inventoryLength - 1
	else:
		print("Unable to tab at index " + str(subInv) + " to gather the size of.")

def SortTab(tab):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab
	if(TabExists(tab)):
		inventory[subInv - 1].sort()
		PushInventoryToTextFile(inventory)
	else:
		print("Unable to sort tab at index " + str(subInv))


def Sort():
	inventory = GetItemsFromTextFile()
	i = 0
	while i < len(inventory):
		inventory[i].sort(reverse = False)
		i = i + 1

	PushInventoryToTextFile(inventory)

def Clear():
	file = open(filePath, "w")
	file.write("")
	file.close()

def ClearTab(subInv):
	inventory = GetItemsFromTextFile()
	if(isinstance(subInv, int)):
		if(TabExists(subInv)):
			inventory[subInv - 1] = inventory[subInv-1][:1]
		else:
			print("Unable to clear tab at index " + str(subInv))
	if(isinstance(subInv, str)):
		if(TabExists(subInv)):
			tabToClear = FindTabPosition(subInv) - 1
			if(tabToClear != None):
				inventory[tabToClear] = inventory[tabToClear][:1]
			else:
				print("Unable to clear tab.")
		else:
			print("Unable to clear tab '" + subInv + "'")
	

	PushInventoryToTextFile(inventory)

def Retrieve(tab, index):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	if(isinstance(index, int)): #Checks if looking for an integer
		if(ItemExists(tab, index, False)):
			desiredItem = inventory[subInv - 1][index]
			return desiredItem
	else:
		print("Cannot take index of item as a string. Recieved '" + index + "'")

def ItemCount(tab, item):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	instancesOfItem = 0
	if(isinstance(item, str)):
		for items in inventory[subInv - 1]:
			items = items.lower()
			item = item.lower()
			if(item == items):
				instancesOfItem = instancesOfItem + 1

	if(isinstance(item, int)):
		itemAtPosition = Retrieve(subInv, item)

		for items in inventory[subInv - 1]:
			items = str(items)
			items = items.lower()
			itemAtPosition = itemAtPosition.lower()
			if(itemAtPosition == items):
				instancesOfItem = instancesOfItem + 1

	return instancesOfItem


def ItemExists(tab, itemStr, caseSens):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	if(TabExists(subInv)):
		if(isinstance(itemStr, str)): #Checks if looking for a string
			for items in inventory[subInv - 1]:
				if(caseSens == False):
					items = items.lower()
					itemStr = itemStr.lower()
				if(itemStr == items):
					return True
		if(isinstance(itemStr, int)):
			if(itemStr < len(inventory[subInv - 1]) and itemStr >= 1):
				return True

	return False;


def FindItemPosition(tab, item):
	inventory = GetItemsFromTextFile()

	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	position = 0
	positions = ["*" + item + " cannot be found in specified inventory tab.*"]
	for items in inventory[subInv - 1]:
		items = items.lower()
		item = item.lower()
		if(item == items):
			if(len(positions[0]) > 39):
				positions = [" "]
			positions.append(position)
		position = position + 1

	if(positions[0][0] == "*"):
		return positions
	else:
		return positions[1:]

def AddItem(tab, item):
	inventory = GetItemsFromTextFile()
	invLength = int(len(inventory[0]))

	if(invLength > 0):
		if(isinstance(tab, str)):
			subInv = FindTabPosition(tab)
			if(subInv == None):
				return None
		else:
			subInv = tab

		if(subInv - 1 < len(inventory) and subInv > 0):
			if(tab == 1):
				inventory[subInv - 1].append(item.name)
				inventory[subInv - 1].append(item.damage)
				inventory[subInv - 1].append(item.criticalChance)
				inventory[subInv - 1].append(item.accuracy)
			if(tab == 3):
				inventory[subInv - 1].append(item.name)
				inventory[subInv - 1].append(item.protection)
			if(tab == 2):
				inventory[subInv - 1].append(item.name)
				inventory[subInv - 1].append(item.variant)
				inventory[subInv - 1].append(item.affector)
				inventory[subInv - 1].append(item.amount)

		else:
			print("Cannot find specified inventory tab to add '" + item + "' to.")
			return
	PushInventoryToTextFile(inventory)


def RemoveItem(tab, item, removeAll):
	inventory = GetItemsFromTextFile()
	OneTimeRun = removeAll
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
	else:
		subInv = tab
	if(isinstance(item, int)): #Checks if looking for an integer
		if(item >= 1 and item <= len(inventory[tab - 1]) - 1):
			if(removeAll == False):
				inventory[subInv - 1].pop(item)
			else:
				if(ItemExists(subInv, item, False)):
					item = Retrieve(subInv, item)
	if(isinstance(item, str)): #Checks if looking for a string
		if(ItemExists(subInv, item, False)):
			item = item.lower()
			positionOfItem = FindItemPosition(subInv, item)
			i = 0
			
			while i < len(positionOfItem) and removeAll == True:
				itemAtPosition = Retrieve(subInv, positionOfItem[i])
				inventory[subInv - 1].remove(itemAtPosition)
				i = i + 1

			while i < len(positionOfItem) and removeAll == False and OneTimeRun == False:
				itemAtPosition = Retrieve(subInv, positionOfItem[i])
				inventory[subInv - 1].remove(itemAtPosition)
				i = i + 1
				OneTimeRun = True
		else:
			if(isinstance(tab, str)):
				print("Unable to locate item '" + item + "' in '" + tab + "' tab.")
			else:
				if(TabExists(tab)):
					print("Unable to locate item '" + item + "' in '" + FindTabIdentifier(tab) + "' tab")
				else:
					print("There is no tab at index number " + str(tab))

	PushInventoryToTextFile(inventory)

def ReplaceItem(tab, itemToReplace, item):
	inventory = GetItemsFromTextFile()
	if(isinstance(tab, str)):
		subInv = FindTabPosition(tab)
		if(subInv == None):
			return None
	else:
		subInv = tab

	if(isinstance(itemToReplace, int)): #Checks if looking for an integer
		inventory[subInv - 1].pop(itemToReplace)
		inventory[subInv - 1].insert(itemToReplace, item)

	if(isinstance(itemToReplace, str)): #Checks if looking for an String
		if(ItemExists(subInv, itemToReplace, False)):
			positionOfItemToReplace = FindItemPosition(subInv, itemToReplace)
			inventory[subInv - 1].pop(positionOfItemToReplace[0])
			inventory[subInv - 1].insert(positionOfItemToReplace[0], item)
		else:
			subInventoryName = inventory[subInv - 1][0]
			subInventoryName = subInventoryName.strip("*")
			print('Could not find "' + itemToReplace + '" in ' + subInventoryName + '.')
	PushInventoryToTextFile(inventory)

def AddTab(identifier):
	inventory = GetItemsFromTextFile()
	if(isinstance(identifier, str)):
		identifierString = "*" + identifier + "*"
		extraTab = [identifierString]
		inventory.append(extraTab)
		PushInventoryToTextFile(inventory)
		file = open(filePath, "r")
		contents = file.readline()
		file.close()
		if(contents[0] == "|"):
			contents = contents[1:]
			file = open(filePath, "w")
			file.write(contents)
			file.close()
	else:
		print("Adding a tab requires a string. Instead, recieved the number " + str(identifier))

def RemoveTab(tab):
	inventory = GetItemsFromTextFile()

	if(isinstance(tab, int)):
		if(TabExists(tab - 1)):
			inventory.pop(tab - 1)
		else:
			print("Unable to remove tab number '" + str(tab) + "'")

	if(isinstance(tab, str)):
		if(TabExists(tab)):
			tabToRemove = FindTabPosition(tab) - 1
			inventory.pop(tabToRemove)
		else:
			print("Unable to remove tab '" + tab + "'")


	PushInventoryToTextFile(inventory)

def FindTabIdentifier(tabNum):
	inventory = GetItemsFromTextFile()
	
	if(isinstance(tabNum, int)):
		if(tabNum <= len(inventory) and tabNum >= 1):
			tabIdentifier = inventory[tabNum - 1][0]
			tabIdentifier = tabIdentifier.strip("*")
			return tabIdentifier
		if (tabNum > len(inventory)):
			print("The specified tab index is too large, cannot find tab number " + str(tabNum))
			return None
		else:
			print("The specified tab index is too small, cannot find tab number " + str(tabNum))
			return None
	if(isinstance(tabNum, str)):
		print("Cannot take string as argument.")
		return None

def FindTabPosition(tabName):
	inventory = GetItemsFromTextFile()
	if(isinstance(tabName, str)):
		tabName = tabName.lower()
		count = 0

		for tab in inventory:
			tabIdentifier = tab[0]
			tabIdentifier = tabIdentifier.strip("*")
			tabIdentifier = tabIdentifier.lower()
			if(tabName == tabIdentifier):
				return count + 1
			count = count + 1

		print("Unable to find tab '" + tabName + "'")
		return None

	else:
		print("Cannot take an integer as argument.")
		return None

def TabExists(tab):
	inventory = GetItemsFromTextFile()

	if(isinstance(tab, str)):
		tab = tab.lower()
		for tabs in inventory:
			tabIdentifier = tabs[0]
			tabIdentifier = tabIdentifier.strip("*")
			tabIdentifier = tabIdentifier.lower()

			if(tabIdentifier == tab):
				return True

		return False

	if(isinstance(tab, int)):
		if(tab >= 1 and tab <= len(inventory)):
			return True

		return False

