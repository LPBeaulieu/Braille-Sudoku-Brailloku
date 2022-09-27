import random
import os
import copy
import sys
import re
from alive_progress import alive_bar

print('Now generating one of your "Brailloku" Sudoku puzzles!\n')

#Difficulty levels (based on the article
#Procedia Technology 2013 10 392-399):
#1-Extremely easy: more than 46 clues
#2-Easy: 36-46 clues
#3-Medium: 32-35 clues
#4-Difficult: 28-31 clues
#5-Evil: 17-27 clues
#It should be noted that when generating a more difficult sudoku
#puzzle (around 46 empty cells), the time required in some cases
#can exceed 5 seconds, but is otherwise generally lower than two
#seconds.

#The user can specify the number of desired empty cells
#(up to 46, inclusively) as an additional argument, when running
#the Python code, by specifying the number of empty cells preceded
#by the letter "e". For example "python3 brailloku.py e46" would
#generate a sudoku puzzle with 46 empty cells. Furthermore, the user
#can specify how many sudoku puzzles (each contained within its
#own PEF file) he or she wishes to generate by preceding that number
#by the letter "n". For example "python3 brailloku.py n50" would
#generate 50 sudoku puzzles. Both these arguments can either be used alone,
#or in combination in any order, as the letter allows to distinguish them.
#Finally, the user can opt for a truncated version of the sudoku grid
#excluding some of the header text and the topmost and lowest horizontal
#delimiters, bringing the number of lines per page down to 18 lines, which
#allows for embossing on A4 paper in landscape mode. They would then enter
#"short" as an additional argument after the Python call and the variable
#"short" (initialized to "False"), would then be set to "True".

#The variable "user_input_number_of_empty_cells" initialized to false,
#and is set to "True" if the user selects a number of empty cells below 47.
#If "number_of_removed_digits_before_function_call" is "False", then the
#"number_of_empty_cells" is initialized for every generated puzzle by
#selecting a random number in the range of 26 and 46 (inclusively), which
#corresponds to extremely easy to easy puzzles, but with the added difficulty
#of having to play without visual references and pencil marking notes.
#In fact, the code struggles to find more than 46 cells to remove that all
#meet at least one of the seven basic criteria (listed in the functions
#"criterion_1" to "criterion_7") used in solving sudoku puzzles without pencil marks.
number_of_puzzles = 1
user_input_number_of_empty_cells = False
short = False
try:
    if len(sys.argv) > 1:
        for argv in sys.argv[1:]:
            if argv[0] == "e" and int(argv[1:]) < 47:
                user_input_number_of_empty_cells = True
                target_number_of_empty_cells = int(argv[1:])
            elif argv[0] == "e" and int(argv[1:]) >= 47:
                target_number_of_empty_cells = 46
                print("Sorry, the maximal amount of empty cells in Brailloku is 46." +
                "\nHere is a puzzle with 46 empty cells: \n\n")
            elif argv[0] == "n":
                number_of_puzzles = int(argv[1:])
            elif argv.isalpha() and argv.lower() == "short":
                short = True
except:
    pass

