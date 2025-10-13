#!/usr/bin/python
"""Step by step sample for building an interface that displays a list
of files in the specified directory, and displays the contents of the
file in the lower portion of the window ('non-object-oriented' version).
"""

# import Tkinter module to have access to Tk wrapped widgets
import Tkinter

# import Tkconstants to module scope for ease of use
from Tkconstants import *

# import the operating system module
import os

# import a local module we created for Tkinter GUI convenience functions
import tkinterGui

# define globals for managing the lists and current working directory
# (these become members of an object in the object-oriented version)
_selectedDirectory = None
_dirList   = None
_fileList  = None
_gotoEntry = None

def _setCWD(cwd):
    """Updates the user interface with specified current working directory"""
    if not cwd or not os.path.isdir(cwd):
        return
    _selectedDirectory.set(cwd)
    _gotoEntry.delete(0, END)
    _gotoEntry.insert(0, cwd)
    _setEntries()
        

def _setDirectory(*unused):
    """Event callback connected to GoTo button and text entry at top of gui"""
    _setCWD(_gotoEntry.get())
    

def _showDirectory(*unused):
    """Event callback connected to the directories list item selection"""
    selectedDirectory = _dirList.getSelection()
    if not selectedDirectory:
        return
    
    cwd = _selectedDirectory.get()
    if selectedDirectory == os.pardir:
        cwd = cwd[:cwd.rfind(os.sep)]
    else:
        if cwd.endswith(os.sep):
            cwd = cwd[:-1]
        cwd += os.sep + selectedDirectory

    _setCWD(cwd)


def _bindEvents():
    """Binds mouse and keyboard events to respond to gui events"""
    
    # bind double-click mouse event on directory list to show the directory
    _dirList.bind('<Double-Button-1>', _showDirectory)
    _gotoEntry.bind('<Return>',        _setDirectory)

    
def _buildTextDisplay(unused):
    """NOTE: decided to do the object-oriented version at this point,
    so no real impl for the display functionality in this module
    """
    return Tkinter.Frame()
    

def _setEntries():
    """Sets the names of the files and directories in the lists"""
    if not _selectedDirectory.get():
        _selectedDirectory.set(os.getcwd())

    cwd   = _selectedDirectory.get()
    files = []
    dirs  = []
    for e in os.listdir(cwd):
        if os.path.isdir(os.path.join(cwd, e)):
            dirs.append(e)
        else:
            files.append(e)

    # sort the lists
    dirs.insert(0, os.pardir)  # always include the parent directory
    dirs.sort()
    files.sort()

    # populate the list boxes with their respective entries
    _dirList.delete(0, END)
    _dirList.insert(0, *dirs)
    _fileList.delete(0, END)
    _fileList.insert(0, *files)


def _buildCWDFrame(topLevel):
    """Builds the current working directory frame at top of GUI"""
    global _selectedDirectory, _gotoEntry
    cwdFrame = Tkinter.Frame(topLevel, name='cwdFrame')
    tkinterGui.anchor(cwdFrame, 2, 2)

    Tkinter.Label(cwdFrame, name='cwdLabel').grid(row=0, col=0, sticky=W)
    
    # create the label's variable that will store the name of the cwd
    _selectedDirectory = Tkinter.StringVar()
    # set the string variable's value with name of current working directory
    _selectedDirectory.set(os.getcwd())
    # bind the label on the frame with the string variable
    Tkinter.Label(cwdFrame, name='cwdStringVar',
                  textvariable=_selectedDirectory).grid(row=0, col=1, sticky=W)

    # add a button to allow the user to 'GoTo' a specified directory
    Tkinter.Button(cwdFrame, name='cwdButton',
                   command=_setDirectory).grid(row=1, col=0, sticky=W)
    _gotoEntry = Tkinter.Entry(cwdFrame, name='cwdEntry')
    _gotoEntry.grid(row=1, col=1, sticky=E+W)
    
    return cwdFrame


def _buildListFrame(topLevel):
    """create the frame that contains list of files and text entry"""
    global _dirList, _fileList
    
    # create labels for file and directory list
    listrows = 5
    listFrame = Tkinter.Frame(topLevel, name='listFrame')
    tkinterGui.anchor(listFrame, listrows, 2)

    row = 0
    Tkinter.Label(listFrame, name='dirLabel' ).grid(row=row, col=0, sticky=NW)
    Tkinter.Label(listFrame, name='fileLabel').grid(row=row, col=1, sticky=NW)
    row += 1

    # create the listbox for directories in specified directory
    _dirList = tkinterGui.SelectableList(listFrame, 'dirList', row, 0, listrows)
    _dirList.setCommand(_showDirectory)

    # create the listbox for filenames in specified directory
    _fileList = tkinterGui.SelectableList(listFrame, 'fileList', row, 1, listrows)

    # include a row for the horizontal scrollbars
    row += listrows

    # create the save as filename label and entry
    row += 1
    Tkinter.Label(listFrame, name='entryLabel').grid(row=row, col=0, sticky=NW)
    row += 1
    Tkinter.Entry(listFrame, name='fileEntry').grid(row=row, col=0, sticky=EW,
                                                    columnspan=2)

    return listFrame


def buildGui(topLevel):
    """Main function that organizes how the GUI is built"""
    _buildCWDFrame(topLevel).grid( row=0, col=0, sticky=NSEW)
    _buildListFrame(topLevel).grid(row=1, col=0, sticky=NSEW)

    # set the list of files and directories in current directory
    _setEntries()

    # build the bottom portion of the window
    _buildTextDisplay(topLevel).grid(row=2, col=0, sticky=NSEW)
    
    # bind events to the listboxes
    _bindEvents()

    
def main():
    """Sample use of Tkinter to build a graphical user interface"""
    # initialize Tk and get the top level window for our application
    topLevel = Tkinter.Tk()

    # load the resources (options) for all the 'named' widgets
    topLevel.option_readfile(tkinterGui.OPTION_FILE,
                             priority=tkinterGui.OPTION_PRIORITY)

    # allow the child widgets to resize with outer window
    tkinterGui.anchor(topLevel, 2, 1)
    
    # populate the topLevel window with other 'named' GUI components
    buildGui(topLevel)

    # start the main event loop
    topLevel.mainloop()


# This idiom allows you to treat more than one python module (file) in
# your application as your runtime 'main' (commonly used for unit testing),
# similar to having each Java module (file) have its own main() method.
#
# Also similar to (in C/C++):
#     #ifdef TEST
#       int main(int argc, char *argv[]) { ... }
#     #endif
#
if __name__ == "__main__":
    main()
