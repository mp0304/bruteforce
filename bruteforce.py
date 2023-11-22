import random
'''Imports the "random" library. In this program, it is used to generate a random number to determine the length of a 
guess, as well as to pick a random selection of characters from the character list.'''
import hashlib
'''Imports the "hashlib" library. This is used to take a guess and encrypt it in the sha256 format. The hash is then
compared to a user inputted hash, or hash from csv.'''
import time
# Imports the "time" library. This is used to calculate the time it takes for each hash to be cracked.
import csv
# Imports the "csv" library. This is used to read the csv file for the hashes to be inputted into the program.

chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ¬`¦!£€$%^&*()_+-={}[];:@'#~<,>.?/|\\"'"'
# A string that contains all of the characters on a UK keyboard.
charlist = list(chars)
# Converts the string to a list, seperating the characters. e.g. ['a'],['b'],['c']

correctlist = []
# Creates an empty list to be used later in the code. This list will store all of the correct passwords.
hashlist = []
'''Creates an empty list to be used later in the code. This list will store all of the user inputted hashes, or hashes
from the csv file.'''
def userinput():
    hashmethod = int(input("Press 1 to insert hashes yourself, 2 to use a csv: "))
    # The user chooses between inserting the hashes into the program themselves, or to use a csv file.
    if hashmethod == 1:
        # If the user chooses to input the hashes themselves:
        hashamount = int(input("How many hashes would you like to crack? "))
        # Allows the user to choose how many different hashes they want to input.
        for i in range(hashamount):
            # This loop will run i amount of times, with i being the number the user entered.
            hashinput = input("Please enter a hash: ")
            # The user enters the hash
            hashlist.append(hashinput)
            # The hash just entered will be added to the list of hashes, which is empty at first.
    if hashmethod == 2:
        # If the user chooses to have the hashes read from a csv file:
        with open('sha256_hashes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            '''The above code was sourced from https://docs.python.org/3/library/csv.html. It is used to read the csv file 
            and allows the column names, hash and plain, to be ignored.'''
            for row in reader:
                # This loop will run as many times as there is rows in the csv file, excluding the top row.
                hashlist.append(row['hash'].lower())
                '''Adds every hash in the csv file to the hash list. row['hash'] allows the code to skip the top line that 
                labels the column.'''
    global output
    output = int(input("Press 1 to have an output displayed, 2 to hide it (recommended for performance). "))
    global starttime
    starttime = time.time()
    # Measures the amount of time passed since the epoch, 1st January 1970, in seconds. This will be used later.
userinput()

def bruteforce():
    guesshashed = ""
    # Sets the guesshashed variable to an empty string. This will allow for the variable to be used later on.
    while guesshashed != hashlist[:-1]:
        # This loop will iterate as long as the hashed guess does not appear in the hash list.
        guesslen = random.randint(1, 5)
        # The length of the string containing the guess will be random, from 1 character, to 5.
        guess = random.choices(charlist, k=guesslen)
        # The guess will be a random selection of x amount of characters from the character list, x being set above.
        guess = "".join(guess)
        # Joins the characters together so that they appear "abc", rather than ['a'],['b'],['c'].
        guesshashed = hashlib.sha256(guess.encode('utf-8')).hexdigest()
        '''The above code is sourced from https://datagy.io/python-sha256/. This is used to encrypt the guess generated
        into the sha256 format.'''
        if output == 1:
            print(guess, " - ", guesshashed)
        '''This will print the guess and its hash into the command line. This shows the user the process that the code
        is going through.'''
        if guesshashed == hashlist[0]:
            # If the hashed guess is the same as the first item in the hashlist:
            correctlist.append(guess)
            # Adds the guess that was hashed to get the match to a list.
            endtime = time.time()
            # Measures the amount of time passed since the epoch, 1st January 1970, in seconds.
            totaltime = endtime - starttime
            # This takes the end time, defined above, and subtracts the start time from it, presenting the difference.
            if len(correctlist) == 1:
                # If the length of the correct guesses list is exactly 1:
                print("The cracked hash is: ", correctlist, ". Guessed in ", totaltime, "s")
                # Prints the above message, showing the correct guess, and the amount of time it took to get it.
            else:
                # If the list is longer than 1:
                print("The cracked hashes are: ", correctlist, ". Guessed in ", totaltime, "s")
                # Prints the above message, showing the correct guesses, and how long it took to get it.
            guesshashed = ""
            # Sets the hashed guess back to an empty string. This will trigger the while loop above.
            hashlist.remove(hashlist[0])
            '''Removes the first item in the list of hashes. This allows the code to compare the guess hashed to a new 
            hash'''
            if len(hashlist) == 0:
                # If the hash list is empty:
                break
                # Stops the code.


bruteforce()
