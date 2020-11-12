import os, FileInterface, random
from PIL import ImageTk, Image


def get_enemy_sprite(name, res_scale):
    script_directory = os.path.dirname(__file__) #<-- absolute directory the script is in

    relational_path = "GameData\\Absolute_Enemies.wad"
    absolute_path_to_wad = os.path.join(script_directory, relational_path)

    index_of_sprite_group = FileInterface.data_index(absolute_path_to_wad, name)
    
    respective_image_path = FileInterface.line_from_file(absolute_path_to_wad, index_of_sprite_group + 1)
    respective_image_path = respective_image_path[0]

    image_width = round(524 * res_scale);
    image_height = round(340 * res_scale);

    try:
        # Try to load image from path file 

        image = Image.open(respective_image_path)
        image = image.resize((image_width, image_height), Image.ANTIALIAS)
        image_data = ImageTk.PhotoImage(image)
    except:
        # If image encountered error while loading, load a default image 
        image_data = ImageTk.PhotoImage(Image.open(script_directory + "\\GameData\\Fallback.png"))

    return image_data;


def get_UI_sprite(name, res_scale):
    script_directory = os.path.dirname(__file__) #<-- absolute directory the script is in

    relational_path = "GameData\\Absolute_UI.wad"
    absolute_path_to_wad = os.path.join(script_directory, relational_path)

    index_of_sprite_group = FileInterface.data_index(absolute_path_to_wad, name)
    
    respective_image_path = FileInterface.line_from_file(absolute_path_to_wad, index_of_sprite_group + 1)
    respective_image_path = respective_image_path[0]


    image_width = round(24 * res_scale);
    image_height = round(24 * res_scale);

    try:
        # Try to load image from path file 
        image = Image.open(respective_image_path)
        image = image.resize((image_width, image_height), Image.ANTIALIAS)
        image_data = ImageTk.PhotoImage(image)
    except:
        # If image encountered error while loading, load a default image 
        image_data = ImageTk.PhotoImage(Image.open(script_directory + "\\GameData\\Fallback.png"))

    return image_data;
    

def get_location_sprite(name, res_scale):
    script_directory = os.path.dirname(__file__) #<-- absolute directory the script is in
    relational_path = "GameData\\Absolute_Locations.wad"
    absolute_path_to_wad = os.path.join(script_directory, relational_path)

    index_of_sprite_group = FileInterface.data_index(absolute_path_to_wad, name)
    respective_image_path = FileInterface.line_from_file(absolute_path_to_wad, index_of_sprite_group + 1)
    
    respective_image_path = respective_image_path[0]

    image_width = round(524 * res_scale);
    image_height = round(340 * res_scale);

    try:
        # Try to load image from path file 
        image = Image.open(respective_image_path)
        image = image.resize((image_width, image_height), Image.ANTIALIAS)
        image_data = ImageTk.PhotoImage(image)
    except Exception as exc:
        print(exc)
        # If image encountered error while loading, load a default image 
        image_data = ImageTk.PhotoImage(Image.open(script_directory + "\\GameData\\Fallback.png"))

    return image_data;

def get_random_player_sprite(gender, res_scale):
    script_directory = os.path.dirname(__file__) #<-- absolute directory the script is in
    if(gender.capitalize() == "Male"):
        image_number = random.randrange(1, 15)
    else:
        image_number = random.randrange(1, 5)
    relational_path = "\\Sprites\\Player_" + gender.capitalize() + "\\" + gender.capitalize() + str(image_number) + ".png"
    absolute_path = os.path.join(script_directory + relational_path)


    image_width = round(340 * res_scale);
    image_height = round(342 * res_scale);

    image = Image.open(absolute_path)
    image = image.resize((image_width, image_height), Image.ANTIALIAS)

    image_data = ImageTk.PhotoImage(image)
    return image_data, image_width, image_height, absolute_path;


def get_player_sprite(path, res_scale):
    image_width = round(524 * res_scale);
    image_height = round(340 * res_scale);
    script_directory = os.path.dirname(__file__);

    try:
        image = Image.open(path)
        image = image.resize((image_width, image_height), Image.ANTIALIAS)
        image_data = ImageTk.PhotoImage(image)
    except Exception as exc:
        print(exc)
        # If image encountered error while loading, load a default image
        image = Image.open(script_directory + "\\GameData\\Fallback.png")
        image = image.resize((image_width, image_height), Image.ANTIALIAS)
        image_data = ImageTk.PhotoImage(image)

    return image_data;

