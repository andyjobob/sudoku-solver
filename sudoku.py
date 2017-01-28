import sys
import os
import re
import math
import csv

################################################################################
### Constants
################################################################################
MIN_ROW = 1
MAX_ROW = 9
MIN_COL = 1
MAX_COL = 9

ROWS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
COLS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
GROUPS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Contains rows in given group
GROUP_ROWS = dict((i, []) for i in GROUPS)
GROUP_ROWS[1] = [1, 2, 3]
GROUP_ROWS[2] = [1, 2, 3]
GROUP_ROWS[3] = [1, 2, 3]
GROUP_ROWS[4] = [4, 5, 6]
GROUP_ROWS[5] = [4, 5, 6]
GROUP_ROWS[6] = [4, 5, 6]
GROUP_ROWS[7] = [7, 8, 9]
GROUP_ROWS[8] = [7, 8, 9]
GROUP_ROWS[9] = [7, 8, 9]

# Contains rows NOT in given group
GROUP_NOT_ROWS = dict((i, []) for i in GROUPS)
GROUP_NOT_ROWS[1] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_ROWS[2] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_ROWS[3] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_ROWS[4] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_ROWS[5] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_ROWS[6] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_ROWS[7] = [1, 2, 3, 4, 5, 6]
GROUP_NOT_ROWS[8] = [1, 2, 3, 4, 5, 6]
GROUP_NOT_ROWS[9] = [1, 2, 3, 4, 5, 6]

# Contains columns in given group
GROUP_COLS = dict((i, []) for i in GROUPS)
GROUP_COLS[1] = [1, 2, 3]
GROUP_COLS[2] = [4, 5, 6]
GROUP_COLS[3] = [7, 8, 9]
GROUP_COLS[4] = [1, 2, 3]
GROUP_COLS[5] = [4, 5, 6]
GROUP_COLS[6] = [7, 8, 9]
GROUP_COLS[7] = [1, 2, 3]
GROUP_COLS[8] = [4, 5, 6]
GROUP_COLS[9] = [7, 8, 9]

# Contains columns NOT in given group
GROUP_NOT_COLS = dict((i, []) for i in GROUPS)
GROUP_NOT_COLS[1] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_COLS[2] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_COLS[3] = [1, 2, 3, 4, 5, 6]
GROUP_NOT_COLS[4] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_COLS[5] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_COLS[6] = [1, 2, 3, 4, 5, 6]
GROUP_NOT_COLS[7] = [4, 5, 6, 7, 8, 9]
GROUP_NOT_COLS[8] = [1, 2, 3, 7, 8, 9]
GROUP_NOT_COLS[9] = [1, 2, 3, 4, 5, 6]

def calc_group(col, row):
    #if row >= 1 and row <= 3:
    row_offset = (row - 1) // 3
    col_offset = (col - 1) // 3
    group = col_offset + (3 * row_offset) + 1
    return group


################################################################################
# Function print_possbile_numbers
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def print_possible_numbers():
    print_string = ""

    for row in ROWS:
        if row == 1:
            print_string += " ++===C1===+==C2===+===C3===++===C4===+==C5===+===C6===++===C7===+==C8===+===C9===++\n"
            print_string += " ##                         ##                         ##                         ##\n"
        elif row == 4 or row == 7:
            print_string += " ##                         ##                         ##                         ##\n"
            print_string += " ++===C1===+==C2===+===C3===++===C4===+==C5===+===C6===++===C7===+==C8===+===C9===++\n"
            print_string += " ##                         ##                         ##                         ##\n"
        else:
            print_string += " ++--------+-------+--------++--------+-------+--------++--------+-------+--------++\n"

        for sub_row in range(0,3):
            if sub_row == 1:
                print_string += " R%d " % row
            else:
                print_string += " ## "

            for col in COLS:
                for sub_col in range((sub_row * 3) + 1,(sub_row * 3) + 4):
                    match_found = False
                    for j in possible_numbers[col][row]:
                        if sub_col == j:
                            match_found = True

                    if match_found:
                        print_string += " " + format(sub_col)
                    else:
                        print_string += "  "

                if col == 3 or col == 6 or col == 9:
                    if sub_row == 1:
                        print_string += "  R%d " % row
                    else:
                        print_string += "  ## "
                    #print_string += "  ## "
                else:
                    print_string += " |"

            print_string += "\n"

    print_string += " ##                         ##                         ##                         ##\n"
    print_string += " ++===C1===+==C2===+===C3===++===C4===+==C5===+===C6===++===C7===+==C8===+===C9===++\n"
    print(print_string)


