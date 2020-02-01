import math

def rollOver(number, minimum, maximum, rounding):
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

