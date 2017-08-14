__author__ = 'Andrew'

import time

class dateFormatConversions():

    def __init__(self):

        self.weekdays = {}

        self.weekdays['Monday'] = "Mon"
        self.weekdays['Tuesday'] = "Tue"
        self.weekdays['Wednesday'] = "Wed"
        self.weekdays['Thursday'] = "Thu"
        self.weekdays['Friday'] = "Fri"

        self.months = {}
        self.months['January']="01"
        self.months['February']="02"
        self.months['March']="03"
        self.months['April']="04"
        self.months['May']="05"
        self.months['June']="06"
        self.months['July']="07"
        self.months['August']="08"
        self.months['September']="09"
        self.months['October']="10"
        self.months['November']="11"
        self.months['December']="12"

        self.timezones = {}
        self.timezones['UTC+11']="+1100"
        self.timezones['UTC+10']="+1000"

        self.AM_PM = {}
        self.AM_PM['am'] = 0
        self.AM_PM['pm'] = 12

    def parseFrom_LineDate(self, rawDate):
        stripped = rawDate.replace(",","")
        stripped = stripped.replace("at ", "")
        fields = stripped.split(' ')
        try:
            # Java style date
            #parsedStr = fields[3] + "-" + self.months[fields[2]] + "-" + fields[1].zfill(2) + " " + fields[4] + ":00 " + self.timezones[fields[5]]
            # MBox Style Date/Time
            #parsedStr = fields[0][:3] + " " + fields[1].zfill(2) + " " + fields[2][:3] + " " + fields[3] + " " + fields[4] + " " + self.timezones[fields[5]]
            parsedStr = fields[0][:3] + " " + fields[2][:3] + " " + fields[1].zfill(2) + " " + fields[4] + ":00 " + fields[3]
        except Exception as e:
            print("..error parsing date/time ")
        return parsedStr

    def parseDateField(self, rawDate):
        stripped = rawDate.replace(",","")
        stripped = stripped.replace("at ", "")
        fields = stripped.split(' ')
        try:
            #parsedStr = fields[0][:3] + " " + fields[2][:3] + " " + fields[1].zfill(2) + " " + fields[4] + ":00 " + fields[3]
            parsedStr = fields[0][:3] + ", " + fields[1] + " " + fields[2][:3] + " " + fields[3] + " " + fields[4] + ":00 " + self.timezones[fields[5]]
            print(parsedStr)
        except Exception as e:
            print("..error parsing date/time ")
        return parsedStr

