import string

###############################################################################################################################
###############################################################################################################################
##
## Best Times Program
##
## Mario Moro Hernandez
##
## Lab Exam 2, 17 April 2012
##
###############################################################################################################################
###############################################################################################################################
##
## This program is to manage a data base which stores the best personal times of
## the members of a certain swimming club.
##
## The program loads the data from a file stored on the disk and place those data
## into a dictionary stored in memory.
## The program also allows the user to print the results ordered by time and
## grouped by styles and gender.
## The user can also update the database and save the updated results into a data
## file stored on the disk.
##
##
## Data structures:
## records type<dict>:
##      Its structure is {ID:{'event':event,'gender':gender,'age':age','time':time,'name':name'}
##
##      As it can be seen is a dictionary which contains a subdictionary which
##      contains the data for each case.
##
##      ID: is the main key. This is to eventualy manage the problem that arises
##          when there are two different swimmers with the same name compiting in
##          the same event. This is not implemented in the actual code, but leaves
##          the code ready to do so.
##
##      {subdictionary}:
##          event:  type<str>   stores the event in which the swimmer got their personal best.
##          gender: type<str>   stores swimmer's gender.
##          age:    type<int>   stores swimmer's age.
##          time:   type<float> stores swimmer's personal best in float point format.
##          name:   type<str>   stores swimmer's name.
##
## timeList type<list>:
##      This is a list generated within the sortByTime(records) function. It is
##      an auxiliary data structure to use the sort method implemented in python.
##
##
## Data File format:
## The data are stored on a text file in this format:
##
##      Event:Gender:Age:Time:Name
##
## so, the layout of the file is:
##
##      IM:F:6:58.2:Kirsty Laing
##      BA:F:6:43.5:Joan Pine
##      IM:M:6:57.2:Eric Idle
##      IM:M:6:58.2:Ciaran Johnson
##
##
## Limitations and exceptions:
##
## The program is able to handle exceptions such as not valid filenames when loading
## or saving the data files. It also handles bad user entries on the menu or when
## different options are offered to the user (see, e.g., 'chooseEvent' or 'another'
## functions). However, in the case of the updateTimes() function it is assumed that
## the user types the time in the right format.
##
## The sorting method employed to sort the results in function of the time is the
## own sorting algorithm implemented in the python method for lists list.sort().
## This is probably not the best, but because of the restrictions of the exam
## conditions it is deemed as the best solution in this context.
##
## In this sense, the routine to check and update the results is not the best either.
## However, for the size of the database involved in this case, it is reliable enough.
##
###############################################################################################################################
###############################################################################################################################


records = {}                # global dictionary to store the records loaded from the disk.
quitProgram = False         # boolean variable to control the execution of the program.
debug = 0                   # debug control. 1 sets the debug mode ON, 0 sets the debug mode OFF.


###############################################################################################################################
###############################################################################################################################
##
## another(): auxiliary function to manage the retry situations within the different main functions.
def another():
    options = ('y','n')                             # valid user options.
    userInput = ''
    print 'Do you want to retry (Y/N)?',

    while userInput not in options:                 # keeps on prompting user input until a valid input is entered.
        userInput = string.lower(raw_input())
        if userInput not in options:                # exception handler.
            print 'Please type a valid option Y or N (no case-sensitive):',

    return userInput                                #returns user input.


###############################################################################################################################
###############################################################################################################################
##
## File Handling functions
##
###############################################################################################################################
###############################################################################################################################
##
## loadFile(): this function reads the lines stored in the file and stores the data into the proper data structure.
def loadFile():
    records = {}                                    # local dictionary.
    ID = 0                                          # Index.
    try:
        print 'Please type filename:',
        fileName = raw_input()
        fileIn = open(fileName,'r')                 # open file.
        while True:                                 # read data and place into the data structure routine.
            line = fileIn.readline()                
            if line == '':                          # finish flag.
                break
            else:
                split = string.split(line[:-2],':') # data handling sequence.
                event = split[0]
                gender = split[1]
                age = int(split[2])
                time = float(split[3])
                name = split[4]

                records[ID] = {'event':event,'gender':gender,'age':age,'time':time,'name':name}

                if debug == 1:
                    print records[ID]

                ID = ID + 1

        fileIn.close()                              # close file.

    except IOError:                                 # exception handler (filename error).
        print fileName,'not found',                 # message to the user.
        retry = another()                           # retry sequence.
        if retry == 'y':
            records = loadFile()

    return records


