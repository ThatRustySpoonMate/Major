import random

def get_adjective(amount):
	word = ""

	#List of adjectives
	adjectivesStart = ["Amazing", "Bloody", "Seductive", "Courageous", "Wistful", "Waggish", "Voracious", "Vivacious", "Vacuous", "Truculent", "Arduous", "Placid", "Loutish", "Insidious", "Heady", "Erratic", "Direful", "Decorous", "Abhorrent", "Exquisite", "Mesmerising", "Tasteful", "Dangerous", "Absurd", "Surprising", "Curious", "Rediculous", "Superb", "Menacing", "Destructive", "Hasty", "Scary", "Weighty", "Weightless", "Heavy", "Clumsy", "Superior", "Beautiful", "Gorgeous", "Awkward", "Lethal", "Legendary", "Crazy", "Stupid", "Pearlescent", "Lustrous", "Extraordinary", "Hopeless", "Woeful", "Deep", "Monstrous", "Bountiful", "Atrocious", "Powerful", "Unique", "Mild", "Wreckless", "Disgusting", "Ludicrous"]
	adjectivesFinal = ["Amazing", "Genuine", "High-quality", "Low-quality", "Top-tier", "Holy", "God-Tier", "Sh*t", "Swift", "Wistful", "Sinful", "Innocent", "Petite", "Hairy", "Hard", "Firm", "Sweet", "Bullsh*t", "B*tchass", "Silky", "Smooth", "Kinky", "Effervescent", "Efficient", "Waggish", "Voracious", "Vivacious", "Vacuous", "Truculent", "Torpid", "Arduous", "Tawdry", "Squalid", "Recondite", "Quixotic", "Plucky", "Placid", "Piquant", "Picayune", "Overwrought", "Ossified", "Obsequious", "Nondescript", "Macarbe", "Loutish", "Languid", "Irate", "Incandescent", "Heady", "Furtive", "Elated", "Erratic", "Efficacious", "Direful", "Didatic", "Debonair", "Dapper", "Craven", "Brash", "Bawdy", "Acrid", "Exquisite", "Mesmerising", "Tasteful", "Transparent", "Immaculate", "Dense", "Flexible", "Superb", "Strong", "Cute", "Long", "Wide", "Pungent", "Fat", "Dangerous", "Shiny", "Cool", "Sharp", "Menacing", "Pointy", "Destructive", "Loud", "Special", "Speedy", "Hasty", "Blunt", "Huge", "Giant", "Scary", "Weighty", "Mad", "Heavy", "Light", "Clumsy", "Superior", "Beautiful", "Gorgeous", "Awkward", "Lethal", "Deadly", "Fully-sick", "Legendary", "Crazy", "Stupid", "Mad", "Turbocharged", "Pearlescent",  "Lustrous", "Worn", "Slimy", "Atrocious", "Powerful", "Dull", "Marred", "Slick", "Ludicrous", "Extraordinary", "Wet", "Dry", "Boring", "Rusty", "Polished", "Tarnished", "Hopeless", "Woeful", "Rough", "Burred", "Impaired", "Monstrous", "Honoured"] 

	if(amount == 1):
		decider = random.randrange(1,3)
		if(decider == 1):
			word = adjectivesStart[random.randrange(0, len(adjectivesStart))]
		else:
			word = adjectivesFinal[random.randrange(0, len(adjectivesFinal))]
	if(amount == 2):
		wordStart = adjectivesStart[random.randrange(0, len(adjectivesStart))]
		wordStart = str(wordStart)
		wordFinal = wordStart
		while (wordFinal == wordStart):
			wordFinal = adjectivesFinal[random.randrange(0, len(adjectivesFinal))]
		if(wordStart[len(wordStart) - 1] == "y"): #If starting word (Starting adjective word) ends with "y" change it to "ily", otherwise change it to "ly" 
			wordStart = wordStart[:len(wordStart) - 1]
			wordStart = wordStart + "ily"
		else:
			wordStart = wordStart + "ly"

		word = wordStart + " " + wordFinal

	if(amount == 3):
		wordStart = adjectivesStart[random.randrange(0, len(adjectivesStart))]
		wordStart = str(wordStart)
		if(wordStart[len(wordStart) - 1] == "y"): #If starting word (Starting adjective word) ends with "y" change it to "ily", otherwise change it to "ly" 
			wordStart = wordStart[:len(wordStart) - 1]
			wordStart = wordStart + "ily"
		else:
			wordStart = wordStart + "ly"

		wordMiddle = wordStart
		while(wordMiddle == wordStart):
			wordMiddle= adjectivesFinal[random.randrange(0, len(adjectivesFinal))]
		
		wordFinal = adjectivesFinal[random.randrange(0, len(adjectivesFinal))]
		while(wordFinal == wordStart or wordFinal == wordMiddle):
			wordFinal = adjectivesFinal[random.randrange(0, len(adjectivesFinal))]
		word = wordStart + " " + wordMiddle + " but " + wordFinal 


	return word


