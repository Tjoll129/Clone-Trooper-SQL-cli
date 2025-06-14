# import all necessary dependencies
import sys
import os
import random
import mysql.connector

# necessary code to log into sql connection

# replace with your user information for sql
# assumes you have a database named clonetroopers already
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="enter_your_password",
    database="clonetroopers"
)

# gets the size of the screen and saves it
screenSize = os.get_terminal_size().columns

# create variable used in sql functions
mycursor = mydb.cursor()

# lists of variables for troopers that are not numbers
colors = ['Red', 'Blue', 'Orange', 'Gray', 'Green', 'Yellow']
weapons = ['DC-15A Blaster Rifle', 'DC-15X Sniper Rifle', 'WESTAR-M5 Blaster Rifle', 'DC-15S Blaster Carbine',
           'RPS-6 Rocket Launcher', 'Z-6', 'PLX-1 Portable Missile Launcher', 'DC-15s Side Arm Blaster', 'DC-17 Blaster Pistol']
ranks = ['Cadet', 'Private', 'Corporal', 'Sergeant', 'Captain', 'Commander']


# returns random item from inputted list
def randomItem(input_list):
    return random.choice(input_list)

# FORMATTING METHODS


def customCloneTroopersScreen():
    clearScreen()
    screenLine()
    centerFormat("CREATE CUSTOM CLONE TROOPERS")
    screenLine()
    print()

# prints the array in order and numbers them


def printNumArray(arr):
    for i, item in enumerate(arr):
        print(" " * 40, end=" ")
        print(f"{i+1}. {item}")

# prints a line across the entire screen


def screenLine():
    print("-" * screenSize)

# prints a line for the top or bottom of menus


def menuLine():
    line = ""
    for x in range(47):
        line += "-"
    centerFormat(line)
    return line

# clears the screen


def clearScreen():
    print('\033[H\033[J')

# centers any text in the center of the screen


def centerFormat(word):
    length = (screenSize - len(word)) // 2
    for x in range(length):
        print(" ", end="")
    print(word)

# remove recursion


def randomIntInput(userNum):
    print()
    if userNum.isdigit():
        return int(userNum)
    else:
        print("\033[91mError\033[0m: Please enter a valid number.")
        input("Press the enter key to continue...")
        randomGenScreen()

# SQL FUNCTIONS


def generate_unique_id(army):
    new_id = 1
    while True:
        if not checkID(army, new_id):
            return new_id
        new_id += 1


def checkID(army, trooper_id):
    mycursor.execute("SELECT Trooper_ID FROM {}".format(army))
    trooper_ids = [row[0] for row in mycursor.fetchall()]

    if int(trooper_id) in trooper_ids:
        return True
    return False


def deleteID(army, id):
    mycursor.execute(
        "DELETE FROM {} WHERE Trooper_id = '{}'".format(army, id))
    mydb.commit()  # saves the data in mysql


def insertInto(army, values):
    query = "INSERT INTO {} (Trooper_ID, Trooper_Color, Trooper_Age, Trooper_Rank, Trooper_Weapon) VALUES (%s, %s, %s, %s, %s)".format(
        army)

    mycursor.execute(query, values)


def createId(army):
    mycursor.execute("SELECT MAX(Trooper_ID) FROM " + army)
    max = mycursor.fetchone()[0]
    if max is None:
        return 1
    else:
        return int(max) + 1


def createarmy(armyName):
    mycursor.execute("CREATE TABLE " + armyName +
                     " (Trooper_ID int(20), Trooper_Color VarChar(30), Trooper_Age VarChar(3), Trooper_Rank varchar(30), Trooper_Weapon Varchar(50), PRIMARY KEY (Trooper_ID))")
    mydb.commit()  # saves the data in mysql


def droparmy(armyName):
    mycursor.execute("DROP TABLE " + armyName)
    mydb.commit()  # saves the data in mysql


def updatearmys():
    mycursor.execute("SHOW TABLES")

    armys = []  # Initialize an empty list
    for (army_name,) in mycursor:  # Iterate through the cursor result
        armys.append(army_name)  # Append each army name to the list

    return armys


def showarmys():
    menuLine()
    print()
    centerFormat("These are the current available armys of Clone Troopers:\n")

    mycursor.execute("SHOW TABLES")

    list = ""
    armys = []  # Initialize an empty list
    for (army_name,) in mycursor:  # Iterate through the cursor result
        armys.append(army_name)  # Append each army name to the list

    for x in armys:
        list += (x + " ")

    centerFormat(list)
    print()
    menuLine()
    print()
    print()
    return armys


