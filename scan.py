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
        try:
            for path in paths:
                for infile in os.listdir(path):
                    if os.path.isdir(os.path.join(path, infile)):
                        if logger: logger("Entered scanFolder in Scanner")
                        
                        files.append(unicode(infile, 'utf-8'))
        except OSError:
            files.append(unicode('The folder: ' + path + ' does not exist.', 'utf-8'))
        return files
