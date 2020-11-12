import os, FileInterface

def initialise_wads():
    print("Intialising WADS")
    script_directory = os.path.dirname(__file__) # Get the absolute directory this script is in

    # Simple hack to store a single backslash for directories as a single backslash in a string in python is used to create special character sequence and as such, will not work.
    single_backslash = "\\"
    single_backslash = single_backslash[0]


    ui_wad_path = script_directory + "\\Image_UI.wad" 
    enemies_wad_path = script_directory + "\\Image_Enemies.wad" 
    locations_wad_path = script_directory + "\\Image_locations.wad" 

    absolute_ui_wad_path = script_directory + "\\GameData\\Absolute_UI.wad"
    absolute_enemies_wad_path = script_directory + "\\GameData\\Absolute_Enemies.wad"
    absolute_location_wad_path = script_directory + "\\GameData\\Absolute_Locations.wad"


    # Open absolute wad paths
    abs_ui_wad_file = open(absolute_ui_wad_path, "r+")
    abs_enemies_wad_file = open(absolute_enemies_wad_path, "r+")
    abs_locations_wad_file = open(absolute_location_wad_path, "r+")

    # Flush absolute wad paths
    abs_ui_wad_file.truncate(0)
    abs_enemies_wad_file.truncate(0)
    abs_locations_wad_file.truncate(0)

    FileInterface.append_data(absolute_ui_wad_path, "#DO NOT EDIT!", False)
    FileInterface.append_data(absolute_enemies_wad_path, "#DO NOT EDIT!", False)
    FileInterface.append_data(absolute_location_wad_path, "#DO NOT EDIT!", False)

    # NEED FALLBACK IMAGE TO DISPLAY WHEN IMAGE HASNT BEEN LOADED CORRECTLY 
    # Loop through ui wad file, update directories and decide which ones have been modded and copy across to absolute wad file  
    with open(ui_wad_path, "r") as ui_wad_file:
        current_line_index = 0;
        for line in ui_wad_file:
            line = line.replace("\n", "")
            if(line != "" and line[0] == single_backslash): # Local file that we need to check the file path of to respective ensure integrity

                # Get the data at the current line
                data_at_current_line = FileInterface.line_from_file(ui_wad_path, current_line_index) 
                data_at_current_line = data_at_current_line[0]
                # Get the desired path to of the file 
                desired_path = script_directory + data_at_current_line

                FileInterface.append_data(absolute_ui_wad_path, desired_path) # Copy to absolute file path
                

            elif(line[0] != "#"): 
                # Is a user modified directory
                FileInterface.append_data(absolute_ui_wad_path, line.replace("\n", "").replace("@", "")) # Copy to absolute file path 
                
            current_line_index += 1;
    print("1/3 complete...")

    # Loop through enemies wad file, update directories and decide which ones have been modded and copy across to respective absolute wad file  
    with open(enemies_wad_path, "r") as enemies_wad_file: 
        current_line_index = 0;
        for line in enemies_wad_file:
            line = line.replace("\n", "")
            if(line != "" and line[0] == single_backslash): # Local file that we need to check the file path of to respective ensure integrity

                # Get the data at the current line
                data_at_current_line = FileInterface.line_from_file(enemies_wad_path, current_line_index) 
                data_at_current_line = data_at_current_line[0]
                # Get the desired path to of the file 
                desired_path = script_directory + data_at_current_line

                FileInterface.append_data(absolute_enemies_wad_path, desired_path) # Copy to absolute file path
                

            elif(line[0] != "#"): 
                # Is a user modified directory
                FileInterface.append_data(absolute_enemies_wad_path, line.replace("\n", "").replace("@", "")) # Copy to absolute file path 
                
            current_line_index += 1;
    print("2/3 complete...")
    # Loop through locations wad file, update directories and decide which ones have been modded and copy across to respective absolute wad file  
    with open(locations_wad_path, "r") as locations_wad_file: 
        current_line_index = 0;
        for line in locations_wad_file:
            line = line.replace("\n", "")
            if(line != "" and line[0] == single_backslash): # Local file that we need to check the file path of to respective ensure integrity

                # Get the data at the current line
                data_at_current_line = FileInterface.line_from_file(locations_wad_path, current_line_index) 
                data_at_current_line = data_at_current_line[0]
                # Get the desired path to of the file 
                desired_path = script_directory + data_at_current_line

                FileInterface.append_data(absolute_location_wad_path, desired_path) # Copy to absolute file path
                

            elif(line[0] != "#"): 
                # Is a user modified directory
                FileInterface.append_data(absolute_location_wad_path, line.replace("\n", "").replace("@", "")) # Copy to absolute file path 
                
            current_line_index += 1;
    print("3/3 complete...")



    # Close files 
    abs_ui_wad_file.close()
    abs_enemies_wad_file.close()
    abs_locations_wad_file.close()

    print("Booting game...")