def selectFrom(army):
    mycursor.execute("SELECT * FROM " + army)
    result = mycursor.fetchall()

    print("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
        "ID", "Color", "Age", "Rank", "Weapon"))
    print("-" * 82)  # Separator line

    # Print each row in a formatted way
    for row in result:
        print("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
            row[0], row[1], row[2], row[3], row[4]))


# MENU SCREENS

# screen for randomly generating cloone troopers


def randomGenScreen():
    while True:
        clearScreen()
        screenLine()
        centerFormat("RANDOMLY GENERATE CLONE TROOPERS")
        screenLine()
        print()

        trooperNumber = input(
            "Please enter the number of Clone Troopers you want to generate: ")
        randomIntInput(trooperNumber)

        armys = showarmys()

        army = input(
            "Please select which army you would like to put your clone troopers into or press c to create a new army: ")
        print()

        if (army == "c" or army == "C"):
            while True:
                army = input(
                    "Enter the name of the army you want to create: ")
                if army in armys or army.lower() == "c":
                    print()
                    print(
                        "\033[91mError\033[0m: Cannot create duplicate army.")
                    input("Press enter to continue...")
                    print()
                else:
                    createarmy(army)
                    print()
                    print("army " + army + " successfully created")
                    input("Press enter to continue...")
                    print()
                    armys = updatearmys()
                    break
        if army in armys:

            for x in range(int(trooperNumber)):
                id = createId(army)
                trooper_color = random.choice(colors)
                trooper_age = random.randint(10, 60)
                trooper_weapon = random.choice(weapons)
                trooper_rank = random.choice(ranks)
                insertInto(army, (id, trooper_color, trooper_age,
                                  trooper_rank, trooper_weapon))
                mydb.commit()  # saves the data in mysql

            print()
            print("Succesfully generated " +
                  str(trooperNumber) + " Clone Troopers randomly")
            selection = input(
                "Press enter to go to main menu or press s to show generated troopers...")

            if (selection == "s" or selection == "S"):
                print()
                selectFrom(army)
                print()
                input("Press the enter key to continue to the main menu...")
            break

        else:
            print("\033[91mError\033[0m: Please enter a valid army.")
            input("Press enter to continue...")
            print()


def showTroopersScreen():
    while True:
        clearScreen()
        screenLine()
        centerFormat("SHOW CLONE TROOPERS")

        armys = showarmys()

        army = input("Please select which army you would like to view: ")
        print()

        if army in armys:
            selectFrom(army)
            print()
            input("Press enter to continue to main menu...")
            break

        else:
            print()
            print("\033[91mError\033[0m: Please enter a valid army.")
            input("Press enter to continue...")
            print()