################################################################################
# Function clean_possible_numbers
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def clean_possible_numbers():
    result = False
    clean = False
    while not clean:
        clean = True
        #print("  Cleaning")
        for col in COLS:
            for row in ROWS:
                if len(possible_numbers[col][row]) == 1:
                    single_number = possible_numbers[col][row][0]

                    # Clean all columns in current 'row'
                    for i in COLS:
                        if i != col:
                            if possible_numbers[i][row].count(single_number) == 1:
                                possible_numbers[i][row].remove(single_number)
                                clean = False
                                result = True
                                if len(possible_numbers[i][row]) == 1:
                                    print("  Clean   Rows: (%d, %d) = %d" % (i, row, possible_numbers[i][row][0]))


                    # Clean all rows in current 'col'
                    for j in ROWS:
                        if j != row:
                            if possible_numbers[col][j].count(single_number) == 1:
                                possible_numbers[col][j].remove(single_number)
                                clean = False
                                result = True
                                if len(possible_numbers[col][j]) == 1:
                                    print("  Clean   Cols: (%d, %d) = %d" % (col, j, possible_numbers[col][j][0]))


                    # Clean all boxes in current group
                    group = calc_group(col, row)
                    for i in GROUP_COLS[group]:
                        for j in GROUP_ROWS[group]:
                            if not (i == col and j == row):
                                if possible_numbers[i][j].count(single_number) == 1:
                                    possible_numbers[i][j].remove(single_number)
                                    clean = False
                                    result = True
                                    if len(possible_numbers[i][j]) == 1:
                                        print("  Clean   Grps: (%d, %d) = %d" % (i, j, possible_numbers[i][j][0]))


    return result


################################################################################
# Function analyze_cols
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def analyze_cols():
    # Run only when possible numbers is fully clean
    result = False

    for col in COLS:
        for row in ROWS:
            if len(possible_numbers[col][row]) != 1:
                match_found = True
                for number in possible_numbers[col][row]:
                    match_found = False
                    for j in ROWS:
                        if j != row:
                            if possible_numbers[col][j].count(number) == 1:
                                match_found = True
                                break

                    if not match_found:
                        match_number = number
                        break

                if not match_found:
                    possible_numbers[col][row] = [match_number]
                    print("  Analyze Cols: (%d, %d) = %d" % (col, row, match_number))
                    result = True

    return result


################################################################################
# Function analyze_rows
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def analyze_rows():
    # Run only when possible numbers is fully clean
    result = False

    for col in COLS:
        for row in ROWS:
            if len(possible_numbers[col][row]) != 1:
                match_found = True
                for number in possible_numbers[col][row]:
                    match_found = False
                    for i in COLS:
                        if i != col:
                            if possible_numbers[i][row].count(number) == 1:
                                match_found = True
                                break

                    if not match_found:
                        match_number = number
                        break

                if not match_found:
                    possible_numbers[col][row] = [match_number]
                    print("  Analyze Rows: (%d, %d) = %d" % (col, row, match_number))
                    result = True

    return result


################################################################################
# Function analyze_groups
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def analyze_groups():
    # Run only when possible numbers is fully clean
    result = False

    for col in COLS:
        for row in ROWS:
            if len(possible_numbers[col][row]) != 1:
                match_found = True
                group = calc_group(col, row)
                for number in possible_numbers[col][row]:
                    match_found = False
                    for i in GROUP_COLS[group]:
                        for j in GROUP_ROWS[group]:
                            if not (i == col and j == row):
                                # When match is found break out of group row loop
                                if possible_numbers[i][j].count(number) == 1:
                                    match_found = True
                                    break

                        # When match is found break out of group column loop as well
                        if match_found:
                            break

                    # if no match is found after looping through all group boxes,
                    # then we found a solution number and break out of number loop
                    if not match_found:
                        found_number = number
                        break

                # Update possible numbers with solution number found
                if not match_found:
                    possible_numbers[col][row] = [found_number]
                    print("  Analyze Grps: (%d, %d) = %d" % (col, row, found_number))
                    result = True

    return result


################################################################################
# Function analyze_box_cols_rows
#
# Description:
#
#  Arguments:
#
#  Return Values:
#
################################################################################
def analyze_box_cols_rows():
    # Run only when possible numbers is fully clean and after analyze columns and rows
    result = False

    for col in COLS:
        for row in ROWS:
            if len(possible_numbers[col][row]) != 1:
                match_found = True
                group = calc_group(col, row)
                for number in possible_numbers[col][row]:
                    # Check Column
                    match_found = False
                    for j in GROUP_NOT_ROWS[group]:
                        if possible_numbers[col][j].count(number) == 1:
                            match_found = True
                            break

                    # If no match is found after looping through all not group row boxes,
                    # then we found a number we can eliminate form othe boxes in the group
                    if not match_found:
                        for i in GROUP_COLS[group]:
                            for j in GROUP_ROWS[group]:
                                if not (i == col):
                                    if possible_numbers[i][j].count(number) == 1:
                                        possible_numbers[i][j].remove(number)
                                        print("  Analyze BoxCols, Group %d, Col %d must contain %d, removing from (%d, %d)" % (group, col, number, i, j))
                                        if len(possible_numbers[i][j]) == 1:
                                            print("  Analyze BoxCols: (%d, %d) = %d" % (i, j, possible_numbers[i][j][0]))

                                        result = True

                    # Check Row
                    match_found = False
                    for i in GROUP_NOT_COLS[group]:
                        if possible_numbers[i][row].count(number) == 1:
                            match_found = True
                            break

                    # If no match is found after looping through all not group row boxes,
                    # then we found a number we can eliminate form othe boxes in the group
                    if not match_found:
                        for i in GROUP_COLS[group]:
                            for j in GROUP_ROWS[group]:
                                if not (j == row):
                                    if possible_numbers[i][j].count(number) == 1:
                                        possible_numbers[i][j].remove(number)
                                        print("  Analyze BoxRows, Group %d, Row %d must contain %d, removing from (%d, %d)" % (group, row, number, i, j))
                                        if len(possible_numbers[i][j]) == 1:
                                            print("  Analyze BoxRows: (%d, %d) = %d" % (i, j, possible_numbers[i][j][0]))
                                        result = True

    return result


