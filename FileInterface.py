def line_from_file(file_path, start, stop=None, step=None):
    with open(file_path, "r") as target_file:
        current_line = 0;
        data_to_return = []
        for line in target_file:
            if(current_line == start and stop == None and step == None):
                data_to_return.append(line.replace("\n", ""));
            elif(stop != None and current_line >= start and current_line <= stop and step == None):
                 data_to_return.append(line.replace("\n", ""));
            elif(stop != None and current_line >= start and current_line <= stop and (current_line - start) % step == 0):
                 data_to_return.append(line.replace("\n", ""));
            current_line += 1;

        return data_to_return; # Returns an array

def file_data(file_path, return_type = "list", file_type = "lbl"):
        try:

            if(return_type == "string"):
                target_file = open(file_path, "r")
                file_data = target_file.read()
                target_file.close()
            elif(return_type == "list"):
                file_data = []
                if(file_type == "lbl"): # Line by line file
                    for i in range(0, length_of_file(file_path) + 1):
                        file_data.append(line_from_file(file_path, i))
                elif(file_type == "csv"): # Comma separated values
                    target_file = open(file_path, "r")
                    file_data_string = target_file.read()
                    target_file.close()
                    file_data = file_data_string.split(",")

            return file_data # Returns string
        except Exception as ex:
            return "Failed: " + str(ex) 

def create_file(file_path, name, extension = ".txt"):
    try:
        new_file = open(file_path + "\\" + name + extension, "x")
        new_file.close()
        return file_path + "\\" + name + ".txt"
    except Exception as ex:
        return ["Failed:", str(ex)]

def append_data(file_path, text, new_line = True):
    try:
        file = open(file_path, "a")
        file.write(new_line * "\n" + str(text)) # Convert text to string when writing to avoid an error
        file.close()
        return ["Success"]
    except Exception as ex:
        return ["Failed:", str(ex)]

def data_index(file_path, search_text, case_sens=False, occurence_to_find=1): # Takes a string and finds the location of it within a text document, occurence_to_find is an optional specifier that allows change of the occurence to retireve the position at, e.g. the 3rd time a data point comes up in a set of data  
    if(occurence_to_find == -1):
        data_position = [] # Set occurence_to_find to -1 if locations of all search text in file is required
    else:
        data_position = -1; # Returns -1 if search text can't be found
    current_line = 0;
    occurence_count = 0; 
    search_text = str(search_text) # Convert the search text to a string to avoid errors when looking for numbers


    with open(file_path, "r") as target_file:
        for line in target_file:
            if(case_sens == False):
                search_text = search_text.lower() # Generalise search term
                line = line.lower()               # Generalise search result

            if(search_text == line.replace("\n", "")): # Found line
                occurence_count += 1
                if(occurence_to_find == -1):
                    data_position.append(current_line)
                if(occurence_count == occurence_to_find):
                    data_position = current_line
                    break;

            current_line += 1


    return data_position # Returns array or int 

def length_of_file(file_path, exclude_whitespace = False):
    try:
        target_file = open(file_path, "r")
        line_count = 0
        for line in target_file:
            if(exclude_whitespace == True):
                if(line == "\n"):
                    line_count -= 1;
            line_count += 1;
        target_file.close()
        return line_count; # Returns int

    except Exception as ex:
        return "Failed: " + str(ex)

def change_line(file_path, index, replacement_data):
    try:
        target_file = open(file_path, "r+") # Open the file
    except Exception as ex:
        return "Failed: " + str(ex)

    # If file successfuly opened
    target_file_data = file_data(file_path)  # Get data from file
    target_file_data = target_file_data.split("\n") # Transform file data into array of lines
    #print(target_file_data)
    target_file_data[index] = replacement_data; # Replace data at index location
    target_file.truncate(0) # Delete all data from file to prevent overwriting

    i = 0 # Initialise index of array
    for line in target_file_data: # Loop through each line in the array of data from text file
        if(i != len(target_file_data) - 1):
            target_file_data[i] = line + "\n" # Add a new line segment to the end of each line
        i += 1; # Iterate array index

    target_file.writelines(target_file_data) # Rewrite new data over old data

    target_file.close()
    return "Success"


def clear_contents(file_path):

    try:
        target_file = open(file_path, "r+") # Open the file
    except Exception as ex:
        return "Failed: " + str(ex)

    target_file.truncate(0)
    target_file.close()
    return "Success"
