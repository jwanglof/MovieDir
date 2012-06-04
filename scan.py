# -*- coding: utf-8 -*-
import os
import re

logger = True

def logger(str):
    loggerBreaker = "HELPER: "
    print loggerBreaker + str
    
class Scanner:
    def __init__(self):
        if logger: logger("Instance of Scanner created")
    
    def scanFolder(self, paths):
        files = []
        folders = {}
        try:
            for path in paths:
                path = path.rstrip()
                for infile in os.listdir(path):
                    if os.path.isdir(os.path.join(path, infile)):
                        if logger: logger("Entered scanFolder in Scanner")
                        
                        files.append(unicode(infile, 'utf-8'))
                folders[path] = files
                files = []
        except:
            #files.append(unicode('The folder does not exist.', 'utf-8'))
            folders['Error'] = [unicode('One specified folder does not exist. Please check your path\'s so they are correct.', 'utf-8')]
        return folders

    def setFolders(self, file, folders):
        print os.path.isfile(file)
        try:
            if os.path.isfile(file):
                f = open(file, 'w')
                
                #f.write(folders.splitlines().str())
                
                for folder in folders.splitlines():
                    f.write('%s\n' % folder)
                    print folder
                f.close()
                return True
        except IOError:
            print IOError
            return False
        
    def getFolders(self, file):
        folders = []
        try:
            if os.path.isfile(file):
                f = open(file)
                for line in f:
                    folders.append(line)
                f.close()
        except:
            folders.append("NOOOOPE")
        return folders
        
