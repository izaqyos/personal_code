#!/usr/bin/python
"""Tkinter/Pmw GUI implementation of OOGui

COMMENTS
========
+ Easy widget creation; widget hierarchy based on pack() or grid()
  (placement layout is also available but not recommended)
+ Available with Python as of version 1.5
+ The most portable GUI, but not the richest widget set
+ Easily enhance Tkinter by using Pmw without conflict since Pmw is
  built on top of Tk. The other GUI libraries (toolkits) have their
  own event loop, initialization, etc.
+ Don't call mainloop() when running inside IDLE!

IDIOMS
======
+ Use grid_columnconfigure() and grid_rowconfigure() on containers
  to allow anchoring and expanding of children. Options include:
    <> minsize (minimum size of the column)
    <> weight (how much does additional space propagate to this column)
    <> pad (how much space to let in addition to weight)
+ Size of root window based on child sizes
+ Wraps Tk, so all configuration params available during construction
  or after object is created via call to 'configure(opt='xxx')'
+ Don't mix layout managers at the same container lavel!
+ Use of StringVar type to auto-update Label when data value changes
"""

# import GUI modules we use
import Tkinter

# import Tkconstants to module scope for ease of use
from Tkconstants import *

# show the use of Pmw widgets along with Tkinter
import Pmw

# import some system modules
import os

# import our main OOGui class
from oogui import OOGui
import oogui

# values used when loading GUI resources from file
OPTION_FILE     = 'filegui.ad'
OPTION_PRIORITY = 'startupFile'  # Tk's app-specific priority designator

# --------------------------------------------------------------------
# user interface utility functions / classes
# --------------------------------------------------------------------
def anchor(widget, rows=0, cols=0):
    """Takes care of anchoring/stretching widgets via grid 'sticky'"""
    for c in range(cols):
        widget.columnconfigure(c, weight=1)
    for r in range(rows):
        widget.rowconfigure(r, weight=1)


def setScrollbar(w, scrollable, basename, orient=BOTH):
    """Sets the specified scrollbar; returns xScrollbar and yScrollbar;
    None if BOTH not specified
    """
    xScrollbar = None
    yScrollbar = None

    if orient in (HORIZONTAL, BOTH):
        xScrollbar = __setScrollbar(w, basename, HORIZONTAL, scrollable.xview)
        scrollable.config(xscrollcommand=xScrollbar.set)

    if orient in (VERTICAL, BOTH):
        yScrollbar = __setScrollbar(w, basename, VERTICAL, scrollable.yview)
        scrollable.config(yscrollcommand=yScrollbar.set)

    return xScrollbar, yScrollbar


def __setScrollbar(w, basename, orient, cmd):
    """Private function used internally by setScrollbar"""
    scrollbar = Tkinter.Scrollbar(w, name=basename+orient, orient=orient)
    # Tkinter allows any option allowed in the ctor to also be configured
    # using 'config'
    scrollbar.config(command=cmd)

    return scrollbar


