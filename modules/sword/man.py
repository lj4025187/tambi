
module_description = """
Module for reading the bible modules provided by the sword project. There is no download functionality for new modules yet, please use any other sword-frontend for doing this (like bibletime, xiphos or whatsoever).
"""

word = """
Returns the specified bible passage.

@param (required): [string], the name of the book we want to read.
@param (required): [number], the chapter of the book we want to read.
@param (optional): [number] or [number]-[number], the verse or a range of verses to be shown.

Examples:
sword.word genesis 1
sword.word genesis 1 1
sword.word genesis 1 10-20
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
Sets the active sword module the sword.word command is reading from.

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
