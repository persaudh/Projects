import sys
import os
from PIL import Image

class Convert:
    def __init__(self, oldPath, newPath):
        self.oldPath = oldPath
        self.newPath = newPath

    def createNewPath(self):
        if(not os.path.exists(self.newPath)):
            os.mkdir(self.newPath)

    def getFileName(self,file:str):
        name = file.split(".")
        print(name[0])
        return f"{name[0]}.png"
    
    def copyOld(self):
        directory = os.fsencode(self.oldPath)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if(filename.endswith("jpg")):
                filepath = os.path.join(self.oldPath,filename)
                image = Image.open(filepath)
                name = self.getFileName(filename)
                newfilePath = os.path.join(self.newPath,name)
                image.save(newfilePath,"PNG")
                print(f"Copied {filepath} to {newfilePath}")

def get_script_path():
    return os.path.dirname(os.path.relpath(sys.argv[0]))

if __name__ == "__main__":
    print("Starting...")
    currentPath = get_script_path()
    try:
        if(len(sys.argv) > 2):
            arg1 = sys.argv[1]
            arg2 = sys.argv[2]
            print(arg1,arg2)
            oldPath = os.path.join(currentPath,arg1)
            newPath = os.path.join(currentPath,arg2)
            if(os.path.exists(oldPath)):
                convert = Convert(oldPath=oldPath,newPath=newPath)
                if(not os.path.exists(newPath)):
                    convert.createNewPath()
                convert.copyOld()          
            else:
                print(f"Path not found: {oldPath}")
        else: 
            print("Invalid Paramaters")
    except IndexError:
        print("Invalid Paramaters")

   
    