import math

def rollOver(number, minimum, maximum, rounding = True):
	if(number >= minimum and number <= maximum):
		return number
	elif(number > maximum):
		timesOver = number / maximum
		numberRolledOver = maximum * (timesOver - math.floor(timesOver))
		if(rounding == False):
			return numberRolledOver
		if(rounding == True):
			return round(numberRolledOver)
	else:
		timesOver = abs(number / maximum)
		numberRolledOver = maximum * (timesOver - math.floor(timesOver))
		finalNum = maximum - numberRolledOver
		if(rounding == False):
			return finalNum
		if(rounding == True):
			return round(finalNum)


def clamp(number, minimum, maximum):
	if(number < minimum):
		number = minimum
	if(number > maximum):
		number = maximum
	return number


def centerText(width, desiredText):
	#Width = len() of string to center on e.g "i like cats" = 11
	#desiredText = text you want to center
	#return = text with whitespaces already added to center
	text = " " * math.ceil((width - len(desiredText)) / 2) + desiredText
	return text

def lerp(start, end, t):
	# Linear interpolation algorithm
	return start * (1-t) + end * t;

def snap_nearest(initial_value, constraints):
	# Convert to list so that we can easily manipulate values
	constraints = list(constraints)
	if(initial_value in constraints):
		return initial_value;
	# Add value we are trying to find closest value of
	constraints.append(initial_value)
	# Sort initial_value into array
	constraints.sort()
	# Find index of initial value once array is sorted
	index_of_initial_value = constraints.index(initial_value)
	# Test edge cases for quick solutions to the problem
	if(index_of_initial_value == 0):
		return constraints[1]
	elif(index_of_initial_value == len(constraints) - 1):
		return constraints[len(constraints) - 2]
	# If no edge cases are detected, compare the distance of values +- 1 index of the initial value within constraints and return the value with the smallest difference 
	else:
		comparison1 = abs(constraints[index_of_initial_value] - constraints[index_of_initial_value - 1])
		comparison2 = abs(constraints[index_of_initial_value] - constraints[index_of_initial_value + 1])
		if(comparison2 > comparison1):
			return constraints[index_of_initial_value - 1]
		else:
			return constraints[index_of_initial_value + 1]

def get_sign_as_string(number):
	if(number > 0):
		return "+"
	elif(number < 0):
		return "-"
	else:
		return ""
		

def remove_character_from_string(string, start, stop=None):
	
	string = str(string) # Ensure string is a string to avoid errors 

	if(start > len(string) - 1 or stop != None and stop > len(string) - 1):
		return "Index too large";

	string = list(string) # Convert string to array to work with 

	# Remove character from array  
	if(stop != None):
		i = start;
		while(i <= stop):
			string.pop(start)
			i += 1;
	else:
		string.pop(start)

	# Re-assemble string from array
	new_string = "";
	for letter in string:
		new_string += letter; 

	return new_string

def remove_values_from_list(the_list, val):
	return [value for value in the_list if value != val]
