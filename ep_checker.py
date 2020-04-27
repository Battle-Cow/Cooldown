import os
import csv

CHECK_VALUE = 2000

def parse_csv(line):
    
    if len(line) == 6: # Check for length of 6, some CSV lines are invalid
                
        character = {
            "name": parsedLine[0],        
            "class": parsedLine[1],
            "rank": parsedLine[2],
            "ep": parsedLine[3],
            "gp": parsedLine[4],
            "pr": parsedLine[5]
        }
             
        return character

# Save filenames here
fileNameList = []

for file in os.listdir("."):
   
    if file.endswith(".json"):
        fileNameList.append(file)

# Sort them in ascending order
fileNameList.sort()

previousList = [] # Previous file
previousLog = [] # Previously parsed data
previousFileName = ""

for fileName in fileNameList:
    
    file = open(fileName, "r", encoding="utf-8")
    temporaryList = [] # Holds all lines from the JSON file
    
    for line in file:
        temporaryList.append(line)
    
    # Remove any trailing whitespaces
    temporaryList = [line.strip(" ") for line in temporaryList]

    parsedList = [] # Contains only the CSV strings
    
    for line in temporaryList:
        # Find each CSV line and remove all bracket squares
        if line.startswith("["):
            line = line.replace("[", "")
            line = line.replace("],", "")
            line = line.replace("]", "")
            line = line.replace(" ", "")
            line = line.replace('"', "")
            line = line.replace("\n", "")
            parsedList.append(line)
            
    # Check if the previous list is not empty
    if previousList:
        for line in previousList:
            
            # Split each column via the comma
            parsedLine = line.split(",")
            # Convert the list into a dictionary
            previousLog.append(parse_csv(parsedLine))
        
        currentLog = []
        
        for line in parsedList:
            
            # Split the column via the comma
            parsedLine = line.split(",")
            # Convert the list into a dictionary
            currentLog.append(parse_csv(parsedLine))
        
        # Use list comprehension to remove None valeus from both lists
        previousLog = [line for line in previousLog if line]
        currentLog = [line for line in currentLog if line]
        
        # Iterate through the previous character dictionary and compare to the current dictionary
        for previousCharacter in previousLog:
            
            name = previousCharacter["name"]
            previousEP = int(previousCharacter["ep"])
         
            # Now, slooowly, go through the current dictionary searching for this name and compare the EP
            for currentCharacter in currentLog:
                
                if currentCharacter["name"] == name:
                    
                    currentEP = int(currentCharacter["ep"])
                    epDifference = currentEP - previousEP
                    
                    # Check if the EP difference is greater than the set CHECK_VALUE
                    if epDifference > CHECK_VALUE:
                       
                        print("Comparing logs " + previousFileName + " with " + fileName + "\n" 
                            + "\n" + "Character: " + currentCharacter["name"] + "\n"
                            + "Current EP: " + str(currentEP) + "\n"
                            + "Previous EP: " + str(previousEP)
                            + "\n" + "EP Difference: " + str(epDifference) + "\n")
                        
                    break
        
        # Move the comparsion forward
        previousList = parsedList 
        previousFileName = fileName
        # Reset the logs
        previousLog = []
        currentLog = []
        
    else: 
        previousList = parsedList
        previousFileName = fileName

