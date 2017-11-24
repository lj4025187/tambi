# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sqlite3

class Apokryphs(object):
    def __init__(self):
        pass
    
    def initDbConnection(self):
        self.connection = sqlite3.connect("./modules/apokryphs/.db")
        self.cursor = self.connection.cursor()
         
    def getCommands(self):
        return {
            "apokryphs.word" : self.word,
            
        }
    
    def interpreter(self, command, args, queue):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module quran")
    
    def commands(self, none1, none2):
        dic = self.getCommands()
        
        commands = sorted(dic.items())
        
        all_commands = []
        for key in commands:
            line = str(key).split(",")[0]
            all_commands.append(str(line[2:-1]))
            
        result_object = Result()
        result_object.category = "list"
        result_object.payload = all_commands
        return result_object
    
    def word(self, c, args):
        result_object = Result()
        result_object.category = "text"
        
        if len(args) > 0 and args[0] == 'henoch':
            result = self.henoch(args)
            
        
        return result_object
    
    
