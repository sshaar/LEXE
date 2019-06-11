#import datetime
from datetime import datetime


##########################################################################
                         #####interface######


#This function read the deadline from the text that user gives it 
#and then returns the deadline in terms of datetime
def get_deadline(text):
    pass
# requires text to be a string



#This function read the data (grade score, course score, time of task ) 
#from the text that user gives it, and then returns the data as float
def get_data(text):
    pass
# requires text to be a string



#This function returns how many perscentage you will lose if you don't do this task
#we use the output of this task to calculate the score of the task
#we get the inputs from the function get data 
def get_taskGrade(gradeTask, courseGrade):
    pass
# requires both of gradeTask and courseGrade to be a ints or floats



#This function returns the diff between the time you have and how long the task 
#will need to be done 
#we use the output of this task to calculate the score of the task 
#we get the input due from the function get_data
#we get the input deadline from the function get+deadline
def get_taskTime(due, deadLine):
    pass
# requires due to be a int or float
# requires deadline to be datetime



#This function gives you the score for each task
#we get due from get_data or the user manually
#we get taskTime from the function get_taskTime
#we get taskGrade from the function get_taskGrade
def give_score( due, taskTime, taskGrade):
    pass
#requires all of them to be ints or floats



#get the name of the task
def get_taskName(text):
    pass
# requires text to be a string



#This function takes a file that contains a text file that has the tasks
#then it adds the new task and reorder the list, then rewrite the file with 
#the updated list, then returns a dict with the list
#we get the task name from the function get_taskName
#we get the score from the function give_score which uses get_taskTime
#and get_taskGrade which use get_data to read the text from the user
def update_list(task, score):
    pass
# requires task to be a string
# requires score to be an int or a float 
   


#This function takes a text and parse it to get what you should search for
def parse_to_search(text):
    pass
#requires text to be string



##########################################################################

                            #####implementation######

#this function converts words numbers to int number
def text2int (textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand","million", "billion", "trillion"]
        scales2 = ["hundreds", "thousands","millions", "billions", "trillions"]


        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
        for idx, word in enumerate(scales2): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else: 
                scale, increment = numwords[word]

                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            


    if onnumber:
        curstring += repr(result + current)  

    return curstring



#This function read the deadline from the text that user
# gives it and then returns the deadline in terms of datetime
def get_deadline(text):

    text1 = text2int(text)
    newText = text1.split()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    months = [ "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    currentTime = datetime.now()
    final = ["", "" , str(currentTime.year)]
    for i in range(len(newText)):
        if newText[i].lower() in months:
            month = months.index(newText[i].lower()) + 1
            final[1] = str(month)

        if not newText[i].isalpha() and newText[i] != " " and final[1] != "" and int(newText[i]) > int(final[1])  :
            final[2] = str(newText[i])

        if not newText[i].isalpha() and newText[i] != " " and final[1] == "":
            final[0] = newText[0]

    harshCode = text.split()
    hardCode = {"eleven":11, "twelve":12, "thirteen":13, "fourteen":14, "fifteen":15,
        "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19}

    for i in range(1,len(harshCode)):
        if harshCode[i-1] == "twenty" and harshCode[i] in hardCode and hardCode[harshCode[i]] > 10 and hardCode[harshCode[i]] < 20:
            final[2] = str(20*100 + hardCode[harshCode[i]])


    date = "/".join(final)
    #print(date)
    return (datetime.strptime(date, '%d/%m/%Y'))


 
#This function read the data (grade score, course score, time of task ) 
#from the text that user gives it, and then returns the data as float
def get_data(text):

    text = text2int(text).split()
    reult = ""
    #print(text)
    for i in range(1 , len(text)):
        if not text[i - 1].isalpha() and text[i - 1] != " ":

             result = float(text[i - 1]) 

        if not text[i].isalpha() and text[i - 1] != " ":
            result = float(text[i])

        if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "minutes" or text[i] == "minute" ):

            return float(text[i - 1]) / 60

        if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "days" or text[i] == "day" ):

            return float(text[i - 1]) * 24

        if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "hours" or text[i] == "hour" ):
        
            return float(text[i - 1])

    return result

    

#get the name of the task
def get_taskName(text):

    text = text.split()
    j = 0;
    for i in text:
        if i == "add":
            #print(" ".join(text[text.index("add") + 1:]))
            return " ".join(text[text.index("add") + 1:])



