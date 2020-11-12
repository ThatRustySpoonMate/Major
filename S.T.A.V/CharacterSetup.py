from tkinter import *

stats = [1,1,1,1,1]
avaliable_points = 20
current_displayed_description = None

def get_character_customisation():
    #return ["REMOVE THIS",  [5,5,5,5,5], "Female"]
    def finalize():
        global character_data
        character_data = [name_input.get(), stats, gender.get()]
        character_limit = 30;
        if(character_data[0] != "" and character_data[0].isspace() == False and avaliable_points == 0 and not "@" in character_data[0] and len(character_data[0]) <= character_limit):
            root.quit()


    def skill_change(skill_index, sign):
        global avaliable_points
        if(stats[skill_index] > 1 or sign == 1):

            if(avaliable_points > 0 or sign == -1):
                stats[skill_index] += sign
                avaliable_points += -sign
                avaliable_points_label.configure(text = avaliable_points)

            if(skill_index == 0):
                strength_points.configure(text = stats[0])
            elif(skill_index == 1):
                insight_points.configure(text = stats[1])
            elif(skill_index == 2):
                fortune_points.configure(text = stats[2])
            elif(skill_index == 3):
                charisma_points.configure(text = stats[3])
            elif(skill_index == 4):
                agility_points.configure(text = stats[4])

    def show_descripton(skill_index, descriptions):
        global current_displayed_description

        if(skill_index == current_displayed_description):
            descriptions[skill_index].place_forget()
            current_displayed_description = None
        else:
            #Show the description of skill onscreen
            descriptions[skill_index].place(x = 350, y = 110)
            current_displayed_description = skill_index

        #Make all other previous descriptions dissapear
        for description in descriptions:
            if(description != descriptions[skill_index]):
                description.place_forget()



    root = Tk()
    root.title("Character Customisation")
    root.geometry("640x480")

    name_label = Label(root, text="Name:", font=("Courier", 12))
    name_input = Entry(root, width=20, font=("courier", 12 ))
    done_button = Button(root, text="Launch Game", width = 10, height=1, command=finalize)

    gender = StringVar()
    gender.set("Male")
    genders = ["Male", "Female"]
    male_female_cb = OptionMenu(root, gender, *genders)
    male_female_cb.place(x = 400, y = 30)




    fortune_label = Label(root, text = "Fortune", font=("Courier", 12))
    fortune_points = Label(root, text = 1, font=("Courier", 14))
    fortune_points_help = Button(root, text = "?", relief="flat", fg = "red", font=("Courier", 11), command = lambda:show_descripton(2, descriptions))
    fortune_points_up = Button(root, text = ">", command = lambda:skill_change(2, 1), relief="flat")
    fortune_points_down = Button(root, text = "<", command = lambda:skill_change(2, -1), relief="flat")
    fortune_description = Text(root, width = 32, height = 16)
    fortune_description.insert(0.0, "FORTUNE:\n- Increases quality of loot found from enemies \n- Increases quality of loot from chests \n- Increases chances of winning at the gambler")
    fortune_description.configure(state = DISABLED)
    fortune_label.place(x = 40, y =110)
    fortune_points.place(x = 230, y =110)
    fortune_points_up.place(x = 260, y = 110)
    fortune_points_down.place(x = 210, y = 110)
    fortune_points_help.place(x=112, y=105)

    insight_label = Label(root, text = "Insight", font=("Courier", 12))
    insight_points = Label(root, text = 1, font=("Courier", 14))
    insight_points_help = Button(root, text = "?", relief="flat", fg="red", font=("Courier", 11), command = lambda:show_descripton(1, descriptions))
    insight_points_up = Button(root, text = ">", command = lambda:skill_change(1, 1), relief="flat")
    insight_points_down = Button(root, text = "<", command = lambda:skill_change(1, -1), relief="flat")
    insight_description = Text(root, width = 32, height = 16)
    insight_description.insert(0.0, "INSIGHT:\n- Increases chance to crit \n- Increases accuracy with ranged weapons")
    insight_description.configure(state = DISABLED)
    insight_label.place(x = 40, y =170)
    insight_points.place(x = 230, y =170)
    insight_points_up.place(x = 260, y = 170)
    insight_points_down.place(x = 210, y = 170)
    insight_points_help.place(x=112, y=165)

    charisma_label = Label(root, text = "Charisma", font=("Courier", 12))
    charisma_points = Label(root, text = 1, font=("Courier", 14))
    charisma_points_help = Button(root, text = "?", relief="flat", fg="red", font=("Courier", 11),command = lambda:show_descripton(3, descriptions))
    charisma_points_up = Button(root, text = ">", command = lambda:skill_change(3, 1), relief="flat")
    charisma_points_down = Button(root, text = "<", command = lambda:skill_change(3, -1), relief="flat")
    charisma_description = Text(root, width = 32, height = 16)
    charisma_description.insert(0.0, "CHARISMA\n- Lowers prices at merchant")
    charisma_description.configure(state = DISABLED)
    charisma_label.place(x = 40, y =230)
    charisma_points.place(x = 230, y =230)
    charisma_points_up.place(x = 260, y = 230)
    charisma_points_down.place(x = 210, y = 230)
    charisma_points_help.place(x=122, y=225)

    agility_label = Label(root, text = "Agility", font=("Courier", 12))
    agility_points = Label(root, text = 1, font=("Courier", 14))
    agility_points_help = Button(root, text = "?", relief="flat", fg="red", font=("Courier", 11),command = lambda:show_descripton(4, descriptions))
    agility_points_up = Button(root, text = ">", command = lambda:skill_change(4, 1), relief="flat")
    agility_points_down = Button(root, text = "<", command = lambda:skill_change(4, -1), relief="flat")
    agility_description = Text(root, width = 32, height = 16)
    agility_description.insert(0.0, "AGILITY:\n- Increases chances of successfully evading enemy \n- Increases chance to dodge an enemy attack")
    agility_description.configure(state = DISABLED)
    agility_label.place(x = 40, y =290)
    agility_points.place(x = 230, y =290)
    agility_points_up.place(x = 260, y = 290)
    agility_points_down.place(x = 210, y = 290)
    agility_points_help.place(x=112, y=285)

    strength_label = Label(root, text = "Strength", font=("Courier", 12))
    strength_points = Label(root, text = 1, font=("Courier", 14))
    strength_points_help = Button(root, text = "?", relief="flat", fg="red", font=("Courier", 11), command = lambda:show_descripton(0, descriptions))
    strength_points_up = Button(root,text = ">", command = lambda:skill_change(0, 1), relief="flat")
    strength_points_down = Button(root,text = "<", command = lambda:skill_change(0, -1), relief="flat")
    strength_description = Text(root, width = 32, height = 16, relief="sunken")
    strength_description.insert(0.0,"STRENGTH:\n- Increases carry weight \n- Increases damage with melee weapons")
    strength_description.configure(state = DISABLED)
    strength_label.place(x = 40, y=350)
    strength_points.place(x = 230, y=350)
    strength_points_up.place(x = 260, y = 350)
    strength_points_down.place(x = 210, y = 350)
    strength_points_help.place(x=122, y=345)



    avaliable_points_label = Label(root, text = avaliable_points, font=("courier", 20))
    avaliable_points_disclaimer = Label(root, text = "Points Remaining", font=("Courier", 11))
    avaliable_points_label.place(x = 100, y = 400)
    avaliable_points_disclaimer.place(x=50, y = 440)


    name_label.place(x = 40, y= 30)
    name_input.place(x = 140, y = 30)
    done_button.place(x = 300, y = 440)

    descriptions = [strength_description, insight_description, fortune_description, charisma_description, agility_description]


    root.mainloop()



    try: 
        root.destroy()
    except Exception as e:
        input(e)


    return character_data