def get_name(gender, firstName, middleName, lastName):
	name = "a"
	firstNameWord = ""
	middleNameWord = ""
	lastNameWord = ""

	#Populated array male names
	firstNamesMale = ["Liam", "Alton", "Drake", "Brenden", "Brandon", "Hector", "Dean", "Cicero", "Alton", "Omar", "Mahlon", "Reginald", "Spencer", "Roland", "Jeremiah", "Tony", "Vincent", "Barney", "Cecil", "Marcus", "Gustave", "Gordon", "Jerome", "Lonnie", "Austin", "Sherman", "Joshua", "Andy", "Hubert", "Scott", "Irving", "Enoch", "Clayton", "Solomon", "Russell", "Columbus", "Stanley", "Elias", "Jeff", "Marvin", "Timothy", "Nicholas", "Augustus", "Marshall", "Clinton", "Virgil", "Abraham", "Wilbur", "Jose", "Irvin", "Willard", "Simon", "Otis", "Hiram", "Wallace", "Reuben", "Felix", "Cornelius", "Maurice", "Percy", "Mike", "Jake", "Silas", "Nelson", "Gus", "Victor", "Gilbert", "Norman", "Alvin", "Aaron", "Melvin", "Jay", "Mack", "Lloyd", "Winfield", "Lester", "Everett", "Moses", "Levi", "Matthew", "Harold", "Nathan", "Theon", "Leon", "Franklin", "Alonzo", "Wesley", "Leroy", "Dennis", "Amos", "Dave", "Anthony", "Edmund", "Calvin", "Jerry", "Dan", "Bernard", "Dugald", "Sidney", "Ray", "Julius", "Leo", "Alex", "Milton", "Darren", "Warren", "Rufus", "Raymond", "Chester", "Stephen", "Archie", "Allen", "Philip", "Marion", "Horace", "Leonard", "Homer", "Floyd", "August", "Alexander", "Clyde", "Hugh", "Theodore", "Guy", "Patrick", "Ira", "Lawrence", "Luther", "Otto", "Brayden", "Isaac", "Edgar", "Jean", "Paul", "Charley", "Ben", "Edwin", "Claude", "Ed", "Ralph", "Eugene", "Earl", "Harvey", "Francis", "Jim", "Jordan", "Herman", "Bert", "Michael", "Martin", "Tim", "Todd", "Howard", "Leigh", "Lee", "Carl", "Elmer", "Tom", "Herbert", "Roy", "Sam", "Alfred", "Willie", "Frederick", "Peter", "Lewis", "Oscar", "Jesse", "Will", "Ernest", "Daniel", "Andrew", "Richard", "Clarence", "Charlie", "Joe", "Louis", "David", "Albert", "Fred", "Arthur", "Walter", "Harry", "Edward", "Robert", "Henry", "Thomas", "Joseph", "Frank", "George", "Charles" ,"Logan", "Mason", "Lucas", "Aiden", "Elijah", "Tobias", "Rhys", "Benjamin", "Jamie", "Oliver", "James", "William", "Noah", "Christopher", "John", "Samuel", "Ethan", "Jack", "Jacob", "Martin"]
	middleNamesMale = ["Hartley", "Malachi", "Sullivan", "Fernando", "Nicolas", "Isaiah", "Ricardo", "Oliver", "Matteo", "Sheridan", "Julian", "Damien", "Orlando", "Varian", "Apollo", "Emerson", "Gregory", "Garrison", "Xavier", "Avery", "Rory", "Myron", "Tyson", "Tanner", "Trevor", "Hyrum", "Lydon", "Kingston", "Dezi", "Oren", "Porter", "Nevin", "Murphy", "Francis", "Juan", "Doran", "Tristan", "Warren", "Eli", "Jared", "Gavin", "Denver", "Justice", "Oscar", "Kai", "Ryder", "Sutton", "Cody", "Caleb", "Felix", "Levi", "Isaac", "Riley", "Aaron", "Lawrence", "Joseph", "Quintin", "Preston", "Byron", "Randall", "Louis", "Edward", "Vincent", "Thomas", "Brendon", "Dante", "Noel", "Justin", "Michael", "Damon", "Bailey", "Conrad", "Arthur", "Aiden", "Drake", "Glenn", "Jax", "Shane", "Troy", "Will", "Zane", "Neil", "Finn", "Heath", "Ray", "Drew", "Clark", "Dash", "Brock", "Coy", "Lane", "Dex", "Brandt", "Bram", "Trey", "Claude", "Chase", "Luke", "Brett", "Lee", "Kent", "Rhett", "Jude", "George", "Charles", "James", "Hugh", "Grant", "Dean", "Blake", "Ace", "Beck", "Abe", "Arthur", "Jay", "Oliver", "Matthew", "Henry", "Daniel", "Christopher", "Anthony", "Edward", "Jack", "Joseph", "Peter", "Andrew", "David", "Michael", "Robert", "Alexander", "Thomas", "William", "John", "James", "Arnold"]
	#Populated array female names
	firstNamesFemale = ["Olivia", "Abigail", "Jessica", "Trea", "Sigourney", "Reina", "Odilla", "Merry", "Matilda", "Margery", "Heloise", "Cecily", "Beverly", "Beatrice", "Emilia", "Tayla", "Emily", "Jane", "Hannah", "Viola", "Ruth", "Rebecca", "Alana", "Belle", "Amanda", "Lottie", "Lulu", "Eliza", "Georgia", "Addie", "Alma", "Mollie", "Susan", "Kate", "Elsie", "Lydia", "Katie", "Caroline", "Harriet", "Etta", "Mae", "Maud", "Susie", "Flora", "Lizzie", "Della", "Nettie", "Sallie", "Effie", "Nancy", "Ellen", "Blanche", "Mamie", "May", "Nora", "Marie", "Agnes", "Katherine", "Rosa", "Dora", "Anna", "Josephine", "Frannie", "Daisy", "Pearl", "Maggie", "Edna", "Lucy", "Lena", "Frances", "Eva", "Myrtle", "Lula", "Ethel", "Louise", "Jordyn", "Jessie", "Helen", "Lillie", "Ada", "Lillian", "Catherine", "Denise", "Rose", "Mattie", "Edith", "Hattie", "Julia", "Gertrude", "Jennie", "Bessie", "Maude", "Carrie", "Grace", "Nellie", "Laura", "Martha", "Cora", "Florence", "Ella", "Clara", "Annie", "Sarah", "Bertha", "Alice", "Ida", "Margaret", "Elizabeth", "Minnie", "Mary", "Stella", "Charlie", "Melanie", "Ava", "Evelyn", "Harper", "Amelia", "Mia", "Charlotte", "Isabella", "Heatha", "Sophia", "Emma"]
	middleNamesFemale = ["Elise", "Coralie", "Verena", "Imogen", "Naomi", "Gillian", "Abigail", "Rayleen", "Olive", "Nadeen", "Meaghan", "Hollyn", "Erin", "Ellen", "Debree", "Caren", "Candice", "Bernice", "Aryn", "Anise", "Alice", "Adele", "Taye", "Raine", "Merle", "Love", "June", "Brooke", "Blayne", "Blanche", "Blair", "Sue", "Lynn", "Krystan", "Kathryn", "Jae", "Jacklyn", "Aryn", "Fern", "Dawn", "Bree", "Hope", "Charlotte", "Claire", "Belle", "Lee", "Paige", "Ruby", "Jean", "Lily", "Anne", "Kate", "Marie", "Elizabeth", "May", "Jade", "Louise", "Jane", "Grace", "Rose", "Ruth", "Mary"]
	#Populated array last name unisex as last names don't change based on gender
	lastNames = ["Willmington", "Marks", "Corgen", "Stark", "Barnes", "Delores", "Eleanore", "Cotter", "Mooney", "Brice", "Pierce", "Close", "Boyd", "Queen", "Maybelle", "Sterling", "Melville", "Hamilton", "Orwell", "Stewart", "Lorenzo", "Vernon", "Holmes", "Kunic", "Caesar", "Yule", "Wylie", "Wild", "Threston", "Soule", "Seely", "Pritchett", "Passelewe", "Packard", "Orrels", "Lapsley", "Jourdemayne", "Immers", "Holloway", "Giel", "Frostenden", "Emor", "Elford", "Courtier", "Callow", "Bowe", "Baldrick", "Snow", "Wood", "Webb", "Foreman", "Gregory", "Hughes", "Nash", "Godfrey", "Baker", "Hall", "Perez", "Walker", "Robinson", "Lewis", "Clark", "Lopez", "White", "Jackson", "Martin", "Moore", "Taylor", "Anderson", "Martinez", "Wilson", "Davis", "Brown", "Williams", "Garcia", "Johnson", "Miller", "Smith", "Donks", "Roger", "Musket", "O-Donnel", "Willis", "Sun", "Nguyen", "Philp", "Sweeny", "Keller", "Howard", "Beckhaus"]

	#SETTING EACH PART OF NAME RANDOMLY
	if(gender == "male"):

		if (firstName == True):
			firstNameWord = firstNamesMale[random.randrange(0 , len(firstNamesMale))]

		if (middleName == True):
			middleNameWord = middleNamesMale[random.randrange(0 , len(middleNamesMale))]
			while (middleNameWord == firstNameWord):
				middleNameWord = middleNamesMale[random.randrange(0 , len(middleNamesMale))]

		if (lastName == True):
			lastNameWord = lastNames[random.randrange(0 , len(lastNames))]

	if(gender == "female"):

		if (firstName == True):
			firstNameWord = firstNamesFemale[random.randrange(0 , len(firstNamesFemale))]

		if (middleName == True):
			middleNameWord = middleNamesFemale[random.randrange(0 , len(middleNamesFemale))]
			while (middleNameWord == firstNameWord):
				middleNameWord = middleNamesFemale[random.randrange(0 , len(middleNamesFemale))]

		if (lastName == True):
			lastNameWord = lastNames[random.randrange(0 , len(lastNames))]

	#PUTTING NAME TOGETHER 
	if(firstName == True):
		name = "" + firstNameWord
	if(middleName == True):
		if(name[0] == "a"):
			name = "" + middleNameWord
		else:
			name = name + " " + middleNameWord
	if(lastName == True):
		if(name[0] == "a"):
			name = "" + lastNameWord
		else:
			name = name + " " + lastNameWord

	return name

