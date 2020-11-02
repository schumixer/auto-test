from classes import *
def main():
   #read data
   try:
      modelData, studentData, names, resultData = Data.input()
   except:
      print("read data error:", sys.exc_info()[0])
      sys.exit(1) # exiing with a non zero value is better for returning from an error
   #edit data
   try:
      students = Main.mainFunction(modelData, studentData, names, resultData)
   except:
      print("edit data error:", sys.exc_info()[0])
      sys.exit(1) # exiing with a non zero value is better for returning from an error
   #write data
   try:
      Data.writeData(students, modelData, resultData)
   except:
      print("write data error:", sys.exc_info()[0])
      sys.exit(1) # exiing with a non zero value is better for returning from an error
if __name__ == '__main__':
   main()
