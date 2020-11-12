import time

def initialise_elapsed_time(): #Call at start of program
    global initial_time
    initial_time = time.time()


def get_elapsed_time(): #Gets the time since the program was opened
    global initial_time

    current_time = time.time()

    elapsed_time = current_time - initial_time
    return(round(elapsed_time))

