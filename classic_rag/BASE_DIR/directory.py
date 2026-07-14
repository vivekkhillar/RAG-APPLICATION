from os import path
from pathlib import Path

class Directory():

    def __init__(self) -> None:
        self.directory = None
    
    def dir(self):
        base_dir = Path(__file__).resolve().parent.parent        
        return base_dir


if __name__ =="__main__":

    Directory = Directory()
    base_dir = Directory.dir()
    print(base_dir)