################################################################################
### Main
################################################################################
# Process input arguments
if (len(sys.argv) != 2):
    print("Usage: python sudoku.py <INPUT.csv>")
    sys.exit()

input_file = str(sys.argv[1])

possible_numbers = dict((i, dict((j, []) for j in ROWS)) for i in COLS)

for i in COLS:
    for j in ROWS:
        possible_numbers[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

with open(input_file, 'r') as input_fh:
    input_matrix = csv.reader(input_fh)
    j = 1
    for row in input_matrix:
        #print(row)
        if len(row) == 9:
            for i in range(1, 10):
                if (int(row[i - 1]) >= 1) and (int(row[i - 1]) <= 9):
                    dummy_list = []
                    dummy_list.append(int(row[i - 1]))
                    possible_numbers[i][j] = dummy_list
                elif int(row[i - 1]) != 0:
                    print("Invalid data on row ", j, ": ", row)
                    sys.exit()
        else:
            print("Invalid data on row ", j, ": ", row)
            sys.exit()

        j += 1

    if j != 10:
        print("Invalid number of rows: ", j - 1)
        sys.exit()

# Worlds hardest sudoku
#possible_numbers[1][1] = [8]
#possible_numbers[2][3] = [7]
#possible_numbers[2][4] = [5]
#possible_numbers[2][9] = [9]
#possible_numbers[3][2] = [3]
#possible_numbers[3][7] = [1]
#possible_numbers[3][8] = [8]
#possible_numbers[4][2] = [6]
#possible_numbers[4][6] = [1]
#possible_numbers[4][8] = [5]
#possible_numbers[5][3] = [9]
#possible_numbers[5][5] = [4]
#possible_numbers[6][4] = [7]
#possible_numbers[6][5] = [5]
#possible_numbers[7][3] = [2]
#possible_numbers[7][5] = [7]
#possible_numbers[7][9] = [4]
#possible_numbers[8][6] = [3]
#possible_numbers[8][7] = [6]
#possible_numbers[8][8] = [1]
#possible_numbers[9][7] = [8]

#for i in ROWS:
#    for j in COLS:
#        print possible_numbers[i][j]

#print(calc_group(7, 9))
#print_possible_numbers()

# Initial cleaning
print("Initial Cleaning")
clean_possible_numbers()

while True:

    loop_cnt = 0
    progress_is_made = True
    while progress_is_made:
        progress_is_made = False
        print("Analysis Loop: %d" % (loop_cnt))

        if analyze_cols():
            clean_possible_numbers()
            progress_is_made = True

        if analyze_rows():
            clean_possible_numbers()
            progress_is_made = True

        if analyze_groups():
            clean_possible_numbers()
            progress_is_made = True

        if analyze_box_cols_rows():
            clean_possible_numbers()
            progress_is_made = True

        loop_cnt += 1

    print_possible_numbers()

    processing_input = True
    while processing_input:
        response = raw_input("  How do you wish to proceed? (Enter Update: col,row,num1,num2,... | done | quit): ")

        if response == "quit" or response == "Quit" or response == "QUIT":
            print("  Exiting")
            sys.exit()

        elif response == "done" or response == "Done" or response == "DONE":
            print("  Done...return to analyzing")
            processing_input = False

        else:
            match_obj = re.match(r'([1-9]),([1-9])((?:,[1-9])+)', response)
            if match_obj:
                #print(match_obj.group(1), " - ", match_obj.group(2), " - ", match_obj.group(3))
                ud_col = int(match_obj.group(1))
                ud_row = int(match_obj.group(2))
                ud_pn = match_obj.group(3)
                ud_pn = ud_pn.strip(",")
                ud_pn = [int(n) for n in ud_pn.split(",")]
                #ud_pn = ud_pn.split(",")
                while True:
                    temp_string = "  Update table Col: " + str(ud_col) + " Row: " + str(ud_row) + " with: " + str(ud_pn) + "? (y/n): "
                    yn_resp = raw_input(temp_string)
                    if yn_resp == "y" or yn_resp == "Y":
                        print("  Updating possible numbers")
                        possible_numbers[ud_col][ud_row] = ud_pn
                        print_possible_numbers()
                        break
                    elif yn_resp == "n" or yn_resp == "N":
                        print("  NOT updating possible numbers")
                        break
                    else:
                        print("  Response not recognized...try again")

            else:
                print("  Response not recognized...try again")
        #elif response == "N" or response == "n" or response == "No" or response == "no" or response == "NO":
        #    print "  No files removed"
        #    break



