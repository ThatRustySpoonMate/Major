from tkinter import *

stats = [1,1,1,1,1]
avaliable_points = 20
current_displayed_description = None

def get_character_customisation():

    def finalize():
        global character_data
        character_data = [name_input.get(), stats]
        if(character_data[0] != "" and character_data[0].isspace() == False and avaliable_points == 0):
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
            descriptions[skill_index].place(x = 370, y = 30)
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
    done_button = Button(root, text="DONE", width = 5, height=1, command=finalize)

    strength_label = Label(root, text = "Strength", font=("Courier", 12))
    strength_points = Label(root, text = 1, font=("Courier", 14))
    strength_points_help = Button(root, text = "?", relief="flat", font=("Courier", 9), command = lambda:show_descripton(0, descriptions))
    strength_points_up = Button(root,text = ">", command = lambda:skill_change(0, 1), relief="flat")
    strength_points_down = Button(root,text = "<", command = lambda:skill_change(0, -1), relief="flat")
    strength_description = Text(root, width = 32, height = 20, relief="sunken")
    strength_description.insert(0.0,"STRENGTH:\nSupplies are sparse\nSo on seeing something sweet\nBe sure to scavenge, or starve\nThe stronger you aren't, the smaller the stack\nOf scrap, storage and snacks\nThat you can haul on your back\nBut do be sure to stay on track of the numbers\nOr a savage could suddenly strike as you're over-encumbered\nAnd should your special self have such a regrettable incident\nYou'd better get swinging any suitable weapon or implement")
    strength_description.configure(state = DISABLED)
    strength_label.place(x = 40, y=110)
    strength_points.place(x = 230, y=110)
    strength_points_up.place(x = 260, y = 110)
    strength_points_down.place(x = 210, y = 110)
    strength_points_help.place(x=122, y=105)




    insight_label = Label(root, text = "Insight", font=("Courier", 12))
    insight_points = Label(root, text = 1, font=("Courier", 14))
    insight_points_help = Button(root, text = "?", relief="flat", font=("Courier", 9), command = lambda:show_descripton(1, descriptions))
    insight_points_up = Button(root, text = ">", command = lambda:skill_change(1, 1), relief="flat")
    insight_points_down = Button(root, text = "<", command = lambda:skill_change(1, -1), relief="flat")
    insight_description = Text(root, width = 32, height = 20)
    insight_description.insert(0.0, "INSIGHT:\nPost-nuclear places\nAre pretty prearranged\nTo put you through your paces\nPinpoint the parts of predators that plan to prey\nWith the Vault-Tec Assisted Targeting System\nHooray!\nYou may need to pickpocket\nPinching for your own protection\nPracticing your pilfering\nPurloining to perfection\nIf your preferential predilection's\nPetty theft of peoples' possessions\nYou'll be protected by perception")
    insight_description.configure(state = DISABLED)
    insight_label.place(x = 40, y =170)
    insight_points.place(x = 230, y =170)
    insight_points_up.place(x = 260, y = 170)
    insight_points_down.place(x = 210, y = 170)
    insight_points_help.place(x=122, y=165)


    fortune_label = Label(root, text = "Fortune", font=("Courier", 12))
    fortune_points = Label(root, text = 1, font=("Courier", 14))
    fortune_points_help = Button(root, text = "?", relief="flat", font=("Courier", 9), command = lambda:show_descripton(2, descriptions))
    fortune_points_up = Button(root, text = ">", command = lambda:skill_change(2, 1), relief="flat")
    fortune_points_down = Button(root, text = "<", command = lambda:skill_change(2, -1), relief="flat")
    fortune_description = Text(root, width = 32, height = 20)
    fortune_description.insert(0.0, "FORTUNE:\nThe lady\nThat lowers the likelihood of life's lotto's loss for the lazy\nWhen you're larking with lice\nThat are larger than life\nAt least you'll have the lethal last laugh and the like\nThe lie of the land's less than lavish and lovely\nBut when looking for loot you'll locate lots of luxury\nLoads of little lowlifes leering at your luggage?\nA lone laddy's liable to let them them learn what luck is")
    fortune_description.configure(state = DISABLED)
    fortune_label.place(x = 40, y =230)
    fortune_points.place(x = 230, y =230)
    fortune_points_up.place(x = 260, y = 230)
    fortune_points_down.place(x = 210, y = 230)
    fortune_points_help.place(x=122, y=225)


    charisma_label = Label(root, text = "Charisma", font=("Courier", 12))
    charisma_points = Label(root, text = 1, font=("Courier", 14))
    charisma_points_help = Button(root, text = "?", relief="flat", font=("Courier", 9),command = lambda:show_descripton(3, descriptions))
    charisma_points_up = Button(root, text = ">", command = lambda:skill_change(3, 1), relief="flat")
    charisma_points_down = Button(root, text = "<", command = lambda:skill_change(3, -1), relief="flat")
    charisma_description = Text(root, width = 32, height = 20)
    charisma_description.insert(0.0, "CHARISMA\nCommunists conquered this clean continent\nAnd concomitantly corruption was the consequence\nAs such, you must be confident\nAnd cognizant of compliments\nConfirming that commercially you're consummately competent\nConvert companions to confidantes\nConvincing them to change a cuddly toy\nFor cutlery and condiments\nSwallow down countless cups of cocktails\nAnd charm your way from harm, chum\nCombat curtailed")
    charisma_description.configure(state = DISABLED)
    charisma_label.place(x = 40, y =290)
    charisma_points.place(x = 230, y =290)
    charisma_points_up.place(x = 260, y = 290)
    charisma_points_down.place(x = 210, y = 290)
    charisma_points_help.place(x=122, y=285)


    agility_label = Label(root, text = "Agility", font=("Courier", 12))
    agility_points = Label(root, text = 1, font=("Courier", 14))
    agility_points_help = Button(root, text = "?", relief="flat", font=("Courier", 9),command = lambda:show_descripton(4, descriptions))
    agility_points_up = Button(root, text = ">", command = lambda:skill_change(4, 1), relief="flat")
    agility_points_down = Button(root, text = "<", command = lambda:skill_change(4, -1), relief="flat")
    agility_description = Text(root, width = 32, height = 20)
    agility_description.insert(0.0, "AGILITY:\nAfter all the aggro\nAntagonists are all too available\nThere's no ASBOs\nAccelerate your acts of accurate aim\nAnd have any angry adversaries aptly aflame\nAvoid adverse assaults from automatics\nAvert or annul their action with acrobatics\nAgility!\nAmazing adaptability\nAwesome!\nWhat an absolutely ace ability")
    agility_description.configure(state = DISABLED)
    agility_label.place(x = 40, y =350)
    agility_points.place(x = 230, y =350)
    agility_points_up.place(x = 260, y = 350)
    agility_points_down.place(x = 210, y = 350)
    agility_points_help.place(x=122, y=345)


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
