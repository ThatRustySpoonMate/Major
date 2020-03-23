#resolution = get_user_resolution("640x480", "1280x720", "1920x1080", "2560x1440", "3840x2160") SYNTAX
from tkinter import *



def get_user_resolution(*args):
    global tkvar, confirmed, target_res

    confirmed = False
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.title("Resolution Selection")
    tkvar = StringVar(root)

    target_res = args[0]

    def confirmChoice():
        # confirmed
        root.quit()
        confirmed = True

    # on change dropdown value
    def change_dropdown(*args):
        global target_res
        target_res = tkvar.get() 


    #Default resolution
    horizontal = 200
    vertical = 200

    if(len(args) > 3):
        vertical += 20 * (len(args) - 3)

    root.geometry(str(horizontal) + "x" + str(vertical) + "+" + str(round(screen_width / 2)) + "+" + str(round(screen_height / 2)))

    root.resizable(False, False)

    #Setting up drop down selection
    choices = args
    tkvar.set(args[0]) #Set the default option
    #Create dropdown selection
    resolution_selector = OptionMenu(root, tkvar, *choices) #Root, Default Option, Choices
    Label(root, text="Select resolution").place(x = 50, y = 50)
    resolution_selector.place(x = 50 , y = 75)
    confirmationButton = Button(root, text = "Confirm", command = confirmChoice).place(x=70, y = 150)


    # link function to change dropdown
    tkvar.trace('w', change_dropdown)

    root.mainloop()

    try:
        root.destroy()
    except Exception as e:
        input(e)
    

    return target_res


