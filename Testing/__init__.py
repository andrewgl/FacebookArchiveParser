__author__ = 'Andrew'

import tkinter
from tkinter import ttk

from Testing import Base_View
from Testing import ProcessFacebookArchive_Controller

class MakeGUI(object):
    title = "Facebook Archive Parser by Andrew GLEESON"

    def __init__(self,root):
        self.root = root
        self.root.title(self.title)

        ## build frame
        self.mainframe = ttk.Frame(self.root, padding=(6, 6, 12, 12))
        self.mainframe.grid(sticky='nwse')

        for column in range(4):
            self.mainframe.columnconfigure(column, weight=1)
        self.mainframe.rowconfigure(3, weight=1)

        # text labels
        ttk.Label(self.mainframe, text=u"Facebook Archive Parser", anchor='center',
                font=("Helvetica", 32)).grid(in_=self.mainframe,
                        column=0, row=0, columnspan=3, sticky="ew")

        # create the view
        self.view = Base_View.BaseView(root)

        # create the FB parser module
        self.FBParser = ProcessFacebookArchive_Controller.ParseFBArchive_Controller()

        # connect the FB Parser module to the view so the status and result fields can be updated
        self.FBParser.subscribeView(self.view.getStatusNotifiers())

        # connect the view to the controller, so we can start it running from the view
        self.view.subscribeEngine(self.FBParser.getNotifiers())

        # ok we are al connected, nothing else to do here


    pass

def main():
    root = tkinter.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    makeGUI = MakeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()