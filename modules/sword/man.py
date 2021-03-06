
module_description = """
Module for reading the bible modules provided by the sword project. For installing bibles, use the "Module Manager" user inerface in the "Sword"-menu.

For getting started, you can try the command "sword.commands" for an overview of the commands provided by the "sword" module, and of course "man sword.[command]" for getting a description of the given command.

Additionally, this module provides some user-inerfaces available in the "Sword"-menu entry.
"""

books = """
Returns a list of the bible books. This names can be used to specify the book in the command 'sword.word'.

@param (optional): [string], 'ot' or 'nt': list only the books of the old or new testament.

See also:
sword.word
"""

aliases = """
Look at the command 'sword.books' ...
"""

canons = """
List the bible canons which are available here.

See also:
sword.getCanon
sword.setCanon
"""

getCanon = """
Shows which canon is currently used for the bible structure

See also:
sword.canons
sword.setCanon
"""

setCanon = """
Sets the canon to be used for the bible structure

@param (required): [string], the name of the canon to be used.

Examples:
sword.setCanon calvin

See also:
sword.canons
sword.getCanon
"""

word = """
Returns the specified bible passage.

@param (required): [string], the name of the book we want to read. (If it contains spaces, put it between double quotation marks).
@param (required): [number], the chapter of the book we want to read.
@param (optional): [number] or [number]-[number], the verse or a range of verses to be shown.

Examples:
sword.word genesis 1
sword.word genesis 1 1
sword.word genesis 1 10-20
sword.word "I Samuel" 1
"""

modules = """
Returns a list of all installed sword modules.

@param (optional): [string], the language code we want to list the according bible translations (=sword modules) for.

Examples:
sword.modules de (returns all german translations)
"""

getModule = """
Returns the name of the currently active sword module.
"""

setModule = """
Sets the active sword module from where the sword.word command is reading from.

@param (required): [string], the name of the sword module to be active

Examples:
sword.setModule GerNeUe (for activating the bible translation named 'GerNeUe')

See also:
sword.modules
sword.languages
"""

languages = """
Lists the language codes for wich at least one translation (=sword module) is installed.
"""
