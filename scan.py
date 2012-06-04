# -*- coding: utf-8 -*-
import os
import re

# Set to false to turn of debugger
logger = True

def logger(str):
    loggerBreaker = "HELPER: "
    print loggerBreaker + str
    
class Scanner:
    def __init__(self):
        if logger: logger('Instance of Scanner created')
    
    def scanFolder(self, paths):
        files = []
        folders = {}
        try:
            for path in paths:
                path = path.rstrip()
                for infile in os.listdir(path):
                    if os.path.isdir(os.path.join(path, infile)):
                        if logger: logger('Entered scanFolder in Scanner')
                        
                        files.append(unicode(infile, 'utf-8'))
                folders[path] = files
                files = []
        except:
            folders['Error'] = [unicode('One specified folder does not exist. Please check your path\'s so they are correct.', 'utf-8')]
        return folders

    def setFolders(self, file, folders):
        if logger: logger('Entered setFolders in Scanner')

        try:
            if os.path.isfile(file):
                f = open(file, 'w')
                
                for folder in folders.splitlines():
                    f.write('%s\n' % folder)
                    print folder
                f.close()

                return True
        except IOError:
            if logger: logger('IOError in setFolders!\nError: ' + IOError)
            return False
        
    def getFolders(self, file):
        if logger: logger('Entered getFolders in Scanner')
        
        folders = []
        try:
            if os.path.isfile(file):
                f = open(file)
                for line in f:
                    folders.append(line)
                f.close()
        except:
            if logger: logger('Error in getFolders!')
            folders.append("NOOOOPE")
        return folders
        
