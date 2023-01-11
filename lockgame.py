MIN_LEN = 4
MAX_LEN = 8


def main():
    # DICTIONARIES TO CONVERT INPUT TO INDEXES AND INDEXES TO OUTPUT
    index_to_char = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    char_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    permission = "y"
    # TAKING THE CHARACTERS FOR EACH PLAYER
    player_a = str(input("Enter a character for player 1[can't be space] " ": "))
    while len(player_a) != 1 or player_a.strip() == "":
        print("You must enter a valid character: ")
        player_a = str(input("Enter a character for player 1[can't be space] " ": "))
    player_b = str(input("Enter a character for player 2[Can't be space or same character as player A] " ": "))
    while len(player_b) != 1 or player_b.strip() == "" or player_b == player_a:
        print("You must enter a valid character: ")
        player_b = str(input("Enter a character for player 2[Can't be space or same character as player A] " ": "))
    # GAME LOOP
    while permission in ["Y", "y"]:
        try:
            length = int(input("Enter game board size[for 4x4 - 8x8, enter a number between 4-8]: "))
            while length < MIN_LEN or length > MAX_LEN:
                print("Game board size must be between 4x4 - 8x8.")
                length = int(input("Enter game board size[for 4x4 - 8x8, enter a number between 4-8]: "))
        except ValueError:
            print("You must enter a valid integer!")
            continue

        a_locked = 0
        b_locked = 0

        turn_of_a = True            # PLAYER A STARTS FIRST

        table = create_table(length, player_a, player_b)            # CREATE THE STARTING TABLE
        table_print(table, length, index_to_char)                   # PRINT IT

        while a_locked < length-1 and b_locked < length-1:          # GAME ENDS IF A PLAYER HAS LESS THAN 2 STONES
            # MAKE SURE IF THE INPUT IS CORRECT AND THE MOVE IS POSSIBLE
            from_row, from_col, to_row, to_col = \
                get_correct_input(table, length, player_a, player_b, char_to_index, turn_of_a)
            # MAKE THE MOVE
            table, last_row, last_col = move_stone(table, player_a, player_b,
                                                   from_row, from_col, to_row, to_col, turn_of_a)
            # STORING THE LOCK-CHECK TABLE IN CASE THERE ARE NO LOCKED STONES.
            detect_table = lock_detect(table, player_a, player_b, length, index_to_char, turn_of_a, last_row, last_col)
            if detect_table != 0:   # CHANGE THE TABLE IF THERE IS A LOCKED STONE
                table = detect_table[:]
                if turn_of_a:
                    b_locked += 1
                else:
                    a_locked += 1

            table_print(table, length, index_to_char)           # UPDATED TABLE PRINT

            turn_of_a = not turn_of_a             # CHANGE THE TURN BOOLEAN

        if a_locked == length-1:    # ENDGAME PRINTS
            print(f"Player {player_b} won!")
        else:
            print(f"Player {player_a} won!")

        permission = input("Do you want to play another game?(YyNn): ")     # CONTINUE SENTINEL
        while permission not in ["Y", "y", "N", "n"]:
            print("Invalid entry!")
            permission = input("Do you want to play another game?(YyNn): ")
    print("Goodbye!")


def convert_input(location_input, char_to_index):
    # CONVERTING THE STRING INPUT TO COORDINATES
    locations = location_input.split()
    from_row = int(locations[0][0]) - 1
    from_col = char_to_index[(locations[0][1])]
    to_row = int(locations[1][0]) - 1
    to_col = char_to_index[(locations[1][1])]

    return from_row, from_col, to_row, to_col


