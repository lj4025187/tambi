
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from pysword.modules import SwordModules
from pysword.books import BibleStructure

#from modules.bituza.bituza import Bituza

class Sword(object):
    
    current_module = 'GerNeUe'
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "sword.commands": self.commands,
            
            "sword.books": self.books,
            
            "sword.word": self.word,
            
            "sword.modules": self.listModules,
            "sword.getModule": self.getCurrentModule,
            "sword.setModule": self.setCurrentModule,
            
            "sword.languages" : self.listLanguages,
            }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        print("not found in SWORD")
        raise CommandNotInThisModule("command not found in module sword")
    
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
    
    def listModules(self, c, args):
        modules = SwordModules()
        found_modules = modules.parse_modules()
        
        result = []
        for key in found_modules:
            row = []
            row.append(key)
            
            #for item in found_modules[key]:
            #    row.append(found_modules[key][item])
            row.append(found_modules[key]['lang'])
            row.append(found_modules[key]['about'].replace('\par', "\n"))
            
            if len(args) == 1:
                category = "itemized"
                if found_modules[key]['lang'] == args[0]:
                    result.append(row)
            else:
                category = "table"
                result.append(row)
        
        result_object = Result()
        result_object.category = category
        result_object.payload = sorted(result)
        return result_object
    
    def listLanguages(self, c, a):
        result = []
        
        modules = SwordModules()
        found_modules = modules.parse_modules()
        for main_key in found_modules:
            language = found_modules[main_key]['lang']
            #for sub_key in found_modules[main_key]:
            #    language = found_modules[main_key][sub_key]
            
            if not language in result:
                result.append(language)
        
        result = sorted(result)
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = result
        return result_object
    
    def getCurrentModule(self, c, a):
        result_object = Result()
        result_object.category = "list"
        result_object.payload = self.current_module
        return result_object
    
    def setCurrentModule(self, c, args):
        self.current_module = args[0]
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = 'module set to: ' + args[0]
        return result_object
    
    def books(self, c, args):
        structure = BibleStructure('default')
        books = structure.get_books()
        result = []
        
        if ((not len(args) == 0) and (args[0] == 'ot')) or (len(args) == 0):
            for book in books['ot']:
                formatted = str(book)[5:][:-1]
                result.append(formatted)
        if ((not len(args) == 0) and (args[0] == 'nt')) or (len(args) == 0):
            for book in books['nt']:
                formatted = str(book)[5:][:-1]
                result.append(formatted)
        print(result)
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = result
        return result_object
    
    def word(self, c, args):
        result_object = Result()
        result = None
        
        modules = SwordModules()
        try:
            found_modules = modules.parse_modules()
        except FileNotFoundError:
            result_object.error = 'no sword modules found on this computer. please install some!'
        else:
            try:
                bible = modules.get_bible_from_module(self.current_module)
                
                try:
                    book = args[0]
                    
                    import modules.sword.book_names.books_de as books_de
                    if book in books_de.books:
                        book = books_de.books[book]
                    
                    if len(args) == 2:
                        result = bible.get(books=[book], chapters=[int(args[1])], clean=True, join='#|#')
                        
                        splitted = result.split('#|#')
                        result = []
                        for i, line in enumerate(splitted):
                            result.append([i+1, line.strip()])
                    
                    elif args[2].find('-') > -1:
                        verse_min, verse_max = args[2].split('-')
                        verse_range = range(int(verse_min), int(verse_max)+1)
                        
                        try:
                            result = bible.get(books=[book], chapters=[int(args[1])], verses=verse_range, clean=True, join='#|#')
                        except IndexError:
                            result_object.error = 'invalid verse range'
                        else:
                            splitted = result.split('#|#')
                            result = []
                            for i, line in enumerate(splitted):
                                result.append([i+int(verse_min), line.strip()])
                    else:
                        verse_range = int(args[2])
                        
                        result = bible.get(books=[book], chapters=[int(args[1])], verses=verse_range, clean=True, join='\n')
                except ValueError as e:
                    result_object.error = str(e)
                except KeyError:
                    result_object.error = 'book not found in current bible: '+str(book)
            except KeyError:
                result_object.error = 'current module does not exist: '+self.current_module
        
        result_object.category = "text"
        if result:
            result_object.payload = result
        return result_object