#this function returns the diff between the time you have and how long the task will need to be done
def get_taskTime(due, deadLine):

    currentTime = datetime.now()

    deff = 8765.81277 *(deadLine.year - currentTime.year) + 730.484398 *(deadLine.month - currentTime.month) + 24*(deadLine.day - currentTime.day) +(deadLine.hour - currentTime.hour) 
    #print(deff)
    
    if deff <=  0:

         return "missed"

    deff2 = deff - due

    return deff2





#this task returns how many perscentage you have until you drop to lower grade
def get_taskGrade(gradeTask, courseGrade):

    howMuch = courseGrade % 10 
    return   howMuch - (courseGrade - (courseGrade - gradeTask))





#This function gives you the score for each task
def give_score( due, taskTime, taskGrade):

    if taskTime == 0 or ((- 1 * taskTime) / due)*100 >= 80 :

        taskTime = 400

    elif 0 < taskTime and taskTime < 24:

        taskTime = 350

    elif 24 <= taskTime and taskTime < 48:

        taskTime = 300

    elif 48 <= taskTime and taskTime < 72:

        taskTime =250

    elif 72 <= taskTime and taskTime < 96:

        taskTime = 200

    elif 96 <= taskTime and taskTime < 120:

        taskTime = 150

    elif 120 <= taskTime and taskTime < 144:

        taskTime = 100

    elif 144 <= taskTime and taskTime < 168:

        taskTime = 50

    elif  taskTime == "missed" or taskTime >= 168 :

        return 0

    else:

        taskTime == 200


    if taskGrade < 0 :

        taskGrade = 500

    elif 9 <= taskGrade :

        taskGrade = 50

    elif  8 <= taskGrade and taskGrade < 9:

        taskGrade = 100

    elif 7 <= taskGrade and taskGrade < 8:

        taskGrade = 150

    elif 6 <= taskGrade and taskGrade < 7:

        taskGrade = 200

    elif 5 <= taskGrade and taskGrade < 6:

        taskGrade = 250

    elif 4 <= taskGrade and taskGrade < 5 :

        taskGrade = 300

    elif 3 <= taskGrade and taskGrade < 4:

        taskGrade = 350

    elif 2 <= taskGrade and taskGrade < 3:

        taskGrade = 400

    elif 1 <= taskGrade and taskGrade < 2:

        taskGrade = 450

    else:

        taskGrade == 250

    #print(taskGrade + taskTime)
    return taskGrade + taskTime
    


#This function taks a file that contains a text file that has the tasks
#then it adds the new task and reorder the list, then rewrite the file with the updated list
#then returns a dict with the list
def update_list(taskName, taskScore, deadline):

    dataBase = open("/Users/sshaar/hackathon/frontend/theme/backend/tasks.txt")
    line = dataBase.readline()
    while line == "\n":

        line = dataBase.readline()

    tasks = {}
    tasks2 = {}
    while line:
        
        while line == "\n":
            line = dataBase.readline()
        
        task = ""
        score = ""
        counter = 0

        for i in line:

            

            if counter == 1 and i != "@" and i != "\n":

                #print(i)
                score += i

            if i == "@":
                counter += 1

            if counter < 1:
                #print(i)
                task += i 


        tasks[task] = float(score)
        line = dataBase.readline()

    if taskName in tasks:
        tasks[taskName] = taskScore

    else:
        tasks[taskName] = taskScore  

    
    tasks = [(k, tasks[k]) for k in sorted(tasks, key=tasks.get, reverse=True)]


    dataBase = open("/Users/sshaar/hackathon/frontend/theme/backend/tasks.txt" , "w")
    for key , value in tasks:
        dataBase.seek(0,2)
        dataBase.write(key + "@" + str(value) + "\n")

   # print(tasks)
    return tasks


#update_list("Math Homework 3" , 740, get_deadline(" twenty fifth of april"))

#This function takes a text and parse it to get what you should search for
def parse_to_search(text):

    newText = text.split()
    question = ["what", "when", "where", "which", "who", "whom", "whose", "why", "how", "find"]
    asking = ["searchfor", "lookfor", "lookup", "canyou", "tellme", " giveme", "get" , "showme"]
    i = 0
    while  i < len(newText) and newText[i].lower()  not in  question  :
        i += 1;


    if i >= len(newText) :
        j = 1
        while  j < len(newText) and newText[j - 1].lower()  + newText[j].lower() not in  asking:
            j += 1

    j = 1

    while  j < len(newText) and newText[j - 1].lower()  + newText[j].lower() not in  asking:
            j += 1

    if i < len(newText): 
        return " ".join(newText[i:])

    elif j < len(newText):
        return " ".join(newText[j + 1:])

    return " ".join(newText[:])