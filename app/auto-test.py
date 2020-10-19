from classes import *
def main():
   #read data
   modelData, studentData, names, resultData = Data.input()

   #edit data
   students = Main.mainFunction(modelData, studentData, names, resultData)

   #write data
   Data.writeData(students, modelData, resultData)

if __name__ == '__main__':
   main()