# -------------------------------------------------------------
# TkinterGui class extends OOGui and encapsulates the Tkinter
# version of the tutorial sample.
# -------------------------------------------------------------
class TkinterGui(OOGui):
    """Tkinter/Pmw version of the GUI"""
    def __init__(self, geometry=None, resfile=None, startdir=None):
        """Create the Tkinter GUI sample"""
        self._cwd = None

        topLevel  = Tkinter.Tk()

        # we're using Pmw, so initialize its hierarchy
        Pmw.initialise(topLevel)

        if not resfile:
            resfile = OPTION_FILE
        # call our parent class ctor which builds the GUI
        OOGui.__init__(self, topLevel, geometry, resfile, startdir)


    # -------------------------------------------------------------------
    # polymorphic implementations
    # -------------------------------------------------------------------
    
    def _buildGui(self, title):
        """Override parent's abstract 'hook' method called in ctor"""
        # build the working directory frame
        self._buildCWD()
        
        # build the paned widget that contains the lists and display
        self._buildPanes()

        anchor(self._topLevel, 2, 1)
        self._topLevel.title(title)

        
    def _loadResources(self, resfile=OPTION_FILE):
        """Load the resources (options) for all the 'named' widgets"""
        self._topLevel.option_readfile(resfile, priority=OPTION_PRIORITY)
        return 1


    def _setFilename(self, filename):
        """Sets the filename entry field when a file is selected; called
        by base class's _fileSelected() method
        """
        self._filename.set(filename)
        

    def _startGui(self, geometry=None):
        """Runs the application in the main event loop"""
        # set the top level window placement and size if specified
        if geometry:
            self._topLevel.geometry(geometry)

        # NOTE: DO NOT run the Tkinter mainloop while running in IDLE!"
        self._topLevel.mainloop()


    def _getSelectedDirectory(self):
        """Returns currently selected directory name"""
        return self._dirList.getSelection()


    def _getCurrentDirectory(self):
        """Returns the full pathname of the current working directory"""
        return self._cwd.get()
    

    def _getSelectedFile(self):
        """Returns currently selected file name"""
        if self._selectedFile:
            return self._selectedFile
        return self._fileList.getSelection()
    

    def _getTopLevel(self):
        """Special access method used by base to ensure top level is created"""
        return self._topLevel

        
    def _displayBinary(self, filename):
        """Displays binary files; in this case, we don't have a binary
        viewer, so we alert the user to that effect
        """
        self._display.unavail(filename)


    def _displayHTML(self, filename):
        """Implemented behavior for displaying HTML files"""
        self._display.html(filename)


    def _displayImage(self, filename):
        """Implemented behavior for displaying image files"""
        self._display.image(filename)


    def _displayText(self, filename):
        """Implemented behavior for displaying text (other) files"""
        self._display.text(filename)


    # -------------------------------------------------------------------
    # private class methods 
    # -------------------------------------------------------------------
    
    def _buildCWD(self):
        """Private method to construct the working directory frame"""
        cwdFrame = Tkinter.Frame(self._topLevel, name='cwdFrame')
        anchor(cwdFrame, 2, 2)

        Tkinter.Label(cwdFrame, name='cwdLabel').grid(row=0, col=0, sticky=W)

        # create the label's variable that will store the name of the cwd
        self._cwd = Tkinter.StringVar()
        # set the string variable's value with name of current working directory
        self._cwd.set(os.getcwd())
        # bind the label on the frame with the string variable
        Tkinter.Label(cwdFrame, name='cwdStringVar',
                      textvariable=self._cwd).grid(row=0, col=1, sticky=W)

        # add a button to allow the user to 'GoTo' a specified directory
        Tkinter.Button(cwdFrame, name='cwdButton',
                       command=self._setDirectory).grid(row=1, col=0, sticky=W)
        self._gotoEntry = Tkinter.Entry(cwdFrame, name='cwdEntry')
        self._gotoEntry.grid(row=1, col=1, sticky=E+W)
        self._gotoEntry.bind('<Return>', self._setDirectory)

        cwdFrame.pack(anchor=NW, expand=NO, fill=X)


    def _buildPanes(self):
        """Build a PanedWidget with panes for lists and display views"""
        panedW = Pmw.PanedWidget(self._topLevel,
                                 hull_width=400, hull_height=350)
        panedW.pack(expand=YES, fill=BOTH, anchor=NW)

        # place the lists in the 'list' pane
        listFrame = self._buildLists(panedW.add('list', min=oogui.SASH_MIN))
        listFrame.pack(expand=YES, fill=BOTH)

        # place the display in the 'disp' pane
        self._display = DisplayFrame(panedW.add('disp', min=oogui.SASH_MIN))
        self._display.pack(expand=YES, fill=BOTH)
        

    def _buildLists(self, pane):
        """Create the frame that contains list of files and text entry"""
        # create labels for file and directory list
        listFrame = Tkinter.Frame(pane, name='listFrame')
        listrows = 5
        anchor(listFrame, listrows, 2)

        row = 0
        Tkinter.Label(listFrame, name='dirLabel' ).grid(row=row, col=0,
                                                        sticky=NW)
        Tkinter.Label(listFrame, name='fileLabel').grid(row=row, col=1,
                                                        sticky=NW)
        row += 1

        # create the listbox for directories in specified directory
        self._dirList = SelectableList(listFrame, 'dirList', row, 0, listrows)
        self._dirList.setCommand(self._directorySelected)

        # create the listbox for files in specified directory
        self._fileList = SelectableList(listFrame, 'fileList', row, 1, listrows)
        self._fileList.setCommand(self._fileSelected)

        # include a row for the horizontal scrollbars
        row += listrows

        # create the save as filename label and entry
        row += 1
        Tkinter.Label(listFrame, name='entryLabel').grid(row=row, col=0, sticky=W)
        row += 1
        # create a variable to use for filename entry
        self._filename = Tkinter.StringVar(pane)
        entry = Tkinter.Entry(listFrame, name='fileEntry',
                              textvariable=self._filename)
        entry.grid(row=row, col=0, sticky=E+W, columnspan=2)
        entry.bind('<Return>', self._setFile)
        
        return listFrame
    

    def _setCWD(self, cwd):
        """Updates the GUI by setting the current working directory to 'cwd'"""
        if not cwd or not os.path.isdir(cwd):
            return
        self._cwd.set(cwd)
        self._setEntries()


    def _setDirectory(self, *unused):
        """Event callback for GoTo button and text entry to set the
        current working directory.
        """
        self._setCWD(self._gotoEntry.get())


    def _setFile(self, *unused):
        """Event callback for filename text entry to specify full pathname
        of file to display.
        """
        self._selectedFile = self._filename.get()
        self._fileSelected()
        self._selectedFile = None


    def _setEntries(self):
        """Sets the names of files and directories in the lists for the
        'current selected directory'
        """
        cwd = self._cwd.get()
        if not cwd:
            cwd = os.getcwd()
            self._cwd.set(cwd)
            
        self._gotoEntry.delete(0, END)
        self._gotoEntry.insert(0, cwd)

        # CHANGE since submission to Python10
        dirs, files = self._getEntries(cwd)

        # populate the list boxes with their respective entries
        self._dirList.delete(0, END)
        self._dirList.insert(0, *dirs)
        self._fileList.delete(0, END)
        self._fileList.insert(0, *files)


    # CHANGE since submission to Python10
    def _showDirectory(self):
        """Removed method after the python10 submission; refactored
        code to use the base class to join selected directory with
        selected base directory name from list"""
        pass



