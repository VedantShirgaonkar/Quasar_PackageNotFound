# Integrate all the Funcitons in a Single File and Make it Menu Driven 
from mcq_generator import generateMCQ,convertToJSON

# Generating MCQ from the User Domain Request and the Number of Questions Involved

domain=input("Enter Your Domain: ")
numOfQuestions=int(input("Enter the number of Questions : "))


mcq_text=generateMCQ(domain,numOfQuestions)

filePath=input("Enter the File Path to Store the Data :")
# Try Converting this Questions in JSON format 
convertToJSON(mcq_text,filePath)