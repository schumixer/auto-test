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
            tempList[i]=tempList[i][0].upper()
        return tempList
    
    @staticmethod
    def readData(titleName):
        dir = Data.chooseDirectory(titleName)

        files = []
        for root, dirs, tempFiles in os.walk(dir):  
            for fileName in tempFiles:
                if fileName.endswith('.txt'):
                    files.append(fileName)

        if titleName == 'model':
            with open(dir+"/"+"version.txt", encoding="utf8") as f:
                Data.version = f.read().strip()
                files.remove("version.txt")

        return {"dir":dir, "files":files}

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
        df.to_excel(resultData+"/output.xlsx") 
