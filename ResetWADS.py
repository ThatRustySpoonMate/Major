import os, FileInterface, time;
print("Restoring WADS...")
script_drectory = os.path.dirname(__file__);

# When WADS are complete, copy and paste the printed output of each data (UI_data, Enemies_data etc...) and save as variable 

UI_data = """# These files are made to be editable so that you can easily mod how you like :)
# Simply replace any of the following locations (beggining with a '\', do not change the names above the locations) with an at symbol ("@"), followed by the absolute location of the desired image
baguette_icon
\\Sprites\\UI\\baguette_icon.png
gun_icon
\\Sprites\\UI\\gun_icon.png
sword_icon
\\Sprites\\UI\\sword_icon.png
weight_icon
\\Sprites\\UI\\weight_icon.png""".split('\n')


Enemies_data = """# These files are made to be editable so that you can easily mod the game :) 
# Simply replace any of the following locations (beggining with a '\', do not change the names above the locations) with an 'at' symbol (@), followed by the absolute path of the desired image
Pirate
\\Sprites\\Enemies\\Pirate.png
Automaton
\\Sprites\\Enemies\\Automaton.png
Diesel-Mechanic
\\Sprites\\Enemies\\Diesel-Mechanic.png
Dwarf
\\Sprites\\Enemies\\Dwarf.png
Clock-work Mage
\\Sprites\\Enemies\\Clock-work Mage.png
Baguettist
\\Sprites\\Enemies\\Baguettist.png
Ex-marine
\\Sprites\\Enemies\\Ex-marine.png
High-brow
\\Sprites\\Enemies\\High-brow.png
NoEnemy
\\Sprites\\Enemies\\NoEnemy.png
Nuclear-waste Farmer
\\Sprites\\Enemies\\Nuclear-waste Farmer.png
French Soldier
\\Sprites\\Enemies\\French Soldier.png
Irradiated
\\Sprites\\Enemies\\Irradiated.png
Monocle bandit
\\Sprites\\Enemies\\Monocle bandit.png
Outlaw
\\Sprites\\Enemies\\Outlaw.png
Rich
\\Sprites\\Enemies\\Rich.png
Super Mutant
\\Sprites\\Enemies\\Super Mutant.png""".split('\n')

Locations_data = """# These files are made to be editable so that you can easily mod how you like :) 
# Simply replace any of the following locations (locations start with a '\', do not change the names above the locations) with an at symbol ("@"), followed by the absolute location of the desired image
Dealer
\\Sprites\\Locations\\Two_up_dealer_dark.png
Location_Start
\\Sprites\\Locations\\Location_Start.png
Location01
\\Sprites\\Locations\\Location01.png
Location02
\\Sprites\\Locations\\Location02.png
Location03
\\Sprites\\Locations\\Location03.png
Location04
\\Sprites\\Locations\\Location04.png
Location05
\\Sprites\\Locations\\Location05.png
Location06
\\Sprites\\Locations\\Location06.png
Location07
\\Sprites\\Locations\\Location07.png
Location08
\\Sprites\\Locations\\Location08.png
Location09
\\Sprites\\Locations\\Location09.png
Location10
\\Sprites\\Locations\\Location10.png
Location11
\\Sprites\\Locations\\Location11.png
Location12
\\Sprites\\Locations\\Location12.png
Location13
\\Sprites\\Locations\\Location13.png
Location14
\\Sprites\\Locations\\Location14.png
Location15
\\Sprites\\Locations\\Location15.png
Location16
\\Sprites\\Locations\\Location16.png
Location17
\\Sprites\\Locations\\Location17.png
Location18
\\Sprites\\Locations\\Location18.png
Location19
\\Sprites\\Locations\\Location19.png
Location20
\\Sprites\\Locations\\Location20.png
Location21
\\Sprites\\Locations\\Location21.png
Location22
\\Sprites\\Locations\\Location22.png
Location23
\\Sprites\\Locations\\Location23.png
Location24
\\Sprites\\Locations\\Location24.png
Location25
\\Sprites\\Locations\\Location25.png
Location26
\\Sprites\\Locations\\Location26.png
Location27
\\Sprites\\Locations\\Location27.png
Location28
\\Sprites\\Locations\\Location28.png
Location_Loot
\\Sprites\\Locations\\Location_Loot.png
Town_End
\\Sprites\\Towns\\Town_End.png
Town01
\\Sprites\\Towns\\Town01.png
Town02
\\Sprites\\Towns\\Town02.png
Town03
\\Sprites\\Towns\\Town03.png
Town04
\\Sprites\\Towns\\Town04.png
Town05
\\Sprites\\Towns\\Town05.png
Town06
\\Sprites\\Towns\\Town06.png
Town07
\\Sprites\\Towns\\Town07.png
Town08
\\Sprites\\Towns\\Town08.png
Town09
\\Sprites\\Towns\\Town09.png""".split('\n')


try:
    FileInterface.clear_contents(script_drectory + "\\Image_UI.wad")
    new_line = False;
    for line in UI_data:
        FileInterface.append_data(script_drectory + "\\Image_UI.wad", line, new_line)
        new_line = True;
    print("1/3 Restored...")


    FileInterface.clear_contents(script_drectory + "\\Image_Enemies.wad")
    new_line = False;
    for line in Enemies_data:
        FileInterface.append_data(script_drectory + "\\Image_Enemies.wad", line, new_line)
        new_line = True;
    print("2/3 Restored...")

    FileInterface.clear_contents(script_drectory + "\\Image_Locations.wad")
    new_line = False;
    for line in Locations_data:
        FileInterface.append_data(script_drectory + "\\Image_Locations.wad", line, new_line)
        new_line = True;
    print("3/3 Restored...")

    print("WADS successfully restored")
    time.sleep(3)
    quit()
except Exception as reason:
    print("WADS could not be successfully restored, reason:\n" + str(reason))
    
