'''This class is for testing the oop file implementation'''

#version 1

import os
class File:
    def __init__(self, path):
        self.path = path

    def getSize(self):
        if not os.path.isdir(self.path):
            return
        name_list = os.listdir(self.path)
        size = 0
        for files in name_list:
            pathIndex = f'{self.path}/{files}'
            if os.path.isdir(pathIndex):
                size += File(pathIndex).getSize()
            else:
                size += os.path.getsize(pathIndex)
        return size






