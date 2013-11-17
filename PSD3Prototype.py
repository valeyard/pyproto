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

records = {}                # global dictionary to store the student records loaded from the disk.
courses = {}                # global dictionary to store the courses information loaded from the disk.
quitProgram = False         # boolean variable to control the execution of the program.
debug = 1                   # debug control. 1 sets the debug mode ON, 0 sets the debug mode OFF.

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


## processStudentsFile(fileIn): auxiliary function to process students record files.
def processStudentsFile(fileIn):
    print 'inside processStudentsFile'
    student = {}                                # local dictionary.
    fileIn.readline()
    while True:                                 # read data and place into the data structure routine.
        print 'inside while'
        line = fileIn.readline()
        if line == '':                          # finish flag.
            break
        else:
            print 'inside else'
            split = string.split(line[:-1],',') # data handling sequence.
            course = split[0]
            IDNumber = split[1]
            courseWork = int(split[2])
            exam = int(split[3])
            total = int(split[4])

            student[IDNumber] = {'course':course,
                           'IDNumber':IDNumber,
                           'coursework':courseWork,
                           'exam':exam,
                           'total':total}

            if debug == 1:
                print student[IDNumber]
    return student


## processCoursesFile(fileIn): auxiliary function to process courses information files.
def processCoursesFile(fileIn):
    courses = {}                                    # local dictionary.
    fileIn.readline()
    while True:                                     # read data and place into the data structure routine.
            line = fileIn.readline()
            if line == '':                          # finish flag.
                break
            else:
                split = string.split(line[:-1],',') # data handling sequence.
                firstName = split[0]
                surname = split[1]
                IDNumber = split[2]
                courses[IDNumber] = {'firstName':firstName,
                                     'surname':surname,
                                     'IDNumber':IDNumber}
                i = 3
                while i < len(split):
                    var = 'lab' + str(i-2)
                    courses[IDNumber].update({var:split[i]})
                    i = i + 1
                    
                if debug == 1:
                    print courses[IDNumber]
    return courses


## saveStudentsFile(fileName,dataStructure): auxiliary function to save students record into a file.
def saveStudentsFile(fileName,dataStructure):                # exception flag.
    fileOut = open(fileName, 'w')                            # open file in write mode.
    fileOut.write('Course,ID number,Coursework,Exam,Total\n')
    for ID in dataStructure:                                 # writting into file sequence.
        line = (dataStructure[ID]['course'] + ',' +
               dataStructure[ID]['IDNumber'] + ',' +
               str(dataStructure[ID]['coursework']) + ',' +
               str(dataStructure[ID]['exam']) + ',' +
               str(dataStructure[ID]['total']) + '\n')

        if debug == 1:
            print line

        fileOut.write(line)

    fileOut.close()                                         # close file.


## saveCoursesFile(fileName,dataStructure): auxiliary function to save courses attendance into a file
def saveCoursesFile(fileName,dataStructure):                # exception flag.
    fileOut = open(fileName, 'w')                           # open file in write mode.

    headerOfFile = ('First name,' +                         # builds the first line
                    'Surname,' +
                    'ID number,')
    i = 1
    while i <= len(courses.items()[0][1]) - 3:
        headerOfFile = headerOfFile + 'Assignment: Laboratory ' + str(i) + ','
        i = i + 1
        
    headerOfFile = headerOfFile[:-1] + '\n'
    fileOut.write(headerOfFile)

    for ID in dataStructure:                                # writting into file sequence.
        line = (dataStructure[ID]['firstName'] + ',' +
                dataStructure[ID]['surname'] + ',' +
                dataStructure[ID]['IDNumber'] + ',')
                
        i = 1
        while i <= len(courses.items()[0][1]) - 3:
            field = 'lab' + str(i)
            line = line + dataStructure[ID][field] + ','
            i = i + 1
        line = line[:-1] + '\n'

        if debug == 1:
            print line

        fileOut.write(line)

    fileOut.close()                                         # close file.


###############################################################################################################################
###############################################################################################################################
##
## File Handling functions
##
###############################################################################################################################
###############################################################################################################################
##
## loadFile(filetype): this function reads the lines stored in the file and stores the data into the proper data structure.
def loadFile(fileType):
    try:
        print 'Please type filename:',
        fileName = raw_input()
        fileIn = open(fileName,'r')                 # open file.

        if fileType == 0:                           # process student files
            records = processStudentsFile(fileIn)
            return records
        if fileType == 1:                           # process course files
            courses = processCoursesFile(fileIn)
            return courses
        fileIn.close()                              # close file.

    except IOError:                                 # exception handler (filename error).
        print fileName,'not found'                  # message to the user.
    return                                          # exits gently

## saveFile(fileType, dataStructure): this function places the data stored in memory into a text file stored on disk.
def saveFile(fileType, dataStructure):
    nameError = True                                # exception flag.
    fileName = ''
    while nameError == True:                        # filename input sequence.
        print '\nPlease type a valid filename (ending in ".csv"):',
        fileName = raw_input()

        if fileName == '' or fileName[-4:] != '.csv':   # bad name exception handling code.
            print fileName, 'is not a valid filename. Make sure you typed ".csv" at the end.\n'
            retry = another()
            if retry == 'n':
                break
        else:
            nameError = False                       # exception flag.
            if fileType == 0:
                saveStudentsFile(fileName, dataStructure)
            if fileType == 1:
                saveCoursesFile(fileName, dataStructure)
    return

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
## Main menu function
##
###############################################################################################################################
###############################################################################################################################
##
## menu(): contains the main menu.
def menu():
    global records                          # global records dictionary.
    global courses
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
		print "Please enter which time of file you are loading, 0 for student records, 1 for courses"
		fileType = input()
        #records = loadFile(0)
        #courses = loadFile(1)
		if fileType == 0:
			records = loadFile(0)
		else
			courses = loadFile(1)
    elif userInput == 's':
		print "Please enter which time of file you want to save, 0 for student records, 1 for courses"
		fileType = input()
        #records = loadFile(0)
        #courses = loadFile(1)
		if fileType == 0:
			saveFile(0, records)
		else
			saveFile(1, courses)
        #saveFile(0,records)
        #saveFile(1,courses)
    elif userInput == 'p':
        printResults(records)
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
