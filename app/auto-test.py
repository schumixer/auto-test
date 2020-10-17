from classes import *
def main():
   #read data
   modelData = Data.readData('model')
   studentData = Data.readData('student')
   names = Data.readNames("names")
   resultData = Data.chooseDirectory("result")

   #check out all the students
   students = []

   for file in studentData["files"]:
      with open(f"{studentData['dir']}/{file}", encoding="utf8") as studentFile:
         studentLines = studentFile.readlines()
         configure = studentLines[0] = studentLines[0].strip()
         fullName = studentLines[1] = studentLines[1].strip()

         if fullName in names:
            isExist = False
            studentsNumber = len(students)
            for i in range(len(students)):
               if fullName == students[i].fullName:
                  studentsNumber = i
                  isExist = True
                  break
            if not isExist:
               students.append(Student(fullName))
            
            if configure in Data.TruncateExtensions(copy.copy((modelData["files"]))):
               with open(f"{modelData['dir']}/{configure+'.txt'}", encoding="utf8") as modelFile:
                  modelLines = modelFile.readlines()

                  isRight = True


                  if(len(studentLines)==len(modelLines)+2):

                     for i in range(len(modelLines)):

                        if studentLines[i+2].strip()!=modelLines[i].strip():
                           students[studentsNumber].currentResults[configure]="-"
                           isRight = False
                           break

                     if isRight:
                        students[studentsNumber].currentResults[configure]="+"

                  else: 
                     students[studentsNumber].currentResults[configure]="-"

            else:
               students[studentsNumber].currentResults[configure]="-"

   #addition undone configures
   for i in range(len(students)):
      for item in Data.TruncateExtensions(copy.copy((modelData["files"]))):
         if item not in students[i].currentResults.keys():
            students[i].currentResults[item]="-"
   
   #calculating finished results
   for i in range(len(students)):
      students[i].calculateFinishResult(len((modelData["files"])))



   #write data
   Data.writeData(students, modelData, resultData)
if __name__ == '__main__':
   main()