# -----------------------------------------------------------------------
# Selectable, scrollable list with user-defined callback for double-click
# -----------------------------------------------------------------------
class SelectableList(Tkinter.Listbox):
    """Selectable, scrollable list object"""
    def __init__(self, w, name, row=0, col=0, rowspan=1):
        Tkinter.Listbox.__init__(self, w, name=name)
        xsb, ysb = setScrollbar(w, self, name+'Scroll')
        self.grid(row=row, col=col, sticky=NSEW, rowspan=rowspan)
        xsb.grid(row=row+rowspan,  col=col, sticky=S+E+W)
        ysb.grid(row=row, col=col, sticky=E+N+S, rowspan=rowspan)


    def setCommand(self, command):
        """Bind double-click mouse event to perform specified command"""
        self.bind('<Double-Button-1>', command)


    def getSelection(self):
        """Returns the value of the current selection of specified list"""
        activeIndex = self.index(ACTIVE)
        if activeIndex >= 0:
            return self.get(activeIndex)
        return None


# -----------------------------------------------------------------------
# Specialized scrolled frame that displays text and image files
# -----------------------------------------------------------------------
class DisplayFrame(Tkinter.Frame):
    """Specialized scrolled frame that displays text and image files"""
    # CHANGE since submission to Python10 (fixed image display)
    def __init__(self, w):
        """Creates the frame that will display the specified file"""
        Tkinter.Frame.__init__(self, w, name="displayFrame")
        self._sw    = None   # rebuilt each time _show() is called
        self._image = None   # need to keep a handle to it or it gets GC'd
        anchor(self, 1, 1)

    def unavail(self, filename):
        """Resets/Clears the scrolled text and displays unavailable format"""
        self.text(None, 'Binary viewer not available for: %s' % filename)


    def html(self, filename):
        """No Pmw widgets available to display rich text, so just display
        the HTML source.
        """
        self.text(filename)


    # CHANGE since submission to Python10 (fixed image display bug)
    def image(self, filename):
        """Display the image (hold onto it so it doesn't get GC'd)"""
        import Image
        import ImageTk

        labelText = self._show(filename)
        try:
            img = Image.open(filename)
        except IOError:
            print 'Error opening image file: ', filename
        else:
            self._sw = Pmw.ScrolledFrame(self, labelpos=NW, label_text=labelText)
            self._sw.pack(expand=YES, fill=BOTH)
            label = Tkinter.Label(self._sw.interior(), bd=0)
                                             
            if img.mode == "1":
                # bitmap image
                self._image = ImageTk.BitmapImage(img, foreground="white")
                label.configure(bg="black")
            else:
                # photo image
                self._image = ImageTk.PhotoImage(img)
            label.configure(image=self._image)
            label.pack()


    def text(self, filename, altText=None):
        """Displays the text of the specified file"""
        labelText = self._show(filename)
        self._sw = Pmw.ScrolledText(self, usehullsize=1, borderframe=1,
                                    text_wrap=NONE, labelpos=NW,
                                    label_text = labelText,
                                    hull_width = oogui.DISPLAY_WIDTH,
                                    hull_height= oogui.DISPLAY_HEIGHT)
        self._sw.configure(hscrollmode="dynamic",vscrollmode="dynamic")
        self._sw.pack(expand=YES, fill=BOTH)
        if altText:
            self._sw.settext(altText)
        else:
            self._sw.importfile(filename)
        

    def _show(self, filename=None):
        """Manages the Pmw ScrolledText widget that displays the file"""
        if self._sw:
            self._sw.pack_forget()
            self._sw = None

        if not filename:
            filename = oogui.DISPLAY_UNAVAIL
        labelText = oogui.DISPLAY_LABEL + filename

        return labelText