def createTrooper():
    while True:
        customCloneTroopersScreen()
        cloneNum = input(
            "Enter how many Clone Troopers you would like to create: ")

        print()
        if cloneNum.isdigit():
            for x in range(int(cloneNum)):

                # Color selection Screen
                while True:
                    customCloneTroopersScreen()
                    centerFormat("Which Color would you like to select?")
                    menuLine()
                    printNumArray(colors)
                    menuLine()
                    cloneColor = input("Enter your selection: ")

                    if (cloneColor.isdigit() and int(cloneColor) < 7 and int(cloneColor) > 0):
                        centerFormat("You have chosen color: " +
                                     colors[int(cloneColor) - 1])
                        print()
                        print()
                        input("Press enter to continue to Age selection...")
                        print()
                        break
                    else:
                        print()
                        print(
                            "\033[91mError\033[0m: Please enter a valid number.")
                        input("Press enter to try again...")
                        print()

                # Trooper Age Selection
                while True:
                    customCloneTroopersScreen()
                    centerFormat("What age is your Clone Trooper?")
                    menuLine()
                    cloneAge = input(
                        "Please enter desired age for Clone Trooper: ")

                    if (cloneAge.isdigit() and int(cloneAge) < 1000 and int(cloneAge) > 0):
                        centerFormat(
                            "Your Clone Trooper's age is: " + cloneAge)
                        print()
                        print()
                        input("Press enter to continue to Trooper Rank...")
                        print()
                        break
                    else:
                        print()
                        print(
                            "\033[91mError\033[0m: Please enter a valid number.")
                        input("Press enter to try again...")
                        print()

                # Trooper Rank Selection
                while True:
                    customCloneTroopersScreen()
                    centerFormat("Which Rank would you like to select?")
                    menuLine()
                    printNumArray(ranks)
                    menuLine()
                    cloneRank = input("Enter your selection: ")

                    if (cloneRank.isdigit() and int(cloneRank) < 7 and int(cloneRank) > 0):
                        centerFormat("You have chosen rank: " +
                                     ranks[int(cloneRank) - 1])
                        print()
                        print()
                        input("Press enter to continue to Weapon selection...")
                        print()
                        break
                    else:
                        print()
                        print(
                            "\033[91mError\033[0m: Please enter a valid number.")
                        input("Press enter to try again...")
                        print()

                # Trooper Weapon Selection
                while True:
                    customCloneTroopersScreen()
                    centerFormat("Which Weapon would you like to select?")
                    menuLine()
                    printNumArray(weapons)
                    menuLine()
                    cloneWeapon = input("Enter your selection: ")

                    if (cloneWeapon.isdigit() and int(cloneWeapon) < 10 and int(cloneWeapon) > 0):
                        centerFormat("You have chosen the weapon: " +
                                     weapons[int(cloneWeapon) - 1])
                        print()
                        print()
                        input("Press enter to continue to army selection...")
                        print()
                        break
                    else:
                        print()
                        print(
                            "\033[91mError\033[0m: Please enter a valid number.")
                        input("Press enter to try again...")
                        print()

                # army Selection
                while True:
                    customCloneTroopersScreen()
                    centerFormat("army Selection")
                    armys = showarmys()

                    army = input(
                        "Please select which army you would like to store Clone Trooper data in: ")
                    print()

                    if army in armys:
                        customCloneTroopersScreen()
                        centerFormat("Your Clone Trooper")
                        centerFormat("-" * 86)  # Separator line

                        id = createId(army)

                        centerFormat("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
                            "ID", "Color", "Age", "Rank", "Weapon"))
                        centerFormat("-" * 86)  # Separator line

                        # Print each row in a formatted way
                        centerFormat("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
                            id, colors[int(cloneColor) - 1], cloneAge, ranks[int(cloneRank) - 1], weapons[int(cloneWeapon) - 1]))

                        insertInto(army, (id, colors[int(cloneColor) - 1], cloneAge,
                                          ranks[int(cloneRank) - 1], weapons[int(cloneWeapon) - 1]))

                        print("\nClone Trooper " + str(id) +
                              " successfully added to army " + army)
                        input("Press enter to continue to main menu...")
                        mydb.commit()  # saves the data in mysql
                        break
                    else:
                        print(
                            "\033[91mError\033[0m: Please enter a valid army.")
                        input("Press enter to continue...")
            break
        else:
            print()
            print("\033[91mError\033[0m: Please enter a valid digit.")
            input("Press enter to continue...")


def createArmy():
    # used later to get out of giant nested while loop
    success = False
    while True:
        clearScreen()
        screenLine()
        centerFormat("CREATE YOUR ARMY")

        armys = showarmys()

        army = input(
            "Please select which army you would like to pick your Clone Troopers from: ")
        print()

        if army in armys:
            while True:
                selectFrom(army)
                print()
                id = input("Enter Trooper ID you want to add to your army:")

                if id.isdigit():
                    IDFound = checkID(army, id)
                    if IDFound:
                        while True:
                            clearScreen()
                            screenLine()
                            centerFormat("CREATE YOUR ARMY")
                            showarmys()
                            print()
                            destination_army = input(
                                "Enter the name of the destination army or press c to create a new army: ")

                            if (destination_army.lower() == "c"):
                                while True:
                                    print()
                                    army_name = input(
                                        "Enter the name of the army you want to create: ")
                                    if army_name in armys or army.lower() == "c":
                                        print()
                                        print(
                                            "\033[91mError\033[0m: Cannot create duplicate army.")
                                        input("Press enter to continue...")
                                        print()
                                    else:
                                        createarmy(army_name)
                                        print()
                                        print("army " + army +
                                              " successfully created")
                                        input("Press enter to continue...")
                                        print()
                                        armys = updatearmys()
                                        destination_army = army_name
                                        break

                            if destination_army in armys:
                                mycursor.execute(
                                    f"SELECT * FROM {army} WHERE Trooper_ID = {id}")
                                trooper_data = mycursor.fetchone()
                                temp_army = f"temp_{id}_army"
                                createarmy(temp_army)
                                new_id = generate_unique_id(destination_army)
                                trooper_data = (new_id,) + trooper_data[1:]
                                insertInto(temp_army, trooper_data)
                                mydb.commit()

                                # Insert the trooper data into the destination army
                                mycursor.execute(
                                    f"INSERT INTO {destination_army} SELECT * FROM {temp_army}")
                                mydb.commit()

                                # Drop the temporary army
                                droparmy(temp_army)

                                # Delete the trooper from the source army
                                deleteID(army, id)
                                print("\nSuccessfully moved Clone Trooper " +
                                      str(id) + " to army " + destination_army + "!")
                                input("Press enter to continue to main menu...")
                                success = True
                                break
                            else:
                                print(
                                    "\n\033[91mError\033[0m: Please enter a valid army.")
                                input("Press the enter key to continue...")
                        if success:
                            break
                    else:
                        print(
                            "\n\033[91mError\033[0m: Please enter a valid number.")
                        input("Press the enter key to continue...")
                else:
                    print(
                        "\n\033[91mError\033[0m: Please enter a valid number.")
                    input("Press the enter key to continue...")
        else:
            print("\n\033[91mError\033[0m: Please enter a valid army.")
            input("Press enter to continue...")
            if success:
                break
        if success:
            break


