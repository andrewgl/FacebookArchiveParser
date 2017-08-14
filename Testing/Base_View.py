__author__ = 'Andrew'

from tkinter import ttk, filedialog
from functools import partial
import threading


class BaseView(ttk.LabelFrame):
    title = "Base View Frame"
    statusDef = "Status: "
    resultsDef = "Results: "

    def __init__(self, parent):
        self.parent = parent

        self.callbacks = {}
        self.FBArchive = "None"
        self.viewlock = threading.Lock()

        self.labels = {}

        ttk.LabelFrame.__init__(self, self.parent, padding=(6, 6, 12, 12),
                                text=self.title)

        self.initUI()

    def initUI(self):
        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)

        self.addWidget(
            ttk.Button(self, text="Select FB Archive to process", command=self.setArchive),
            "FBArchiveFile", 'nw')
        self.addWidget(ttk.Label(self, text="FBArchiveFile selected: " + self.FBArchive), "Selected Archive", 'nw')

        self.labels['ProcessButton'] = ttk.Button(self, text="Process Archive: ", command=self.processCommand)
        self.labels['ProcessButton'].grid(in_=self, sticky='sw')

        self.update()

        info = (u"Status: ", u"Results: ")

        for i, item in enumerate(info):
            self.labels[item] = ttk.Label(self, text=u"%s:" % item + "unprocessed")
            self.labels[item].grid(in_=self, sticky='w')

    def addWidget(self, widget, item, align):
        self.labels[item] = widget
        self.labels[item].grid(in_=self, sticky=align)

    def status_Default(self):
        widget = self.labels['Status: ']
        widget.config(text=self.statusDef)
        self.update()

    def statusUpdate(self, newText):
        self.viewlock.acquire()

        widget = self.labels['Status: ']
        widget.config(text=self.statusDef + newText)
        self.update()

        self.viewlock.release()

    def resultUpdate(self, newText):
        self.viewlock.acquire()

        widget = self.labels['Results: ']
        widget.config(text=self.resultsDef + newText)
        self.update()

        self.viewlock.release()

    def updateLabel(self, item, newText):
        widget = self.labels[item]
        t = item + ": " + newText
        widget.config(text=t)

        self.update()

    def getStatusNotifiers(self):
        ret = {}
        ret['statusUpdate'] = self.statusUpdate
        ret['resultUpdate'] = self.resultUpdate

        return ret

    def setArchive(self):
        self.FBArchive = filedialog.askopenfilename().replace("/", "\\")
        #self.FBArchive = "U:\\Gleeson\\python projects\\FacebookArchiveParser\\Testing\\Resources\\facebook-andrewgleeson752.zip"
        #self.FBArchive =  "C:\\Users\\cf21578\\Documents\\Heggarty-FacebookDL\\facebook-benjaminhegarty1.zip"
        self.updateLabel("Selected Archive", self.FBArchive)

        cb = partial(self.callbacks['SetFBArchive'])
        cb(self.FBArchive)


    def processCommand(self):
        print(" def process_Callback(self)")

        self.callbacks['ParseFBArchive']()


    def subscribeEngine(self, methods):
        self.callbacks.update(methods)
