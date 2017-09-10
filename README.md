# WrapIt
Sublime Text 3 plugin to easily wrap a text selection in predefined code blocks.

## WhatFor?
- Want to surround a selection with brackets? Easy. __Just WrapIt!__
- Need to have these few lines inside an if-else block. It's fun. __Just WrapIt!__
- Like to join several functions into a class declaration? No problem. __Just WrapIt!__
- Want to ... I think you get it! __Just WrapIt!__ ;-)

## Installation
Just use PackageControl. I am not going to explain here how to use it. 

##  Usage
### Wrapping
1. Put your cursor anywhere, or select some text then hit <kbd>alt</kbd>+<kbd>w</kbd>.
2. The quick panel will open giving you a range of code structure for wrapping your text with.
3. Once you chose one, your text will rapidly get embedded into the selcted code structure.
4. _Like in any snippets you can use <kbd>tab</kbd> to move between different regions of that code to successively fill it._

### Defining custom wrappers
By default WrapIt comes with templates for PHP, Python, JavaScript and JSON. You can extend the user settings file with custom templates for any syntax. Like so:

        "definitions":[
                        { 
                          "name":"Python",
                          "syntaxes": [
                            "Packages/Python/Python.sublime-syntax",
                            "Packages/Python 3/Python3.tmLanguage",
                            "Packages/Python Improved/PythonImproved.tmLanguage",
                            "Packages/MagicPython/grammars/MagicPython.tmLanguage"
                          ],
                          "wrappers": [
                            {
                              "name": "if / else",
                              "description": "Wrap with: if - else block",
                              template":"\nif ${1}:\n\t<sel>\nelse:\n\t${2}"
                            }
                          ]
                        }
                      ]
1. Copy definitions from to default to user settings file of the WrapIt package.
2. Either extend an existing language or define a new one.
3. "name" - name of language e.g. PYthon
4. "syntaxed" - array of paths to .tmLanguage files for that language
5. "wrappers" - array of objects for defining code blocks
- code block -
6. "name" - name code block (label for quick panel)
7. "descriptions" - one sentence descriptin of code block (sublabl for quick panel)
8. "template" - template definition

Note: Both "name" and "template" must be filled or the respective code block will not be listed in the quick panel.


#### templating
- `<sel>` - where your selection should be placed
- `\n` - new line
- `\t` - indent for line, if preceeding <sel> tag, all lines of a multiline selection will get indented
- `${x}` - regions for <kbd>tab</kbd> navigation, just like in snippets

## Custom keybinding
As an alternative to the qick panel, commonly used wrapping can be bound to own key combination.
In your user keybindings file, do:

        {"keys": [ YOUR KEY COMBINATION ],
        "command": "wrap_it",
        "args": { NAME OF CODE BLOCK},
        "context": [SPECIFY SYNTAX HERE]},

## Contributors
- lattespirit: original idea, primordial version called sublime-wrapper.
