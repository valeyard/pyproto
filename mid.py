import string

records = {}                # global dictionary to store the records loaded from the disk.
quitProgram = False         # boolean variable to control the execution of the program.
debug = 0                   # debug control. 1 sets the debug mode ON, 0 sets the debug mode OFF.
students = [1101652, 1101653, 1101654, 1101655, 1101656, 1101657] # assuming that this is list of students


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
                course = split[0]
		student = split[1]
		lectureTime = split[2]
		attended = int(split[3])

		records[ID] = {'course':course,'student':student,'lectureTime':lectureTime,'attended':attended}

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
		line = records[ID]['course'] + ':' + records[ID]['student'] + ':' + records[ID]['lectureTime'] + ':' + str(records[ID]['attended']) + '\r' + '\n'

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


## printResults(records): make use of the functions defined earlier to get an output of the
##                        results in the required the format.
def printRecords(records):
    for value in records:
        print records[value][course] + " - " + records[value][lectureTime] + " - " + records[value][student] + " - " + records[value][attended]


### markAttendence
def markAttendence():
   course = raw_input( "Type course: ")
   lectureTime = raw_input("What's lecture time: ")
   
   for svalue in students:
       student = svalue
       attended = raw_input("Did student " + student + " attended? Enter 0/1:")
       records[] =  course + ":" + student + ":" + lectureTime + ":" + attended

   saveFile(records)

def exportAttendenceByCourse(eCourse):
    for value in records:
        if eCourse == records[value][course]:
            # generate new ditcionary for export
        
        # save to file # file name can be hardcoded
        # print data? for admin?


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

    options = ('l','s','p','1','2', '3', 'q')         # valid user's inputs.
    userInput = ''

    print '\nl. Load File.'
    print 's. Save File.'
    print 'p. Print Results.'
    print '1. Export attendence by course '
    print '2. Export Student Attendence.'
    print '3. Mark attendence.'
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
        printRecords(records)
    elif userInput == '1':
       # checkTimes(records)
    elif userInput == '2':
      # 
    elif userInput == '3':
        markAttendence()
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