def deleteTrooperarmy():
    while True:
        clearScreen()
        screenLine()
        centerFormat("DELETE CLONE TROOPER ARMY")
        armys = showarmys()
        army = input(
            "Enter the name of the army that you would like to delete: ")
        if army in armys:
            droparmy(army)
            print()
            print("Successfully deleted army " + army + "!")
            input("Press enter to continue to main menu...")
            break
        else:
            print("\n\033[91mError\033[0m: Please enter a valid army.")
            input("Press enter to continue...")
            print()


def deleteTrooper():
    while True:
        clearScreen()
        screenLine()
        centerFormat("DELETE CLONE TROOPER army")
        armys = showarmys()
        army = input(
            "Enter the name of the army that you would like to delete Troopers from: ")
        if army in armys:
            while True:
                clearScreen()
                mycursor.execute("SELECT * FROM " + army)
                result = mycursor.fetchall()

                print("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
                    "ID", "Color", "Age", "Rank", "Weapon"))
                print("-" * 82)  # Separator line

                # Print each row in a formatted way
                for row in result:
                    print("{:<13} {:<16} {:<14} {:<15} {:<24}".format(
                        row[0], row[1], row[2], row[3], row[4]))
                print()
                id = input("Enter the Trooper ID that you want to remove: ")

                print()
                if id.isdigit():
                    deleteID(army, id)
                    print("Successfully deleted Clone Trooper " +
                          id + " in army " + army + "!")
                    input("Press enter to continue to main menu...")
                    break
                else:
                    print(
                        "\033[91mError\033[0m: Please enter a valid number.\n")
                    input("Press the enter key to continue...")

            break
        else:
            print("\n\033[91mError\033[0m: Please enter a valid army.")
            input("Press enter to continue...")


# startup intro screen


def introScreen():
    clearScreen()
    screenLine()
    centerFormat(" ____ _____  _    ____   __        ___    ____  ____  ")
    centerFormat("/ ___|_   _|/ \  |  _ \  \ \      / / \  |  _ \/ ___| ")
    centerFormat("\___ \ | | / _ \ | |_) |  \ \ /\ / / _ \ | |_) \___ \ ")
    centerFormat(" ___) || |/ ___ \|  _ <    \ V  V / ___ \|  _ < ___) |")
    centerFormat("|____/ |_/_/   \_\_| \_\    \_/\_/_/   \_\_| \_\____/ ")
    print()
    centerFormat("THE CLONE GENERATOR")
    screenLine()
    print()
    print()
    input("Press enter to continue...")

# main menu screen also directs user to other screens based on user input

def mainscreen():
    while True:
        clearScreen()
        screenLine()
        centerFormat("THE CLONE TROOPER GENERATOR")
        centerFormat("Commands")
        menuLine()
        centerFormat("g - randomly generate Clone Troopers")
        print()
        centerFormat("c - create custom Clone Troopers")
        print()
        centerFormat("a - create new army of Clone Troopers")
        print()
        centerFormat("s - show all Clone Troopers")
        print()
        centerFormat("d - remove Clone Trooper armys")
        print()
        centerFormat("r - remove Clone Troopers")
        print()
        centerFormat("e - exit program")
        menuLine()
        print()
        selection = input("Please enter your command: ")

        if (selection == "g" or selection == "G"):
            randomGenScreen()

        elif (selection == "c" or selection == "C"):
            createTrooper()

        elif (selection == "a" or selection == "A"):
            createArmy()

        elif (selection == "s" or selection == "S"):
            showTroopersScreen()

        elif (selection == "d" or selection == "D"):
            deleteTrooperarmy()

        elif (selection == "r" or selection == "R"):
            deleteTrooper()

        elif (selection == "e" or selection == "E"):
            clearScreen()
            print("\033[94m", end="")
            centerFormat("May the Force be With you...")
            print("\033[0m")
            sys.exit(0)

        else:
            # prints a line then prints the word error in red then rest of the text in white
            print("\n\033[91mError\033[0m: Please enter a valid command.")
            input("Press the enter key to continue...")


# acts as main method
introScreen()
mainscreen()