## saveFile(records): this function places the data stored in memory into a text file stored on disk.
def saveFile(records):
    nameError = True                                # exception flag.
    fileName = ''
    while nameError == True:                        # filename input sequence.
        print '\nPlease type a valid filename (ending in ".txt"):',
        fileName = raw_input()

        if fileName == '' or fileName[-4:] != '.txt':   # bad name exception handling code.
            print fileName, 'is not a valid filename. Make sure you typed ".txt" at the end.\n'
            retry = another()
            if retry == 'n':
                break
        else:
            nameError = False                       # exception flag.
            fileOut = open(fileName, 'w')           # open file in write mode.
            for ID in records:                      # writting into file sequence.
                line = records[ID]['event'] + ':' + records[ID]['gender'] + ':' + str(records[ID]['age']) + ':' + str(records[ID]['time']) + ':' + records[ID]['name'] + '\r' + '\n'

                if debug == 1:
                    print line

                fileOut.write(line)

            fileOut.close()                         # close file.

    return records


###############################################################################################################################
###############################################################################################################################
##
## Print functions
##
###############################################################################################################################
###############################################################################################################################
##
## sortByTime(records) makes a copy of the data stored in records on a list and sort the records by time
def sortByTime(records):
    timeList = []                               # creates the list.

    for ID in records:                          # makes the copy onto the list.
        timeList = timeList + [[records[ID]['time'],records[ID]['event'],
                                records[ID]['gender'],records[ID]['age'],
                                records[ID]['name']]]

    timeList.sort()                             # sorts the list.

    return timeList


## extractGender(timeList) splits the list generated by sortByList into two different lists based on gender.
def extractGender(timeList):
    male = []                                   # creates the two lists: one for males another for females.
    female = []
    for i in range(len(timeList)):              # split sequence.
        if timeList[i][2] == 'F':
            female = female + [timeList[i]]
        else:
            male = male + [timeList[i]]
    return male,female                          # return both lists.


## extractEvent(timeList): splits the cases stored in a list of times by event. This is an auxiliary function
##                         for the function printByGender(gender).
def extractEvent(timeList):
    IM = []                                     # creates one list for each event.
    BS = []
    BA = []
    CR = []
    FS = []
    for i in range(len(timeList)):              # distributes the cases into the right event.
        if timeList[i][1] == 'IM':
            IM = IM + [timeList[i]]
        elif timeList[i][1] == 'BS':
            BS = BS + [timeList[i]]
        elif timeList[i][1] == 'BA':
            BA = BA + [timeList[i]]
        elif timeList[i][1] == 'CR':
            CR = CR + [timeList[i]]
        elif timeList[i][1] == 'FS':
            FS = FS + [timeList[i]]
            
    return IM,BS,BA,CR,FS                       # returns the lists with the results of all the events.


## printByGender(gender): takes each list of times created by the function extractGender(timeList) and print the
##                        results. It is a subfunction of the main function printResults(records).
def printByGender(gender):
    IM,BS,BA,CR,FS = extractEvent(gender)           # asigns the records into the apropiate event list.

    if debug == 1:
        print len(IM),len(BS),len(BA),len(CR),len(FS)

    if len(IM) != 0:                                # if there are records for an event, it prints the results,
        print '\nTime\tEvent\tGender\tAge\tName'    
        for i in range(len(IM)):
            print IM[i][0],'\t',IM[i][1],'\t',IM[i][2],'\t',IM[i][3],'\t',IM[i][4]
    else:
        del IM                                      # otherwise, it deletes the list.
    if len(BS) != 0:
        print '\ntime\tEvent\tGender\tAge\tName'
        for i in range(len(BS)):
            print BS[i][0],'\t',BS[i][1],'\t',BS[i][2],'\t',BS[i][3],'\t',BS[i][4]
    else:
        del BS
    if len(BA) != 0:
        print '\ntime\tEvent\tGender\tAge\tName'
        for i in range(len(BA)):
            print BA[i][0],'\t',BA[i][1],'\t',BA[i][2],'\t',BA[i][3],'\t',BA[i][4]
    else:
        del BA
    if len(CR) != 0:
        print '\ntime\tEvent\tGender\tAge\tName'
        for i in range(len(CR)):
            print CR[i][0],'\t',CR[i][1],'\t',CR[i][2],'\t',CR[i][3],'\t',CR[i][4]
    else:
        del CR
    if len(FS) != 0:
        print '\ntime\tEvent\tGender\tAge\tName'
        for i in range(len(FS)):
            print FS[i][0],'\t',FS[i][1],'\t',FS[i][2],'\t',FS[i][3],'\t',FS[i][4]
    else:
        del FS
        