def is_move_possible(table, length, from_row, from_col, to_row, to_col, player_a, player_b):
    # THIS FUNCTION CHECKS IF THE MOVE IS POSSIBLE. (STEP OVER, DIAGONAL MOVE ETC.)
    if from_row == to_row:
        if to_col > from_col:  # move to right
            move_right = True
            i = 1
            horizontal_limit = 0
            stone = is_stone(table, player_a, player_b, from_row, from_col + i)
            while stone == 0 and from_col + i < length:
                horizontal_limit += 1
                i += 1
                if from_col + i == length:
                    break
                else:
                    stone = is_stone(table, player_a, player_b, from_row, from_col + i)
        elif to_col < from_col:  # move to left
            move_right = False
            i = 1
            horizontal_limit = 0
            stone = is_stone(table, player_a, player_b, from_row, from_col - i)
            while stone == 0 and from_col - i >= 0:
                horizontal_limit += 1
                i += 1
                if from_col - i < 0:
                    break
                else:
                    stone = is_stone(table, player_a, player_b, from_row, from_col - i)
        else:
            print("You need to move to another square!")
            return False

        if move_right:
            if horizontal_limit + from_col >= to_col:
                return True
            else:
                return False
        else:
            if from_col - horizontal_limit <= to_col:
                return True
            else:
                return False

    elif from_col == to_col:
        if to_row < from_row:  # move up
            move_up = True
            i = 1
            vertical_limit = 0
            stone = is_stone(table, player_a, player_b, from_row - i, from_col)
            while stone == 0 and from_row - i >= 0:
                vertical_limit += 1
                i += 1
                if from_row - i < 0:
                    break
                else:
                    stone = is_stone(table, player_a, player_b, from_row - i, from_col)
        else:  # move down
            move_up = False
            i = 1
            vertical_limit = 0
            stone = is_stone(table, player_a, player_b, from_row + i, from_col)
            while stone == 0 and from_row + i < length:
                vertical_limit += 1
                i += 1
                if from_row + i >= length:
                    break
                else:
                    stone = is_stone(table, player_a, player_b, from_row + i, from_col)

        if move_up:
            if from_row - vertical_limit <= to_row:
                return True
            else:
                return False
        else:
            if from_row + vertical_limit >= to_row:
                return True
            else:
                return False

    else:
        print("You can only move vertically or horizontally!")
        return False


def is_stone(table, player_a, player_b, row, col):
    # CHECKS IF THERE IS A STONE ON A SPECIFIC SQUARE(IF YES, RETURNS THE STONE TYPE. ELSE, RETURNS FALSE)
    try:
        if table[row][col] == player_a:
            return player_a
        elif table[row][col] == player_b:
            return player_b
        else:
            return False
    except IndexError:
        return False


def create_table(length, player_a, player_b):
    # CREATES A 2D LIST FOR THE GAME
    table = [[" " for _ in range(length)] for _ in range(length)]
    for row in range(length):
        for column in range(length):
            if row == 0:
                table[row][column] = player_b
            elif row == length - 1:
                table[row][column] = player_a
            else:
                continue
    return table


def table_print(table, length, char_dict):
    # THIS IS FOR DISPLAYING THE TABLE TO USER
    print_length = 5 * length + length + 1
    print("      ", end="")
    for index in range(length):
        if index == length - 1:
            print(char_dict[index], "   ")
            break
        print(char_dict[index], end="     ")
    print("   ", end="")
    print("-" * print_length)
    for row in range(length):
        print(f"{row + 1}  ", end="")
        for column in range(length):
            if column == length - 1:
                print(f"|  {table[row][column]}  |", end="")
                print(f"  {row + 1}")
                print("   ", end="")
                print("-" * print_length)
            else:
                print(f"|  {table[row][column]}  ", end="")
    print("      ", end="")
    for index in range(length):
        if index == length - 1:
            print(char_dict[index], "   ")
            break
        print(char_dict[index], end="     ")