with alive_bar(number_of_puzzles) as bar:
    for i in range(number_of_puzzles):
        if user_input_number_of_empty_cells == False:
            target_number_of_empty_cells = random.randint(26,46)

        def make_sudoku(substitution_row_boxes_2_done, substitution_row_boxes_3_done):
            #A random column within the 9x9 sudoku grid will be filled with random digits taken from the
            #"initial_random_numbers" list. In other words, a "column_box" value (0, 1 or 2) within a random
            #element of "column_boxes" (0, 1, 2) will be selected as the starting column to insert the random
            #numbers. This may help ensure maximal variance in the makup of the sudoku grid, so that every
            #puzzle is different (I'm not a probability statistician, so I just included this additional
            #element of randomness in the initial column selection as an extra precaution, without knowing
            #exactly if/how much it helps in the overall randomization of the sudoku grid).
            def fill_first_column(sudoku_grid, row_boxes, column_boxes,
            row_box, column_box, initial_random_numbers, initial_random_numbers_index):
                #The "for _ in range(3):" loop will cycle through every column "column_box", of a given row
                #within a box and assign it a number from the "initial_random_numbers" list. This list
                #will also be useful later in the code, because it contains information as to the location
                #of the first digits included in the sudoku grid. This data will prevent placing the same numbers
                #within the same row, column or box. An index "initial_random_numbers_index" is therefore used
                #to navigate the list instead of popping out the elements as they are placed within the sudoku grid,
                #in order to keep "initial_random_numbers_index" intact for later reference.
                for _ in range(3):
                    sudoku_grid[row_boxes][column_boxes][row_box][column_box] = (
                    initial_random_numbers[initial_random_numbers_index])
                    initial_random_numbers_index += 1
                    #After assigning a number to a given column, move on to the next
                    #row within the same box (for the same "box_column"), unless you are
                    #already at the last row of the box, in which case "row_box" set
                    #to 0 in order to start at the first row of the next row of boxes
                    #(walking down the sudoku grid).
                    if row_box < 2:
                        row_box += 1
                    else:
                        row_box = 0
                #After the "for _ in range(3):" loop has assigned random numbers (in the
                #same column, "column_box") to every row of a given box, it will move on
                #to the next row of boxes ("row_boxes += 1"), if it is not already at the
                #last row of boxes (row 2). The "fill_first_column" function is being called
                #three times within a "for _ in range(3):" loop in order to assign numbers
                #in each of the three row of boxes.
                if row_boxes < 2:
                    row_boxes += 1

                return (sudoku_grid, row_boxes, column_boxes,
                row_box, column_box, initial_random_numbers, initial_random_numbers_index)

            #The function "insert_numbers" will screen the 9x9 sudoku grid row by row and assign
            #random numbers to every cell that contains a 0, insofar as the number it inserts isn't
            #found in the same line, column or box, as per sudoku rules.
            def insert_numbers(sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i):
                #"column_box" is initialized to 0 so that every time the function "insert_numbers" is
                #called, the first column within a box will be considered. "column_box" will be incremented
                #if there is already a non-zero digit at that location. The "for _ in range(3):" loop will
                #thus cover each of the three possible values of "column_box" before returning, whether or
                #not there has been number insertion into one of the positions.
                column_box = 0
                for _ in range(3):
                    #The "row" list contains all the digits within one of the nine rows of the 9x9 sudoku grid.
                    #As the row encompasses digits from every value of "column_boxes" (from every box in the row),
                    #the numbers 0,1 and 2 can be used instead of the variable "column_boxes".
                    row = (sudoku_grid[row_boxes][0][row_box] + sudoku_grid[row_boxes][1][row_box] +
                    sudoku_grid[row_boxes][2][row_box])
                    #The "column" list contains all the digits within one of the nine columns of the 9x9 sudoku grid.
                    #As the column contains one digit from each row of the 9x9 sudoku grid, the variables "row_boxes"
                    #and "row_box" do not need to be used, as all permutations are covered in number form below (0, 1 and 2).
                    column = ([sudoku_grid[0][column_boxes][0][column_box]] +
                    [sudoku_grid[0][column_boxes][1][column_box]] +
                    [sudoku_grid[0][column_boxes][2][column_box]] +
                    [sudoku_grid[1][column_boxes][0][column_box]] +
                    [sudoku_grid[1][column_boxes][1][column_box]] +
                    [sudoku_grid[1][column_boxes][2][column_box]] +
                    [sudoku_grid[2][column_boxes][0][column_box]] +
                    [sudoku_grid[2][column_boxes][1][column_box]] +
                    [sudoku_grid[2][column_boxes][2][column_box]])
                    #Flattening the list of lists representing the three rows of the box
                    #(sudoku_grid[row_boxes][column_boxes]) using list comprehension
                    box = [item for sublist in sudoku_grid[row_boxes][column_boxes] for item in sublist]
                    #If the digit in the cell under investigation isn't zero, it means that it has already
                    #been substituted. Furthermore, if the "column_box" variable is equal to 2, it means
                    #that the last digit of a row within a box has already been assigned, and we can move
                    #on to the next box within the row of boxes by incrementing ("column_boxes").
                    if sudoku_grid[row_boxes][column_boxes][row_box][column_box] != 0 and column_box == 2:
                        column_boxes+=1
                    #If the digit in the cell under investigation isn't zero, it means that it has already
                    #been substituted. Furthermore, if the "column_box" variable is not equal to 2, it means
                    #that the las digit of a row within a box has not already been assigned, and we can move
                    #on to the next column within the row of the same box by incrementing ("column_box").
                    elif sudoku_grid[row_boxes][column_boxes][row_box][column_box] != 0 and column_box != 2:
                        column_box+=1
                    #If the digit in the cell under investigation is a zero, it means that it hasn't been
                    #substituted yet. We must now determine whether it the random number at index "i" of the
                    #list "random_numbers" fills the conditions required for its inclusion at that cell of
                    #the sudoku grid, namely that it is not already found in the same row, column or box.
                    #If the substitution takes place, then the digit is removed from the "random_numbers"
                    #list ("random_numbers.pop(i)").
                    elif (sudoku_grid[row_boxes][column_boxes][row_box][column_box] == 0 and
                    random_numbers[i] not in row and random_numbers[i] not in column and
                    random_numbers[i] not in box):
                        sudoku_grid[row_boxes][column_boxes][row_box][column_box] = random_numbers[i]
                        random_numbers.pop(i)
                        #If the substitution has taken place at the last cell of the row of a given box
                        #("column_box == 2"), then the next substitution will occur in the following box
                        #within the same row of boxes, and so "column_boxes" is incremented. Similarly,
                        #if the substitution occured at the second cell of the row of a given box
                        #("column_box == 2") and that the third element is not a zero (because it contains
                        #one of the digits introduced initially in one of the columns of the 9x9 sudoku
                        #grid), then we need to skip over that element and proceed to the next box within
                        #the same row of boxes (and "column_boxes" is incremented in that case as well).
                        if (column_box == 2 or (column_box == 1 and
                        sudoku_grid[row_boxes][column_boxes][row_box][column_box+1] != 0)):
                            column_boxes+=1
                        return sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i

                    #If there is more than one element left in the list "random_numbers" and that
                    #the current element under investigation is a zero and that one of the remaining
                    #elements within the "random_numbers" list meets the requirements for its inclusion
                    #in that cell (not already present in the current row, column or box), then the
                    #substitution is made.
                    elif i < len(random_numbers):
                        for j in range(i, len(random_numbers)):
                            if (sudoku_grid[row_boxes][column_boxes][row_box][column_box] == 0 and
                            random_numbers[j] not in row and random_numbers[j] not in column and
                            random_numbers[j] not in box):
                                sudoku_grid[row_boxes][column_boxes][row_box][column_box] = random_numbers[j]
                                random_numbers.pop(j)
                                #Similar to above, "column_boxes" is incremented once non-zero digits are found
                                #in all three positions of the row under investigation in the current box.
                                if (column_box == 2 or (column_box == 1 and
                                sudoku_grid[row_boxes][column_boxes][row_box][column_box+1] != 0)):
                                    column_boxes += 1
                                return sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i
                #If no substitution has taken place, then the length of the list "random_numbers" will be the
                #same as it initially was (as stored in the variable "length_random_numbers") before it was
                #sent in during the "insert_numbers" function call. This means that none of the remaining
                #digits in the "random_numbers" list could be placed in the current row while meeting the
                #requirements of not already being present in the current row, column or box. The code will
                #then reinitialize "sudoku_grid" at either point at which the latest line was filled with
                #random numbers, or its initial state after including a column of random numbers, if no line
                #has yet been filled. The list "random_numbers" will be created once more so as to yield
                #different results that will meet all the requirements listed above.
                return sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i


            def fill_row_boxes_1(initial_random_numbers, sudoku_grid):
                #Random numbers will be assigned to every zero-containing cell of every row or the
                #9x9 sudoku grid, starting from the first row. As such, the variables "row_boxes",
                #"column_boxes", "row_box" and "column_box" are set to zero. The "current_line"
                #variable is set to zero and will keep track of which line is currently under
                #consideration. This will be important later on in this function to determine
                #whether to repeat from the beginning or last completed line upon reaching
                #a point where it is impossible to assign further numbers within a line
                #(see comments below).
                row_boxes = 0
                column_boxes = 0
                row_box = 0
                column_box = 0
                current_line = 0
                #Generating the randomized list "random_numbers" of nine numbers between 1 and 9,
                #inclusively and without repetition using the "random.sample()" method with a list
                #size "k" of 9. This list will be refreshed for every row that is being filled with
                #random numbers, to ensure that the grid is thoroughly randomized. As a column of
                #the 9x9 sudoku grid has already been filled with random digits, one of the digits
                #in "random_numbers" needs to be removed every time "random_numbers" is regenerated.
                #For example, the first element of "initial_random_numbers" corresponds to the random
                #number that was initially included in the first row. The list "random_number" is then
                #updated to remove the number that is already assigned on that given line of the 9x9
                #sudoku grid. Because when assigning random numbers to a given row, it might happen
                #that the last remaining random digits in the "random_numbers" list cannot be placed
                #in that row, either because these numbers are present in the current line, column or
                #box, as per the sudoku rules, there needs to be a savepoint so that the grid may be
                #reinitialized and the process repeated with a fresh list of "random_numbers" until
                #these conditions are met. As such, the "copy.deepcopy()" method is used to ensure
                #that the nested list "sudoku_grid" is stored on a different location on memory than
                #its copy "initial_grid", so that changes made to "sudoku_grid" will not be carried
                #over to "initial_grid".
                random_numbers = random.sample(range(1,10), k=9)
                random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]
                initial_grid = copy.deepcopy(sudoku_grid)
                sudoku_grid_before_next_line = []
                #The "while row_box < 3:" loop will attempt to substitute random numbers for zeros in
                #the line under consideration, until the three lines of the current row of boxes ("row_boxes")
                #have been completely assigned.
                while row_box < 3:
                    #When a line is completely assigned, the "random_numbers" list will be empty. If this
                    #is the case, and that the row that was just completed within the current box is not the
                    #last one of the box, then "row_box" is incremented in order to proceed to the next
                    #row of the box. Similarly, "current_line" is incremented, as we effectively proceed to
                    #the next line of the 9x9 sudoku grid. Finally, "column_boxes" is reset to zero in order
                    #to start at the first box of the next line. A deep copy  of the sudoku grid is stored in
                    #"sudoku_grid_before_next_line" in case the random number assignment to the next row needs
                    #to be repeated (see comment above concerning "initial_grid"), effectively serving as a
                    #savepoint after the last completed line.
                    if random_numbers == [] and row_box <= 2:
                        row_box += 1
                        current_line += 1
                        column_boxes = 0
                        sudoku_grid_before_next_line = copy.deepcopy(sudoku_grid)
                        #If after incrementing "row_box", it is equal to 3, this means that all three rows
                        #in the current "row_boxes" have been completely filled with random numbers, and
                        #the "while row_box < 3:" loop can consequently be broken in order to move on the
                        #the next "while row_box < 3:" loop pertaining to the following row of boxes.
                        if row_box == 3:
                            initial_random_numbers = initial_random_numbers[1:]
                            return initial_random_numbers, sudoku_grid
                        #As a column of the 9x9 sudoku grid has initially been filled with random digits, one
                        #of the numbers in "random_numbers" needs to be removed every time "random_numbers" is
                        #regenerated (see comments above). To ensure that the first digit in the list
                        #"initial_random_numbers" always corresponds to the number that needs to be removed from
                        #the list "random_numbers", "initial_random_numbers" needs to be truncated every line to
                        #reflect the change in line, up to the last line of the sudoku grid ("current_line == 8").
                        elif current_line < 8:
                            initial_random_numbers = initial_random_numbers[1:]
                            random_numbers = random.sample(range(1,10), k=9)
                            random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]

                    #Every number in the "random_numbers" list will be considered for substitution of the zeros
                    #of the current row. Every time a number has been assigned, and that this number has been
                    #subsequently removed from the list "random_numbers", the length of the list will be changed
                    #and the "for i in range(len(random_numbers)):" loop will be broken in order to avoid indexing
                    #issues. While all the rows of the current row of boxes have not been filled with random digits,
                    #the "for i in range(len(random_numbers)):" loop will be repeated with an updated version of the
                    #"random_numbers".
                    for i in range(len(random_numbers)):
                        length_random_numbers = len(random_numbers)
                        sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i = (
                        insert_numbers(sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i))
                        if len(random_numbers) < length_random_numbers:
                            break
                        #If no substitution has taken place, then the length of the list "random_numbers" will be the
                        #same as it initially was (as stored in the variable "length_random_numbers") before it was
                        #sent in during the "insert_numbers" function call. This means that none of the remaining
                        #digits in the "random_numbers" list could be placed in the current row while meeting the
                        #requirements of not already being present in the current row, column or box. The code will
                        #then reinitialize "sudoku_grid" at either point at which the latest line was filled with
                        #random numbers, or its initial state after including a column of random numbers, if no line
                        #has yet been filled ("current_line == 0"). The list "random_numbers" will be created once
                        #more so as to yield different results that will meet all the requirements listed above.
                        #"column_boxes" is reset to zero (effectively starting at the beginning of the row) because
                        #"sudoku_grid" has been reset either to its initial state after inclusion of a column of
                        #random numbers, or to the latest completed line.
                        elif len(random_numbers) == length_random_numbers:
                            if current_line == 0:
                                sudoku_grid = copy.deepcopy(initial_grid)
                            else:
                                sudoku_grid = copy.deepcopy(sudoku_grid_before_next_line)
                            random_numbers = random.sample(range(1,10), k=9)
                            random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]
                            column_boxes = 0
                            break


            def fill_row_boxes_2(initial_random_numbers, sudoku_grid, substitution_row_boxes_2_done):
                #This second "while row_box < 3:" loop is identical to the first one, with one
                #difference being the value of "row_boxes", which is defined as 1 to account for
                #the fact that the first row of boxes has already been filled with random numbers.
                #Also, "initial_grid" is not defined here, as it was done in the first
                #"while row_box < 3:" loop and there is also no need for the "current_line"
                #variable, both of which were used to reinitialize the sudoku grid when reaching
                #a point where it is impossible to assign further numbers in a given row, because
                #that number is either already present in the line, column or box, as per the sudoku
                #rules. In the second and third rows of boxes ("row_boxes" of 1 and 2, respectively),
                #the grid is in such cases entirely reinitialized (although the column of random numbers is
                #retained) through assigning the value of "False" to the variable "could_not_complete",
                #which returns "sudoku_grid" and "initial_random_numbers" but without changing the
                #value of "substitution_row_boxes_2" or "substitution_row_boxes_3" from "False" to
                #"True", which effectively restarts all three "fill_row_boxes" functions. Only upon
                #having set the value of "substitution_row_boxes_2_done" to "True" can the function
                #"fill_row_boxes_3" be called, and only upon having switched the value of
                #"substitution_row_boxes_2_done" to "True" can the "while substitution_row_boxes_3_done == False:"
                #be broken.
                row_boxes = 1
                column_boxes = 0
                row_box = 0
                column_box = 0
                random_numbers = random.sample(range(1,10), k=9)
                random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]
                could_not_complete = False
                while row_box < 3:
                    if random_numbers == [] and row_box <= 2:
                        row_box += 1
                        column_boxes = 0
                        if row_box == 3:
                            substitution_row_boxes_2_done = True
                            initial_random_numbers = initial_random_numbers[1:]
                            return initial_random_numbers, sudoku_grid, substitution_row_boxes_2_done
                        elif row_box < 8:
                            initial_random_numbers = initial_random_numbers[1:]
                            random_numbers = random.sample(range(1,10), k=9)
                            random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]

                    elif could_not_complete == True:
                        return initial_random_numbers, sudoku_grid, substitution_row_boxes_2_done
                    for i in range(len(random_numbers)):
                        length_random_numbers = len(random_numbers)
                        sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i = (
                        insert_numbers(sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i))
                        if len(random_numbers) < length_random_numbers:
                            break
                        elif len(random_numbers) == length_random_numbers:
                            could_not_complete = True
                            break


            def fill_row_boxes_3(initial_random_numbers, sudoku_grid, substitution_row_boxes_3_done):
                #The only difference between the functions "fill_row_boxes_2" and
                #"fill_row_boxes_3" is that the starting "row_boxes" in "fill_row_boxes_3"
                #is set to 2, since the two first rows of boxes have already been filled
                #with random numbers.
                row_boxes = 2
                column_boxes = 0
                row_box = 0
                column_box = 0
                random_numbers = random.sample(range(1,10), k=9)
                random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]
                could_not_complete = False
                while row_box < 3:
                    if random_numbers == [] and row_box <= 2:
                        row_box += 1
                        column_boxes = 0
                        if row_box == 3:
                            substitution_row_boxes_3_done = True
                            initial_random_numbers = initial_random_numbers[1:]
                            return initial_random_numbers, sudoku_grid, substitution_row_boxes_3_done
                        elif row_box < 8:
                            initial_random_numbers = initial_random_numbers[1:]
                            random_numbers = random.sample(range(1,10), k=9)
                            random_numbers = [number for number in random_numbers if number != initial_random_numbers[0]]
                    elif could_not_complete == True:
                        return initial_random_numbers, sudoku_grid, substitution_row_boxes_3_done
                    for i in range(len(random_numbers)):
                        length_random_numbers = len(random_numbers)
                        sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i = (
                        insert_numbers(sudoku_grid, row_boxes, column_boxes, row_box, column_box, random_numbers, i))
                        if len(random_numbers) < length_random_numbers:
                            break
                        elif len(random_numbers) == length_random_numbers:
                            could_not_complete = True
                            break


            #Generating a randomized list of nine numbers between 1 and 9, inclusively
            #and without repetition using the "random.sample()" method with a list size
            #"k" of 9. These numbers will be used to fill in an initial column in the 9x9
            #sudoku grid, which is initially filled with zeros.
            initial_random_numbers = random.sample(range(1,10), k=9)

            #An index "initial_random_numbers_index" (initialized to 0) is used
            #to navigate the list "initial_random_numbers" instead of popping out
            #the elements as they  are placed within the sudoku grid, in order to
            #keep the list "initial_random_numbers_index" intact for later reference.
            initial_random_numbers_index = 0

            #The initial 9x9 sudoku grid is initialized with zeros to facilitate detection of
            #empty cells versus cells that have a digit between 1 and nine, inclusively.
            #The variables 1-"row_boxes", 2-"column_boxes", 3-"row_box" and 4-"column_box" defined
            #in the code below respectively designate:
            #
            #1-A row of boxes (so the first element in the nested list "sudoku_grid", for example:
            #"sudoku_grid[0]" for the first row of boxes).
            #2-A column of boxes (sudoku_grid[0][0] for the first column of boxes in the first
            #row of boxes).
            #3-A three-digit row within a box (for example: "sudoku_grid[0][0][0] for the first
            #row of three digits, in the first box of the first row of boxes").
            #4-The column within a box (so "sudoku_grid"[0][0][0][0] would designate the digit
            #in the top left corner of the 9x9 sudoku grid).
            sudoku_grid = ([[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],
                            [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],
                            [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]])

            #Since numbers will be assigned for a whole column at a random point within
            #the 9x9 sudoku grid, only the starting indices pertaining to the column in
            #question ("column_boxes" to determine in which column of boxes the "column_box"
            #is found, the latter describing the column index within a given box) need to
            #be randomized.
            row_boxes = 0
            column_boxes = random.choice(range(0,3))
            row_box = 0
            column_box = random.choice(range(0,3))
            #The "fill_first_column" function is being called three times within a
            #"for _ in range(3):" loop in order to assign numbers in each of the
            #three row of boxes.
            for _ in range(3):
                sudoku_grid, row_boxes, column_boxes, row_box, column_box, initial_random_numbers, initial_random_numbers_index = (
                fill_first_column(sudoku_grid, row_boxes, column_boxes, row_box, column_box,
                initial_random_numbers, initial_random_numbers_index))

            initial_random_numbers, sudoku_grid = fill_row_boxes_1(initial_random_numbers, sudoku_grid)
            initial_random_numbers, sudoku_grid, substitution_row_boxes_2_done = fill_row_boxes_2(initial_random_numbers, sudoku_grid, substitution_row_boxes_2_done)

            #The function "fill_row_boxes_3()" is only called if "substitution_row_boxes_2_done" is set to True,
            #to ensure that if "initial_random_numbers" and "sudoku_grid" are returned without switching
            #"substitution_row_boxes_2_done" to "True" (as would be the case if no further random digits in
            #the list "random_numbers" could be assigned in a given row because those digits would already
            #be present in the row, column or box), it will not result in an incomplete sudoku grid in the end.
            if substitution_row_boxes_2_done == True:
                initial_random_numbers, sudoku_grid, substitution_row_boxes_3_done = fill_row_boxes_3(initial_random_numbers, sudoku_grid, substitution_row_boxes_3_done)
            return sudoku_grid, substitution_row_boxes_3_done


        #This is the first function call for "make_sudoku()" that will be the
        #starting point in the code. Additional "make_sudoku()" are made within
        #the "while number_of_removed_digits < target_number_of_empty_cells:" below
        #when a certain amount of unsuccessful attempts to remove a number
        #from a sudoku grid have been made, hinting that a new grid might
        #need to be generated in order to remove the desired "target_number_of_empty_cells"
        #while respecting every criterion enumerated in the functions below
        #(ex: criterion_1(), criterion_2(), criterion_3, etc).

        #Only upon having set the value of "substitution_row_boxes_2_done" to "True" can the function
        #"fill_row_boxes_3" be called, and only upon having switched the value of
        #"substitution_row_boxes_2_done" to "True" can the "while substitution_row_boxes_3_done == False:"
        #be broken, which then allow for a certain number of givens or clues to be removed afterwards.
        substitution_row_boxes_2_done = False
        substitution_row_boxes_3_done = False
        while substitution_row_boxes_3_done == False:
            sudoku_grid, substitution_row_boxes_3_done = make_sudoku(substitution_row_boxes_2_done, substitution_row_boxes_3_done)
            sudoku_grid_solution = copy.deepcopy(sudoku_grid)


        #This criterion only changes the "current_number" for a zero if it is also present
        #in the the two other rows and that there are no empty cells in the current "row_box".
        def criterion_1(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            if (current_number in other_row_1 and current_number in other_row_2 and
            zero_indices_in_row_box == []):
                sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                #The "current_number" is changed for a zero if it is also present in the the two other
                #rows and there are no empty cells in the current "row_box".
                return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes the "current_number" for a zero if it is also present
        #in the two other columns, and that there are no empty cells in the other "row_boxes",
        #for that given "column_box".
        def criterion_2(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            if current_number in other_column_1 and current_number in other_column_2:
                #The range of indices at which the "column" list should be sliced for every
                #index of "column_boxes" is accessed through the "column_within_column_range"
                #dictionary.
                column_within_column_range = {0:[0,3], 1:[3,6], 2:[6,9]}
                #The "column" list is sliced at the appropriate box boundaries in order to only
                #retain the elements found within the current box.
                column_within_box = column[column_within_column_range[cell[0]][0]:column_within_column_range[cell[0]][1]]
                zero_counts_in_column_within_box = column_within_box.count(0)
                if zero_counts_in_column_within_box == 0:
                    sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                    #The "current_number" is changed for a zero if it is also present
                    #in the two other columns, and that there are no empty cells in the other "row_boxes",
                    #for that given "column_box" index.
                    return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                    other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes the "current_number" for a zero if it is a "naked single",
        #that is if every other number are present in its row, column or box.
        def criterion_3(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            set_of_digits_for_cell = set()
            for digit in row:
                if digit != 0:
                    set_of_digits_for_cell.add(digit)
            for digit in column:
                if digit != 0:
                    set_of_digits_for_cell.add(digit)
            for digit in box:
                if digit != 0:
                    set_of_digits_for_cell.add(digit)
            if (len(set_of_digits_for_cell) == 9 and sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] != 0):
                sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes "current_number" to zero if there is only one empty cell within the row,
        #and that the same digit as "current_number" can be found in the same column as the empty cell.
        def criterion_4(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            #The indices at which there are zeros in the "row" list are gathered by list comprehension
            #in the list "zero_indices_in_row".
            zero_indices_in_row = [i for i,x in enumerate(row) if x == 0]
            #If there is only one zero in the row, then the length of the list "zero_indices_in_row"
            #will be equal to one.
            if len(zero_indices_in_row) == 1:
                #The dictionary "column_position" allows to obtain the indices of ["row_box", "column_box"] for any
                #given index of the "row" list. This will allow to determine the "column_box" at which the
                #zero is found within the row. In turn, this "column_box" index will allow to slice "sudoku_grid"
                #such as to obtain that whole column ("column_with_zero").
                column_position = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
                index = zero_indices_in_row[0]
                column_with_zero = ([sudoku_grid[0][column_position[index][0]][0][column_position[index][1]]] +
                [sudoku_grid[0][column_position[index][0]][1][column_position[index][1]]] +
                [sudoku_grid[0][column_position[index][0]][2][column_position[index][1]]] +
                [sudoku_grid[1][column_position[index][0]][0][column_position[index][1]]] +
                [sudoku_grid[1][column_position[index][0]][1][column_position[index][1]]] +
                [sudoku_grid[1][column_position[index][0]][2][column_position[index][1]]] +
                [sudoku_grid[2][column_position[index][0]][0][column_position[index][1]]] +
                [sudoku_grid[2][column_position[index][0]][1][column_position[index][1]]] +
                [sudoku_grid[2][column_position[index][0]][2][column_position[index][1]]])
                #"current_number" will only be changed to zero if there is only one empty cell within the row,
                #and that the same digit as "current_number" can be found in the same column as the empty cell.
                if current_number in column_with_zero and sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] != 0:
                    sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                    return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                    other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes "current_number" to zero if there is only one empty cell within the column,
        #and that the same digit as "current_number" can be found in the same row as the empty cell.
        def criterion_5(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            #The indices at which there are zeros in the "column" list are gathered by list comprehension
            #in the list "zero_indices_in_column".
            zero_indices_in_column = [i for i,x in enumerate(column) if x == 0]
            #If there is only one zero in the column, then the length of the list "zero_indices_in_column"
            #will be equal to one.
            if len(zero_indices_in_column) == 1:
                #The dictionary "row_position" allows to obtain the indices of ["row_box", "column_box"] for any
                #given index of the "column" list. This will allow to determine the "row_box" at which the
                #zero is found within the column. In turn, this "row_box" index will allow to slice "sudoku_grid"
                #such as to obtain that whole row ("row_with_zero").
                row_position = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
                index = zero_indices_in_column[0]
                row_with_zero = (sudoku_grid[row_position[index][0]][0][row_position[index][1]] +
                sudoku_grid[row_position[index][0]][1][row_position[index][1]] +
                sudoku_grid[row_position[index][0]][2][row_position[index][1]])
                #"current_number" will only be changed to zero if there is only one empty cell within the column,
                #and that the same digit as "current_number" can be found in the same row as the empty cell.
                if current_number in row_with_zero and sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] != 0:
                    sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                    return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                    other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes "current_number" to zero if there is only one empty cell within the box,
        #which is located at a row and column other than "current_number", and the same digit as "current_number"
        #can be found either in the row or column of that empty cell.
        def criterion_6(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            #The indices at which there are zeros in the "box" list are gathered by list comprehension
            #in the list "zero_indices_in_box".
            zero_indices_in_box = [i for i,x in enumerate(box) if x == 0]
            #If there is only one zero in the box, then the length of the list "zero_indices_in_box"
            #will be equal to one.
            if len(zero_indices_in_box) == 1:
                #The dictionary "box_position" allows to obtain the indices of ["row_box", "column_box"] for any
                #given index of the flattened list "box". This will allow to determine the "row_box" at which the
                #zero is found within the box. In turn, this "row_box" index will allow to slice "sudoku_grid"
                #such as to obtain that whole row. A similar process is done with "column_box" and the column
                #in which the zero is found within the box.
                box_position = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
                index = zero_indices_in_box[0]
                row_with_zero = (sudoku_grid[cell[0]][0][box_position[index][0]] +
                sudoku_grid[cell[0]][1][box_position[index][0]] +
                sudoku_grid[cell[0]][2][box_position[index][0]])

                column_with_zero = ([sudoku_grid[0][cell[1]][0][box_position[index][1]]] +
                [sudoku_grid[0][cell[1]][1][box_position[index][1]]] +
                [sudoku_grid[0][cell[1]][2][box_position[index][1]]] +
                [sudoku_grid[1][cell[1]][0][box_position[index][1]]] +
                [sudoku_grid[1][cell[1]][1][box_position[index][1]]] +
                [sudoku_grid[1][cell[1]][2][box_position[index][1]]] +
                [sudoku_grid[2][cell[1]][0][box_position[index][1]]] +
                [sudoku_grid[2][cell[1]][1][box_position[index][1]]] +
                [sudoku_grid[2][cell[1]][2][box_position[index][1]]])

                #In order to be able to change "current_number" at position "sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]]",
                #the same number must also be observed in either the column or the row in which there is an empty cell within
                #the same box as the number under consideration. Also, the number under investigation must not be located
                #on the same column nor row as the empty cell.
                if ((current_number in row_with_zero or current_number in column_with_zero) and
                sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] != 0 and
                cell[2] != box_position[index][0] and cell[3] != box_position[index][1]):
                    sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                    return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                    other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #This criterion only changes the "current_number" for a zero if this cell is the only
        #cell within the current box that can possibly contain such a value. It proceeds by
        #elimination, assigning a value of 100 to the cells (other than the cell containing
        #"current_number") that already contain a non-zero digit. It also assigns a value of
        #100 to the cells of whose row or column contain the same number as "current_number".
        #At the end of the substitutions, "current_number" is changed for zero if every other
        #cell in the box is 100.
        def criterion_7(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
        other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column):
            #A copy ("box_100") of the list "box" is created in order to convert the
            #digits meeting the conditions explained above into 100 without disturbing
            #the original "box" list.
            box_100 = box.copy()
            #The dictionary "box_possition" allows to obtain the indices of ["row_box", "column_box"] for any
            #given index of the flattened list "box". This will be important to make sure that when cycling
            #through the "for i,number in enumerate(box)" loops, the ["row_box", "column_box"] are different
            #from those of "current_number" and to determine whether the number at index i is in one or more
            #of the following: "other_row_1", "other_row_2", "other_column_1" and "other_column_2".
            box_position = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
            #This loop finds the flattened index corresponding to the ["row_box", "column_box"] values of "current_number",
            #in order to make sure that when cycling through the "for i,number in enumerate(box)" loops, the
            #["row_box", "column_box"] are different from those of "current_number".
            box_position_current_number = 0
            for i,list in box_position.items():
                if list == [cell[2],cell[3]]:
                    box_position_current_number = i
                    break
            #Lists of the indices of "other_row_box_indices" and "other_column_box_indices" allow to find the
            #values of "row_box" and "column_box" other than the ["row_box", "column_box"] coordinate of "current_number".
            #When cycling through the "for i,number in enumerate(box)" loops, this will enable to determine whether
            #the row box at index "i" is part of "other_row_1",  "other_row_2" or the "row_box" containing "current_number".
            #A similar process is done for "column_box" and "other_column_1" and "other_column_2". Seperate
            #"for i,number in enumerate(box)" loops are required for each "other_row_1", "other_row_2", "other_column_1"
            #and "other_column_2", as otherwise only the "if i != box_position_current_number and current_number in other_row_1:"
            #would be selected, as "current_number" is in all other rows and columns.
            for i,number in enumerate(box):
                i_row_box = box_position[i][0]
                if i != box_position_current_number and current_number in other_row_1:
                    if i_row_box == other_row_box_indices[0]:
                        box_100[i] = 100
            for i,number in enumerate(box):
                i_row_box = box_position[i][0]
                if i != box_position_current_number and current_number in other_row_2:
                    if i_row_box == other_row_box_indices[1]:
                        box_100[i] = 100
            for i,number in enumerate(box):
                i_column_box = box_position[i][1]
                if i != box_position_current_number and current_number in other_column_1:
                    if i_column_box == other_column_box_indices[0]:
                        box_100[i] = 100
            for i,number in enumerate(box):
                i_column_box = box_position[i][1]
                if i != box_position_current_number and current_number in other_column_2:
                    if i_column_box == other_column_box_indices[1]:
                        box_100[i] = 100
            #As some non-zero digits may be present on the same line or column as
            #the "current_number", these would fall into one of the above if
            #statements, and so a separate loop is needed to convert the
            #remaining non-zero digits to 100.
            for i,number in enumerate(box):
                if i != box_position_current_number and number != 0:
                    box_100[i] = 100
            #At the end of the substitutions, "current_number" is changed for zero if every other
            #cell in the box is 100.
            if box_100.count(100) == 8 and sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] != 0:
                sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]] = 0
                return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)
            return (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
            other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column)

        #The initial position where the first "current_number"
        #will be analyzed to see whether it can be changed for
        #an empty cell is initialized here. As such, the values
        #of "row_boxes", "column_boxes", "row_box" and "column_box"
        #are all set to random values between 0 and 2.
        row_boxes = random.choice(range(0,3))
        column_boxes = random.choice(range(0,3))
        row_box = random.choice(range(0,3))
        column_box = random.choice(range(0,3))
        #Every time the "current_number" cannot be switched
        #to an empty cell (designated by "0") when applying
        #every one of the seven criteria under consideration
        #in the functions "criterion_1" to "criterion_7",
        #the counter "unsuccessful_function_calls" is incremented.
        #Upon reaching a value of 50, the sudoku grid is reinitialized,
        #in order to remove more digits in the next attempt.
        unsuccessful_function_calls = 0
        #These nested for loops will increment
        #"total_number_of_empty_cells" every time
        #an empty cell (containing "0") is found
        #throughout the sudoku grid.
        total_number_of_empty_cells = 0
        for row_boxes_ in sudoku_grid:
            for column_boxes_ in row_boxes_:
                for row_box_ in column_boxes_:
                    for column_box_ in row_box_:
                        if column_box_ == 0:
                            total_number_of_empty_cells += 1
        #This while loop carries on until the count of
        #"total_number_of_empty_cells" is equal to the
        #target number of empty cells specified in
        #"target_number_of_empty_cells".
        while total_number_of_empty_cells < target_number_of_empty_cells:
            #"cell" represents the list of coordinates that locates
            #the location under consideration at which the number
            #would be changed to a zero, which represents an empty
            #sudoku cell.
            cell = [row_boxes, column_boxes, row_box, column_box]
            current_number = sudoku_grid[cell[0]][cell[1]][cell[2]][cell[3]]
            #The indices for the other "row_boxes", "column_boxes", "row_box" and "column_box"
            #are stored in the lists below. These indices need to be different from those
            #of "current_number".
            other_row_boxes_indices = [row_boxes_index for row_boxes_index in [0,1,2] if row_boxes_index != cell[0]]
            other_column_boxes_indices = [column_boxes_index for column_boxes_index in [0,1,2] if column_boxes_index!= cell[1]]
            other_row_box_indices = [row_box_index for row_box_index in [0,1,2] if row_box_index != cell[2]]
            other_column_box_indices = [column_box_index for column_box_index in [0,1,2] if column_box_index!= cell[3]]

            #Flattening the list of lists representing the three rows of the box
            #(sudoku_grid[row_boxes][column_boxes]) using list comprehension
            box = [item for sublist in sudoku_grid[cell[0]][cell[1]] for item in sublist]

            #A flattened list of the digits found in a the row
            #where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            row = (sudoku_grid[cell[0]][0][cell[2]] +
            sudoku_grid[cell[0]][1][cell[2]] +
            sudoku_grid[cell[0]][2][cell[2]])

            #A flattened list of the digits found in a the column
            #where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            column = ([sudoku_grid[0][cell[1]][0][cell[3]]] +
            [sudoku_grid[0][cell[1]][1][cell[3]]] +
            [sudoku_grid[0][cell[1]][2][cell[3]]] +
            [sudoku_grid[1][cell[1]][0][cell[3]]] +
            [sudoku_grid[1][cell[1]][1][cell[3]]] +
            [sudoku_grid[1][cell[1]][2][cell[3]]] +
            [sudoku_grid[2][cell[1]][0][cell[3]]] +
            [sudoku_grid[2][cell[1]][1][cell[3]]] +
            [sudoku_grid[2][cell[1]][2][cell[3]]])

            #Every time the "current_number" cannot be switched
            #to an empty cell (designated by "0") when applying
            #every one of the seven criteria under consideration
            #in the functions "criterion_1" to "criterion_7",
            #the counter "unsuccessful_function_calls" is incremented.
            #Upon reaching a value of 50, the sudoku grid is reinitialized,
            #in order to remove more digits in the next attempt.
            #Furthermore, "sudoku_grid" is reset if thre is not at
            #least two non-zero digits per line, column and box.
            if (unsuccessful_function_calls >= 50 or box.count(0) > 7 or
            row.count(0) > 7 or column.count(0) > 7):
                row_boxes = random.choice(range(0,3))
                column_boxes = random.choice(range(0,3))
                row_box = random.choice(range(0,3))
                column_box = random.choice(range(0,3))
                unsuccessful_function_calls = 0
                total_number_of_empty_cells = 0
                substitution_row_boxes_2_done = False
                substitution_row_boxes_3_done = False
                while substitution_row_boxes_3_done == False:
                    sudoku_grid, substitution_row_boxes_3_done = make_sudoku(substitution_row_boxes_2_done, substitution_row_boxes_3_done)
                    sudoku_grid_solution = copy.deepcopy(sudoku_grid)
            #A flattened list of the digits found in a one of the other rows
            #than the one where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            other_row_1 = (sudoku_grid[cell[0]][0][other_row_box_indices[0]] +
            sudoku_grid[cell[0]][1][other_row_box_indices[0]] +
            sudoku_grid[cell[0]][2][other_row_box_indices[0]])

            #A flattened list of the digits found in a one of the other rows
            #than the one where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            other_row_2 = (sudoku_grid[cell[0]][0][other_row_box_indices[1]] +
            sudoku_grid[cell[0]][1][other_row_box_indices[1]] +
            sudoku_grid[cell[0]][2][other_row_box_indices[1]])

            #A flattened list of the digits found in one of the other columns
            #than the one where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            other_column_1 = ([sudoku_grid[0][cell[1]][0][other_column_box_indices[0]]] +
            [sudoku_grid[0][cell[1]][1][other_column_box_indices[0]]] +
            [sudoku_grid[0][cell[1]][2][other_column_box_indices[0]]] +
            [sudoku_grid[1][cell[1]][0][other_column_box_indices[0]]] +
            [sudoku_grid[1][cell[1]][1][other_column_box_indices[0]]] +
            [sudoku_grid[1][cell[1]][2][other_column_box_indices[0]]] +
            [sudoku_grid[2][cell[1]][0][other_column_box_indices[0]]] +
            [sudoku_grid[2][cell[1]][1][other_column_box_indices[0]]] +
            [sudoku_grid[2][cell[1]][2][other_column_box_indices[0]]])

            #A flattened list of the digits found in one of the other columns
            #than the one where "current_number" is found is generated by
            #concatenating slices of the "sudoku_grid" list.
            other_column_2 = ([sudoku_grid[0][cell[1]][0][other_column_box_indices[1]]] +
            [sudoku_grid[0][cell[1]][1][other_column_box_indices[1]]] +
            [sudoku_grid[0][cell[1]][2][other_column_box_indices[1]]] +
            [sudoku_grid[1][cell[1]][0][other_column_box_indices[1]]] +
            [sudoku_grid[1][cell[1]][1][other_column_box_indices[1]]] +
            [sudoku_grid[1][cell[1]][2][other_column_box_indices[1]]] +
            [sudoku_grid[2][cell[1]][0][other_column_box_indices[1]]] +
            [sudoku_grid[2][cell[1]][1][other_column_box_indices[1]]] +
            [sudoku_grid[2][cell[1]][2][other_column_box_indices[1]]])

            #If there is only one zero in the "row_box", its index is
            #obtained and the flattened list of digits found on that
            #column is generated.
            other_column_with_zero = []
            zero_indices_in_row_box = [i for i,x in enumerate(sudoku_grid[cell[0]][cell[1]][cell[2]]) if x == 0]
            if len(zero_indices_in_row_box) == 1:
                other_column_with_zero = ([sudoku_grid[0][cell[1]][0][zero_indices_in_row_box[0]]] +
                [sudoku_grid[0][cell[1]][1][zero_indices_in_row_box[0]]] +
                [sudoku_grid[0][cell[1]][2][zero_indices_in_row_box[0]]] +
                [sudoku_grid[1][cell[1]][0][zero_indices_in_row_box[0]]] +
                [sudoku_grid[1][cell[1]][1][zero_indices_in_row_box[0]]] +
                [sudoku_grid[1][cell[1]][2][zero_indices_in_row_box[0]]] +
                [sudoku_grid[2][cell[1]][0][zero_indices_in_row_box[0]]] +
                [sudoku_grid[2][cell[1]][1][zero_indices_in_row_box[0]]] +
                [sudoku_grid[2][cell[1]][2][zero_indices_in_row_box[0]]])

            #If there is only one zero in the part of a column that is
            #circumscribed to a given box, its index is obtained and
            #the flattened list of digits found on that row is generated.
            other_row_with_zero = []
            box_column = ([sudoku_grid[cell[0]][cell[1]][0][cell[3]],
            sudoku_grid[cell[0]][cell[1]][1][cell[3]], sudoku_grid[cell[0]][cell[1]][2][cell[3]]])
            zero_indices_in_box_column = [i for i,x in enumerate(box_column) if x == 0]
            if len(zero_indices_in_box_column) == 1:
                other_row_with_zero = (sudoku_grid[cell[0]][0][zero_indices_in_box_column[0]] +
                sudoku_grid[cell[0]][1][zero_indices_in_box_column[0]] +
                sudoku_grid[cell[0]][2][zero_indices_in_box_column[0]])

            #The number of empty cells (designated by zeros) in the sudoku grid
            #is stored in "number_of_removed_digits_before_function_call".
            #After running the functions, the updated value of "total_number_of_empty_cells"
            #will be checked against that of "number_of_removed_digits_before_function_call".
            #If these two values are equal, it means that no substitution of a digit for
            #zero has happened despite cycling through all seven "criterion" functions
            #and the value of "unsuccessful_function_calls" is then incremented.
            number_of_removed_digits_before_function_call = total_number_of_empty_cells

            #The seven functions "criterion_1" to "criterion_7" are called in random
            #sequence for every "current_number" under investigation, to ensure
            #maximal variability in between puzzles.
            for i in random.sample(range(7), 7):
                (sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column) =  (
                eval("criterion_" + str(i+1))(sudoku_grid, cell, current_number, box, row, other_row_1, other_row_2, column, other_column_1,
                other_column_2, other_row_box_indices, zero_indices_in_row_box, other_column_box_indices, zero_indices_in_box_column))

            #These nested for loops will increment
            #"total_number_of_empty_cells" every time
            #an empty cell (containing "0") is found
            #throughout the sudoku grid.
            total_number_of_empty_cells = 0
            for row_boxes_ in sudoku_grid:
                for column_boxes_ in row_boxes_:
                    for row_box_ in column_boxes_:
                        for column_box_ in row_box_:
                            if column_box_ == 0:
                                total_number_of_empty_cells += 1

            #The number of empty cells (designated by zeros) in the sudoku grid
            #is stored in "number_of_removed_digits_before_function_call".
            #After running the functions, the updated value of "total_number_of_empty_cells"
            #will be checked against that of "number_of_removed_digits_before_function_call".
            #If these two values are equal, it means that no substitution of a digit for
            #zero has happened despite cycling through all seven "criterion" functions
            #and the value of "unsuccessful_function_calls" is then incremented.
            if number_of_removed_digits_before_function_call == total_number_of_empty_cells:
                unsuccessful_function_calls += 1
            #If a digit has been changed to zero, then the "unsuccessful_function_calls"
            #variable is reinitialized to 0, as there doesn't yet apprear to be ongoing issues
            #with assigning empty cells to the sudoku grid.
            elif number_of_removed_digits_before_function_call < total_number_of_empty_cells:
                unsuccessful_function_calls = 0

            #The coordinates for the next "current_number"
            #are determined. The sudoku grid are screened
            #sequentially, and the coordinates within those
            #boxes are randomized. Proceeding box by box
            #helps ensure that the empty cells are more
            #evenly distributed in the grid.

            #If the box isn't the last box in a given row of
            #boxes, the variable "column_boxes" is incremented
            #and the next "current_number" will be found in the
            #following box.
            if column_boxes < 2:
                column_boxes += 1
                row_box = random.choice(range(0,3))
                column_box = random.choice(range(0,3))
            #If the current box is situated at the end of
            #a row of boxes and that the row of boxes is
            #not the last row of boxes, the variable
            #"row_boxes" is incremented and "column_boxes"
            #is reset to 0 to move on to the first box
            #of the next row of boxes.
            elif column_boxes == 2 and row_boxes < 2:
                row_boxes += 1
                column_boxes = 0
                row_box = random.choice(range(0,3))
                column_box = random.choice(range(0,3))
            #If the current box is the last box in
            #the sudoku grid, then both "row_boxes"
            #and "column_boxes" are reset to 0, so that
            #the next "current_number" will be found in
            #the first box of the sudoku grid.
            elif column_boxes == 2 and row_boxes == 2:
                row_boxes = 0
                column_boxes = 0
                row_box = random.choice(range(0,3))
                column_box = random.choice(range(0,3))

        #These nested for loops will add each
        #digit of the "sudoku_grid" list to the
        #empty string "flattened_sudoku_grid_string".
        #The "column_boxes" ("k") are cycled before
        #incrementing the "row_boxes" ("j") to ensure
        #that the data is properly transposed into
        #sudoku format. Why didn't I start with
        #a silt formatted in sudoku format to start with?
        #Good question!
        flattened_sudoku_grid_string = ""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    flattened_sudoku_grid_string += (str(sudoku_grid[i][k][j][0]) + " " +
                    str(sudoku_grid[i][k][j][1]) + " " + str(sudoku_grid[i][k][j][2]) + " ")


        #These nested for loops will add each
        #digit of the "sudoku_grid_solution" list to the
        #empty string "flattened_sudoku_grid_solution_string".
        #The "column_boxes" ("k") are cycled before
        #incrementing the "row_boxes" ("j") to ensure
        #that the data is properly transposed into
        #sudoku format. Why didn't I start with
        #a silt formatted in sudoku format to start with?
        #Good question!
        flattened_sudoku_grid_solution_string = ""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    flattened_sudoku_grid_solution_string += (str(sudoku_grid_solution[i][k][j][0]) + " " +
                    str(sudoku_grid_solution[i][k][j][1]) + " " + str(sudoku_grid_solution[i][k][j][2]) + " ")


        #The "braille_digits" dictionary maps the digits in string form from 0 to 9 to their braille equivalents
        #(preceded by the numeric symbol, except for 0, which maps to two successive empty braille cells, for empty
        #sudoku cells)
        braille_digits = {"0":"⠀⠀", "1":"⠼⠁", "2":"⠼⠃", "3":"⠼⠉", "4":"⠼⠙", "5":"⠼⠑", "6":"⠼⠋", "7":"⠼⠛", "8":"⠼⠓", "9":"⠼⠊"}

        #Transcribing the string "flattened_sudoku_grid_string" into braille.
        mapping_table_braille_digits_sudoku_grid = flattened_sudoku_grid_string.maketrans(braille_digits)
        flattened_sudoku_grid_braille = flattened_sudoku_grid_string.translate(mapping_table_braille_digits_sudoku_grid).split()

        #Transcribing the string "flattened_sudoku_grid_solution_string" into braille.
        mapping_table_braille_digits_sudoku_grid_solution = flattened_sudoku_grid_solution_string.maketrans(braille_digits)
        flattened_sudoku_grid_solution_braille = flattened_sudoku_grid_solution_string.translate(mapping_table_braille_digits_sudoku_grid_solution).split()

        cwd = os.getcwd()

        #If the "Brailoku Sudoku Puzzles" folder doesn't already
        #exist in the working folder, it will be created.
        #Within it, the "Portable Embosser Format (PEF)" and
        #"Braille Ready Format (BRF)" subfolders will be created
        #as well, if not already present.
        if not os.path.exists(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Portable Embosser Format (PEF)")):
            os.makedirs(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Portable Embosser Format (PEF)"))
        if not os.path.exists(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Braille Ready Format (BRF)")):
            os.makedirs(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Braille Ready Format (BRF)"))

        #Compiles the list of Portable Embosser format (".pef") and Braille Ready Format (".brf") files
        #in the respective subfolder within the "Brailloku Sudoku Puzzles" subfolder in the working folder.
        for _, dirnames, filenames in os.walk(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Portable Embosser Format (PEF)")):
            sudoku_pef_files = [filename for filename in filenames if filename[-4:] == ".pef"]
        for _, dirnames, filenames in os.walk(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Braille Ready Format (BRF)")):
            sudoku_brf_files = [filename for filename in filenames if filename[-4:] == ".brf"]

        #The digit of every file is extracted from its name and the maximum file number is determined for
        #the PEF and/or BRF files, if the "sudoku_pef_files" and/or "sudoku_brf_files" list isn't empty,
        #respectively. The starting splicing index of the "filename" corresponds to the index right after
        #the hyphen ("Brailloku Sudoku Puzzle number-"), and the filename is spliced up to the file extension,
        #exclusively.
        largest_sudoku_pef_file_number = []
        largest_sudoku_brf_file_number = []
        if sudoku_pef_files != []:
            largest_sudoku_pef_file_number = max([int(filename[31:-4]) for filename in sudoku_pef_files])
        if sudoku_brf_files != []:
            largest_sudoku_brf_file_number = max([int(filename[31:-4]) for filename in sudoku_brf_files])

        #If both lists "sudoku_pef_files" and "sudoku_brf_files" weren't empty,
        #then the maximum between "largest_sudoku_pef_file_number" and "largest_sudoku_brf_file_number"
        #is determined. If only one of "sudoku_pef_files" or "sudoku_brf_files"
        #wasn't empty, then the largest sudoku file number for that file extension
        #is used as the "number_of_sudoku_files" in order to pick up where the last
        #sudoku problem was generated. If both "sudoku_pef_files" and "sudoku_brf_files"
        #are empty lists, "number_of_sudoku_files" is initialized at zero.
        if sudoku_pef_files != [] and sudoku_brf_files != []:
            number_of_sudoku_files = max(largest_sudoku_pef_file_number, largest_sudoku_brf_file_number)
        elif sudoku_pef_files != [] and sudoku_brf_files == []:
            number_of_sudoku_files = largest_sudoku_pef_file_number
        elif sudoku_pef_files == [] and sudoku_brf_files != []:
            number_of_sudoku_files = largest_sudoku_brf_file_number
        elif sudoku_pef_files == [] and sudoku_brf_files == []:
            number_of_sudoku_files = 0

        #The dictionary "braille_numbers" is used to transcribe the string versions of "number_of_sudoku_files"
        #and "total_number_of_empty_cells" into ASCII.
        braille_numbers = {"0":"⠚", "1":"⠁", "2":"⠃", "3":"⠉", "4":"⠙", "5":"⠑", "6":"⠋", "7":"⠛", "8":"⠓", "9":"⠊"}
        current_file_number = number_of_sudoku_files + 1

        #The "current_file_number_braille" string is initialized with the braille numeric symbol "⠼",
        #and every braille digit equivalent of each character constituting the string version of
        #"current_file_number".
        current_file_number_braille = "⠼"
        for digit in str(current_file_number):
            current_file_number_braille += braille_numbers[digit]

        current_file_name = "Brailloku Sudoku Puzzle number-" + str(current_file_number)

        #The "number_of_empty_cells_braille" string is initialized with the braille numeric symbol "⠼",
        #and every braille digit equivalent of each character constituting the string version of
        #"total_number_of_empty_cells".
        number_of_empty_cells_braille = "⠼"
        for digit in str(total_number_of_empty_cells):
            number_of_empty_cells_braille += braille_numbers[digit]


        #PEF file is assembled by including opening and closing volume, section,
        #page and row tags, with the sudoku puzzle and solution sandwitched in between.
        #The user can opt for a truncated version of the sudoku grid
        #excluding some of the header text and the topmost and lowest horizontal
        #delimiters, bringing the number of lines per page down to 18 lines, which
        #allows for embossing on A4 paper in landscape mode. They would then enter
        #"short" as an additional argument after the Python call and the variable
        #"short" (initialized to "False"), would then be set to "True".
        pef_file_name = current_file_name +  ".pef"
        with open(os.path.join(cwd, "Brailloku Sudoku Puzzles/Portable Embosser Format (PEF)", pef_file_name), "a+", encoding="utf-8") as pef_file:
            pef_file.write('<?xml version="1.0" encoding="UTF-8"?>' +
            '\n<pef version="2008-1" xmlns="http://www.daisy.org/ns/2008/pef">\n\t<head>' +
            '\n\t\t<meta xmlns:dc="http://purl.org/dc/elements/1.1/">' +
			'\n\t\t\t<dc:format>application/x-pef+xml</dc:format>' +
			'\n\t\t\t<dc:identifier>org.pef-format.00002</dc:identifier>\n\t\t</meta>')
            if short == True:
                pef_file.write('\n\t</head>\n\t<body>\n\t\t<volume cols="30" rows="18" rowgap="0" duplex="false">' +
                '\n\t\t\t<section>\n\t\t\t\t<page>\n\t\t\t\t\t<row>⠠⠃⠗⠁⠊⠇⠇⠕⠅⠥</row>')
            elif short == False:
                pef_file.write('\n\t</head>\n\t<body>\n\t\t<volume cols="30" rows="22" rowgap="0" duplex="false">' +
                '\n\t\t\t<section>\n\t\t\t\t<page>\n\t\t\t\t\t<row>⠠⠃⠗⠁⠊⠇⠇⠕⠅⠥</row>' +
                '\n\t\t\t\t\t<row>⠠⠎⠥⠙⠕⠅⠥⠀⠠⠏⠥⠵⠵⠇⠑⠀' + current_file_number_braille +
                '</row>\n\t\t\t\t\t<row>⠠⠝⠥⠍⠀⠃⠻⠀⠷⠀⠑⠍⠏⠞⠽⠀⠉⠑⠇⠇⠎⠒⠀' +
                number_of_empty_cells_braille +'</row>' + '\n\t\t\t\t\t<row>' + 29*"⠤" + "⠄" + "</row>")
            #For each of the nine sudoku lines, for every one of the 9 digits on the line,
            #the braille digit is preceded by a vertical delimiter ("⠇") in between sudoku cells.
            #The solution is added to the next page (after a page break).
            for i in range(9):
                pef_file.write("\n\t\t\t\t\t<row>")
                for j in range(9):
                    next_digit = flattened_sudoku_grid_braille.pop(0)
                    #A "⠿" followed by an empty braille cell will be used to delimitate the different
                    #boxes on the vertical axis, so these characters need to be included before the
                    #"next_digit" only if "j" is either 3 or 6 (although these are actually the 4th
                    #and 7th cells of every line, this is ok because we are adding the delimiter prior
                    #to the "next_digit"). The "j !=0" condition is added to the "if" statement to avoid
                    #including a "⠿⠀" divider before the first number of the row, as 0%3 == 0).
                    if j != 0 and j%3 == 0:
                        pef_file.write("⠿⠀" + next_digit)
                    elif j == 0 or j%3 != 0:
                        pef_file.write("⠇" + next_digit)
                #As the horizontal dividers are placed after the rows (unlike the vertical ones, which were added
                #before "next_digit"), we are actually checking whether "(i+1)%3 == 0". The "i != 8" condition is
                #added to the "if" statement to avoid including the ""⠷⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠇"
                #horizontal divider after the last line, as "8+1%3 == 0".
                if i != 8 and (i+1)%3 == 0:
                    pef_file.write("⠇</row>\n\t\t\t\t\t<row>" + "⠷⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠇</row>")
                elif short == True and i == 8:
                    pef_file.write("⠇</row>")
                elif (short == False and i == 8) or (i != 8 and (i+1)%3 != 0):
                    pef_file.write("⠇</row>\n\t\t\t\t\t<row>" + "⠧⠤⠤⠧⠤⠤⠧⠤⠤⠿⠤⠤⠤⠧⠤⠤⠧⠤⠤⠿⠤⠤⠤⠧⠤⠤⠧⠤⠤⠇</row>")

            pef_file.write("\n\t\t\t\t</page>\n\t\t\t\t<page>")
            if short == True:
                pef_file.write("\n\t\t\t\t\t<row>⠠⠃⠗⠁⠊⠇⠇⠕⠅⠥</row>")
            elif short == False:
                pef_file.write("\n\t\t\t\t\t<row>⠠⠃⠗⠁⠊⠇⠇⠕⠅⠥</row>" +
                "\n\t\t\t\t\t<row>⠠⠎⠕⠇⠥⠰⠝⠀⠿⠀⠠⠏⠥⠵⠵⠇⠑⠀" + current_file_number_braille +
                "</row>\n\t\t\t\t\t<row>⠠⠝⠥⠍⠀⠃⠻⠀⠷⠀⠑⠍⠏⠞⠽⠀⠉⠑⠇⠇⠎⠒⠀" + number_of_empty_cells_braille +
                "</row>\n\t\t\t\t\t<row>" + 29*"⠤" + "⠄" + "</row>")
            for i in range(9):
                pef_file.write("\n\t\t\t\t\t<row>")
                for j in range(9):
                    next_digit = flattened_sudoku_grid_solution_braille.pop(0)
                    if j != 0 and j%3 == 0:
                        pef_file.write("⠿⠀" + next_digit)
                    elif j == 0 or j%3 != 0:
                        pef_file.write("⠇" + next_digit)
                if i != 8 and (i+1)%3 == 0:
                    pef_file.write("⠇</row>\n\t\t\t\t\t<row>" + "⠷⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠿⠶⠶⠶⠷⠶⠶⠷⠶⠶⠇</row>")
                elif short == True and i == 8:
                    pef_file.write("⠇</row>")
                elif(short == False and i == 8) or (i != 8 and (i+1)%3 != 0):
                    pef_file.write("⠇</row>\n\t\t\t\t\t<row>" + "⠧⠤⠤⠧⠤⠤⠧⠤⠤⠿⠤⠤⠤⠧⠤⠤⠧⠤⠤⠿⠤⠤⠤⠧⠤⠤⠧⠤⠤⠇</row>")
            pef_file.write("\n\t\t\t\t</page>\n\t\t\t</section>\n\t\t</volume>\n\t</body>\n</pef>")

            #In this section the Braille Ready Format (BRF) files will be created.
            #The "ASCII_digits" dictionary maps the digits from 0 to 9 to their ASCII equivalents
            #(preceded by the numeric symbol ("#"), except for 0, which maps to two successive spaces,
            #for empty sudoku cells)
            ASCII_digits = {0:"  ", 1:"#A", 2:"#B", 3:"#C", 4:"#D", 5:"#E", 6:"#F", 7:"#G", 8:"#H", 9:"#I"}

            #The dictionary "ASCII_numbers" is used to transcribe the string versions of "number_of_sudoku_files"
            #and "total_number_of_empty_cells" into ASCII.
            ASCII_numbers = {"0":"J", "1":"A", "2":"B", "3":"C", "4":"D", "5":"E", "6":"F", "7":"G", "8":"H", "9":"I"}

            #The list "flattened_sudoku_grid_list" is created by splitting
            #the sting "flattened_sudoku_grid_string" along every space.
            #The other list "flattened_sudoku_grid_ASCII" is populated
            #with the ASCII equivalents (preceded by a "#" ASCII numeric
            #indicator) of every digit found in the "flattened_sudoku_grid_list".
            flattened_sudoku_grid_list = flattened_sudoku_grid_string.split()
            flattened_sudoku_grid_ASCII = []
            for i in range(len(flattened_sudoku_grid_list)):
                #Since the list "flattened_sudoku_grid_list" contains string
                #versions if the sudoku grid digits (as it was built by splitting a string)
                #"j" needs to be converted to a string in order to be compared with
                #"flattened_sudoku_grid_list[i]". If these two values match, then it means
                #that the current index of the dictionary "ASCII_digits" corresponds to the
                #current digit at index "i" of the "flattened_sudoku_grid_list".
                for j in range(len(ASCII_digits)):
                    if str(j) == flattened_sudoku_grid_list[i]:
                        flattened_sudoku_grid_ASCII.append(ASCII_digits[j])

            #A similar approach as above is done for the sudoku grid solution.
            flattened_sudoku_grid_solution_list = flattened_sudoku_grid_solution_string.split()
            flattened_sudoku_grid_solution_ASCII = []
            for i in range(len(flattened_sudoku_grid_solution_list)):
                for j in range(len(ASCII_digits)):
                    if str(j) == flattened_sudoku_grid_solution_list[i]:
                        flattened_sudoku_grid_solution_ASCII.append(ASCII_digits[j])


            #The "current_file_number_ASCII" string is initialized as the ASCII
            #equivalent of a numberic braille simbol ("#"), followed by every ASCII
            #equivalent of each braille character constituting the
            #string version of "current_file_number".
            current_file_number_ASCII = "#"
            for digit in str(current_file_number):
                current_file_number_ASCII += ASCII_numbers[digit]

            #The "number_of_empty_cells_ASCII" string is initialized as the ASCII
            #equivalent of a numberic braille simbol ("#"), followed by
            #every ASCII equivalent of each braille character constituting the
            #string version of "total_number_of_empty_cells".
            number_of_empty_cells_ASCII = "#"
            for digit in str(total_number_of_empty_cells):
                number_of_empty_cells_ASCII += ASCII_numbers[digit]

            #A BRF file is assembled here.
            #The user can opt for a truncated version of the sudoku grid
            #excluding some of the header text and the topmost and lowest horizontal
            #delimiters, bringing the number of lines per page down to 18 lines, which
            #allows for embossing on A4 paper in landscape mode. They would then enter
            #"short" as an additional argument after the Python call and the variable
            #"short" (initialized to "False"), would then be set to "True".
            brf_file_name = current_file_name + ".brf"
            with open(os.path.join(cwd, "Brailloku Sudoku Puzzles", "Braille Ready Format (BRF)", brf_file_name), "a+") as brf_file:
                brf_file.write(",BRAILLOKU")
                if short == False:
                    brf_file.write("\n,SUDOKU ,PUZZLE " + current_file_number_ASCII)
                    brf_file.write("\n,NUMB] ( EMPTY CELLS3 " + number_of_empty_cells_ASCII)
                    brf_file.write("\n" + 29*"-" + "'")

                #For each of the nine sudoku lines, for every one of the 9 digits on the line,
                #the braille digit is preceded by a vertical delimiter ("⠇") in between sudoku cells.
                #The solution is added to the next page (after a page break).
                for i in range(9):
                    brf_file.write("\n")
                    for j in range(9):
                        next_digit = flattened_sudoku_grid_ASCII.pop(0)
                        #A "=" followed by a space will be used to delimitate the different
                        #boxes on the vertical axis, so these characters need to be included before the
                        #"next_digit" only if "j" is either 3 or 6 (although these are actually the 4th
                        #and 7th cells of every line, this is ok because we are adding the delimiter prior
                        #to the "next_digit"). The "j !=0" condition is added to the "if" statement to avoid
                        #including a "= " divider before the first number of the row, as 0%3 == 0).
                        if j != 0 and j%3 == 0:
                            brf_file.write("= " + next_digit)
                        elif j == 0 or j%3 != 0:
                            brf_file.write("L" + next_digit)
                    #As the horizontal dividers are placed after the rows (unlike the vertical ones, which were added
                    #before "next_digit"), we are actually checking whether "(i+1)%3 == 0". The "i != 8" condition is
                    #added to the "if" statement to avoid including "(77(77(77=777(77(77=777(77(77L"
                    #horizontal divider after the last line, as "8+1%3 == 0".
                    if i != 8 and (i+1)%3 == 0:
                        brf_file.write("L\n" + "(77(77(77=777(77(77=777(77(77L")
                    elif short == True and i == 8:
                        brf_file.write("L")
                    elif(short == False and i == 8) or (i != 8 and (i+1)%3 != 0):
                        brf_file.write("L\n" + "V--V--V--=---V--V--=---V--V--L")

                brf_file.write("\f,BRAILLOKU")
                if short == False:
                    brf_file.write("\n,SUDOKU ,PUZZLE " + current_file_number_ASCII)
                    brf_file.write("\n,NUMB] ( EMPTY CELLS3 " + number_of_empty_cells_ASCII)
                    brf_file.write("\n" + 29*"-" + "'")
                for i in range(9):
                    brf_file.write("\n")
                    for j in range(9):
                        next_digit = flattened_sudoku_grid_solution_ASCII.pop(0)
                        if j != 0 and j%3 == 0:
                            brf_file.write("= " + next_digit)
                        elif j == 0 or j%3 != 0:
                            brf_file.write("L" + next_digit)
                    if i != 8 and (i+1)%3 == 0:
                        brf_file.write("L\n" + "(77(77(77=777(77(77=777(77(77L")
                    elif short == True and i == 8:
                        brf_file.write("L")
                    elif(short == False and i == 8) or (i != 8 and (i+1)%3 != 0):
                        brf_file.write("L\n" + "V--V--V--=---V--V--=---V--V--L")

            bar()

if number_of_puzzles == 1:
    print('\nThe BRF and PEF files "' + current_file_name + '" containing ' + str(total_number_of_empty_cells) + ' empty cells were created successfully!\n')
elif number_of_puzzles > 1:
    print('\nYour ' + str(number_of_puzzles) + ' sudoku puzzles have been created successfully!')
