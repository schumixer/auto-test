from imports import *
class Student:
    def __init__(self, fullName):
        self.currentResults ={}
        self.finishResult = "0%"
        self.fullName = fullName
    def calculateFinishResult(self,necessaryLen):
        if len(self.currentResults)!=necessaryLen:
            self.finishResult = "0%"
        else:
            self.finishResult = "100%"
        for key in self.currentResults:
            if self.currentResults[key]=="-":
                self.finishResult = "0%"
                break


class Data:
    titles = {
                "names":"Please select the file with names of the students",
                "model":"Please select the model directory", 
                "student":"Please select the students directory",
                "result": "Please select the result directory"
             }
    version = ""
    columns = ["ФИО","Номер лабы"]
    outputFileName = "output.xlsx"
     
    @staticmethod
    def chooseDirectory(titleName):
        Tk().withdraw()
        return askdirectory(title=Data.titles[titleName])



    @staticmethod
    def chooseFile(titleName):
        Tk().withdraw()
        return askopenfilename(title=Data.titles[titleName])

    @staticmethod
    def readNames(titleName):
        file = Data.chooseFile(titleName)
        tempList =  pd.read_excel(file, index_col=None, header=None).values.tolist()
        for i in range(len(tempList)):
            tempList[i]=Main.replaceSym(tempList[i][0].upper())
        return tempList
    
    @staticmethod
    def readData(titleName):
        dir = Data.chooseDirectory(titleName)

        files = []
        for root, dirs, tempFiles in os.walk(dir):  
            for fileName in tempFiles:
                lowerCaseFileName = fileName.lower()
                if lowerCaseFileName.endswith('.txt'):
                    files.append(fileName)

        if titleName == 'model':
            with open(dir+"/"+"version.txt",encoding='cp437') as f:
                Data.version = f.read().strip()
                files.remove("version.txt")

        return {"dir":dir, "files":files}

    @staticmethod
    def input():
        return (Data.readData('model'), Data.readData('student'),
                Data.readNames("names"), Data.chooseDirectory("result"))
    
    @staticmethod
    def TruncateExtensions(lines):
        for i in range(len(lines)):
            (prefix, sep, suffix) = lines[i].rpartition('.')
            lines[i] = prefix
        return lines
    
    @staticmethod
    def writeData(students, modelData, resultData):
        for configure in Data.TruncateExtensions(copy.copy((modelData["files"]))):
            Data.columns.append(configure)
        Data.columns.append("Итог")

        data = []
        for student in students:
            row = [student.fullName, Data.version]
            for configure in Data.TruncateExtensions(copy.copy((modelData["files"]))):
                row.append(student.currentResults[configure])
            row.append(student.finishResult)
            data.append(row)

        df = pd.DataFrame(data,columns=Data.columns, index = np.arange(1,len(students)+1))
        df.to_excel(resultData+f"/{Data.outputFileName}")






class Main():
   @staticmethod
   def chooseEncoding(file):
      with open(file,"rb") as f:
          text=f.read()
          enc = chardet.detect(text).get("encoding")
          if enc.lower() == "maccyrillic":
              enc = "windows-1251"
          return enc
    
   @staticmethod
   def deleteEmptyLines(studentLines):
       newStudentLines = []
       for item in studentLines:
           if item.strip()!='':
               newStudentLines.append(item.strip())
       return newStudentLines

   @staticmethod
   def replaceSym(string):
       return string.replace("Ё","Е") 
        
   @staticmethod
   def checkRightName(name):
       return name!="#"


   @staticmethod
   def mainFunction(modelData, studentData, names, resultData):
      #initialising all the students from the excel file
      students = []
      for name in names:
         students.append(Student(name))
      
      #checkRightName = True
      #check out all the students
      for file in studentData["files"]:
         #opening the file with students works
         encodingResult=Main.chooseEncoding(f"{studentData['dir']}/{file}")
         
         with open(f"{studentData['dir']}/{file}",encoding=encodingResult) as studentFile:
            studentLines = Main.deleteEmptyLines(studentFile.readlines())
            configure = studentLines[0]
            fullName = studentLines[1] = Main.replaceSym(studentLines[1].upper())
            #checkRightName = Main.checkRightName(configure)
            #if name of the student was in excel file
            if fullName in names:
               #isExist = False
               studentsNumber = len(students)
               for i in range(len(students)):
                  if fullName == students[i].fullName:
                     studentsNumber = i
                     #isExist = True
                     break
               # if not isExist:
               #    students.append(Student(fullName))
               
               if configure in Data.TruncateExtensions(copy.copy((modelData["files"]))):
                  #opening the file with model works
                  with open(f"{modelData['dir']}/{configure+'.txt'}",encoding="cp437") as modelFile:
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
         students[i].calculateFinishResult(len(modelData["files"]))
      
      return students

