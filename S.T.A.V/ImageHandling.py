import os
from PIL import ImageTk, Image

def get_sprite(name, resolution):
    correlating_res = get_image_resolution(resolution)
    script_directory = os.path.dirname(__file__) #<-- absolute directory the script is in
    relational_path  = "EnemySprites\\" + name + " " + correlating_res + ".png"
    absolute_path = os.path.join(script_directory, relational_path)

    return ImageTk.PhotoImage(Image.open(absolute_path))


def get_image_resolution(game_resolution):
    if(game_resolution == "1024x576"):
        correlating_res = "524x340"
    elif(game_resolution == "1280x720"):
        correlating_res = "655x425"	
    elif(game_resolution == "1920x1080"):
        correlating_res = "982x637"
    else:
        correlating_res = "1310x850"

    return correlating_res