## printResults(records): make use of the functions defined earlier to get an output of the
##                        results in the required the format.
def printResults(records):
    timeList = sortByTime(records)
    male,female = extractGender(timeList)
    printByGender(female)
    printByGender(male)


###############################################################################################################################
###############################################################################################################################
##
## Data manipulation functions
##
###############################################################################################################################
###############################################################################################################################
##
## chooseEvent(): is an auxiliary function for restricting the user's event input and keep the database
##                integrity when updating a swimmer's personal best.
def chooseEvent():
    options = ('1','2','3','4','5')         # set of valid user's input options.
    userInput = ''
    print '\n1. Individual Medley (IM).'
    print '2. Breast Stroke (BS).'
    print '3. Backstroke (BA).'
    print '4. Crawl (CR).'
    print '5. Free Style (FS).'
    print '\nChoose an option (1-5):',

    while userInput not in options:         # user's input gather code and input exceptions handler.
        userInput = raw_input()
        if userInput not in options:
            print '\nPlease type a number from 1 to 5:',

    if userInput == '1':
        event = 'IM'
    elif userInput == '2':
        event = 'BS'
    elif userInput == '3':
        event = 'BA'
    elif userInput == '4':
        event = 'CR'
    elif userInput == '5':
        event = 'FS'

    return event                            # returns the event.


## updateTimes(swimmer,temp,recors): this sub-function of the checkTimes(records) function is the actual bit
##                                   of code that checks whether a swimmer's time is better than the one stored
##                                   and updates the database. It takes four arguments: swimmer's name, a temporary
##                                   dictionary with the swimmer's name as a key, the records dictionary, and the
##                                   ID key of the swimmer in the main dictionary.
def updateTimes(swimmer,temp,records,swimmerID):
    print 'Please type time (format SS.D)',
    time = input()
    if time < temp[swimmer]['time']:        # checks if the new time is better.
        event = chooseEvent()               # assigns the event where the new personal best has been achieved.
        temp[swimmer]['time'] = time
        temp[swimmer]['event'] = event
        records[swimmerID] = temp[swimmer]  # updates the main dictionary.
        print '\nPersonal best for',swimmer,'has been updated.'
                
    return records


## checkTimes(records): this function goes throught the dictionary extract the apropiate case and updates the
##                      personal best for the said swimmer.
def checkTimes(records):
    temp = {}                               # creates a temporary dictionary to store the swimmer's record.
    swimmer = raw_input("\nPlease type swimmer's name: ")
    for ID in records:                      # extracts swimmer from the database and place it into.
        if records[ID]['name'] == swimmer:  # the temporary dictionary.
            temp[swimmer] = records[ID]
            swimmerID = ID                  # stores swimmer's key from the main dictionary.
    
    check = temp.get(swimmer,'not found')   # checks whether swimmer is in the database or not.

    if debug == 1:
        print temp
        print check
    
    if check != 'not found':                # update routine
        updateTimes(swimmer,temp,records,swimmerID)
    else:
        print swimmer,'not found',
        retry = another()                   # retry routine if swimmer is not in the database.
        if retry == 'y':
            checkTimes(records)

    return records


###############################################################################################################################
###############################################################################################################################
##
## Main menu function
##
###############################################################################################################################
###############################################################################################################################
##
## menu(): contains the main menu.
def menu():
    global records                          # global records dictionary.
    global quitProgram                      # quitProgram state variable.

    options = ('l','s','p','c','q')         # valid user's inputs.
    userInput = ''

    print '\nl. Load File.'
    print 's. Save File.'
    print 'p. Print Results.'
    print 'c. Check Times.'
    print '\nq. Quit.'
    print '\nPlease, choose an option:',
    
    while userInput not in options:         # user's input and input exception handler.
        userInput = string.lower(raw_input())
        if userInput not in options:
            print 'Please type a valid option (L/S/P/C/Q; no case-sensitive):',

    if userInput == 'l':                    # this bit of code fires the right function according to the user's choice.
        records = loadFile()
    elif userInput == 's':
        saveFile(records)
    elif userInput == 'p':
        printResults(records)
    elif userInput == 'c':
        checkTimes(records)
    elif userInput == 'q':
        quitProgram = True


###############################################################################################################################
###############################################################################################################################
##
## main program routine
##
###############################################################################################################################
###############################################################################################################################

while quitProgram == False:
    menu()
