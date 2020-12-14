import os
import sys

def main(version: str, directory: str) -> None:

    directories = os.listdir(directory)
    
    for directory in directories:    
        
        path = "./dist_conda/{}/poetic-py-{}-py37_0.tar.bz2".format(directory, version)
        command = "anaconda upload " + path
        os.system(command)
        
               
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])