def get_weapon_name(weapon_type, tier):

	ranged_weapons_name = [ 
						  ["Make-shift Revolver", "Single-Barrel Shotgun", "Pistol", "Boomerang"], 																						# First tier options     # Expand this
	 					  ["Double-Barrel Shotgun", "Sub-Machine Gun", "Rifle", "Revolver", "Hand-cannon"],																				# Second tier options    # Expand this
	 					  ["Rocket Launcher", "Gatling Gun", "Rortary Cannon", "Rail Gun", "Coil Gun", "Particle-beam gun", "Bolt Action Rifle", "Combat Shotgun"]						# Third tier options     # Expand this
	 					  ]

	melee_weapons_name = [
						 ["Shiv", "Crow-bar", "Dagger", "Baseball Bat", "Rolling-pin", "Bread Board", "Lead Pipe", "Pipe Wrench", "Hammer", "Quater-Staff"], 							# First tier options     # Expand this
						 ["Machete", "Axe", "Switchblade", "Spiked-knuckles", "Spiked Mace", "Club", "Flail", "Sickle", "Spear"], 														# Second tier options    # Expand this
						 ["Greatsword", "War-axe", "Proto-saber", "Lance", "Sledge-hammer"]   																							# Third tier options     # Expand this
						 ]

	

	if(weapon_type == "melee"):
		return get_adjective(1) + " " + random.choice(melee_weapons_name[tier - 1])
	else:
		return get_adjective(1) + " " + random.choice(ranged_weapons_name[tier - 1])

def get_armour_name(armour_description, tier):
	#Use get adjective to describe armour

	armour_description = armour_description.replace("_"," ").capitalize()
	adjectives = random.randrange(0,tier+1)
	armour_descriptor = get_adjective(adjectives)
	if(adjectives != 0):
		armour_name = armour_descriptor + " " + armour_description;
	else:
		armour_name = armour_description

	return armour_name