def get_correct_input(table, length, player_a, player_b, char_to_index, turn_of_a):
    # IT CHECKS EVERYTHING ENTERED. ALSO USES THE FUNCTION IS_STONE AND IS_MOVE_POSSIBLE. GETS DATA AGAIN AND AGAIN
    # UNTIL ITS TRUE OR THE MOVE IS POSSIBLE.
    correct = False
    if turn_of_a:
        player = player_a
    else:
        player = player_b
    while not correct:
        print(f"Player {player}, please enter the position of your own stone you want to move and the target position: "
              , end="")
        location_raw = input()
        location_raw = location_raw.upper()
        try:
            from_row, from_col, to_row, to_col = convert_input(location_raw, char_to_index)
        except ValueError:
            print("Square does not exist!")
            continue
        except KeyError:
            print("Square does not exist!")
            continue
        except IndexError:
            print("Square does not exist!")
            continue

        stone = is_stone(table, player_a, player_b, from_row, from_col)

        if not stone:
            print("No stone on that square.")

        elif stone == player_b and turn_of_a or stone == player_a and not turn_of_a:
            print("You can only move your stones.")

        else:
            if is_move_possible(table, length, from_row, from_col, to_row, to_col, player_a, player_b):
                return from_row, from_col, to_row, to_col
            else:
                print("Move not possible!")


def move_stone(table, player_a, player_b, from_row, from_col, to_row, to_col, turn_of_a):
    # MOVES A SPECIFIC STONE TO A SPECIFIC SQUARE.
    table[from_row][from_col] = " "
    if turn_of_a:
        table[to_row][to_col] = player_a
    else:
        table[to_row][to_col] = player_b
    return table, to_row, to_col


def corner(length, row, col):
    # CHECKS IF THE GIVEN SQUARE IS A CORNER. RETURNS BOOLEAN.
    if row == 0:
        if col == 0 or col == length - 1:
            return True
    elif row == length - 1:
        if col == 0 or col == length - 1:
            return True
    else:
        return False


def lock_detect(table, player_a, player_b, length, index_to_char, turn_of_a, last_row, last_col):
    # BASICALLY BRUTE FORCE LOCK DETECTOR. CHECKS EVERY SQUARE TO SEE IF THEY ARE LOCKED. ONLY WORKS IF THE TURN AND
    # LOCKED STONE TYPE ARE OPPOSITE. SO THE PLAYER CAN'T SUICIDE.
    locked_count = 0
    locked_list = []        # FOR PRINTING THE LOCKED STONES
    for row in range(length):
        for col in range(length):
            is_lock = False
            stone = is_stone(table, player_a, player_b, row, col)
            if not stone:
                if row == length - 1 and col == length - 1:
                    if locked_count > 0:
                        print(f"Locked Square(s) : {locked_list}")
                        return table
                    else:
                        return 0

            else:  # there is a stone in that sqr
                if row != 0:
                    up = is_stone(table, player_a, player_b, row - 1, col)
                else:
                    up = 0

                if row != length - 1:
                    down = is_stone(table, player_a, player_b, row + 1, col)
                else:
                    down = 0

                if col != 0:
                    left = is_stone(table, player_a, player_b, row, col - 1)
                else:
                    left = 0

                if col != length - 1:
                    right = is_stone(table, player_a, player_b, row, col + 1)
                else:
                    right = 0

                if corner(length, row, col):
                    if right == down and right != 0 and right != stone:
                        is_lock = True
                    elif left == down and left != 0 and left != stone:
                        is_lock = True
                    elif up == left and up != 0 and up != stone:
                        is_lock = True
                    elif up == right and up != 0 and up != stone:
                        is_lock = True
                    else:
                        if row == col == length-1:
                            if locked_count > 0:
                                print(f"Locked Square(s) : {locked_list}")
                                return table
                            else:
                                return 0

                    if is_lock:
                        lock_square = str(row + 1) + str(index_to_char[col])
                        locked_list.append(lock_square)
                        table[row][col] = " "
                        locked_count += 1

                else:  # not a corner
                    if right == left and right != 0 and right != stone:
                        if col - 1 == last_col or col + 1 == last_col:
                            is_lock = True
                    if up == down and up != 0 and up != stone:
                        if row - 1 == last_row or row + 1 == last_row:
                            is_lock = True

                    if is_lock:
                        if stone == player_a and turn_of_a:
                            continue
                        elif stone == player_b and not turn_of_a:
                            continue
                        else:
                            lock_square = str(row + 1) + str(index_to_char[col])
                            locked_list.append(lock_square)
                            table[row][col] = " "
                            locked_count += 1


main()
