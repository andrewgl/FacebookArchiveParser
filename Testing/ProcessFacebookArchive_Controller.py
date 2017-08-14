__author__ = 'Andrew'
import zipfile
import datetime

import re

from Testing import Base_Controller
from Testing import DateFormatConversions

class ParseFBArchive_Controller(Base_Controller.Controller_Base):

    def __init__(self):
        self.fbArchiveFile = "None"

        self.threadTag = "<div class=\"thread\">"
        self.messageTag = "<div class=\"message\">"

        self.testThread = "Multiple Test.html"

        #htmlHeader = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><title>Maxamillion - Messages</title><link rel=\"stylesheet\" href=\"../html/style.css\" type=\"text/css\" /></head><body><div class=\"nav\"><img src=\"../photos/profile.jpg\" /><ul><li><a href=\"../index.htm\">Profile</a></li><li><a href=\"../html/contact_info.htm\">Contact Info</a></li><li><a href=\"../html/wall.htm\">Wall</a></li><li><a href=\"../html/photos.htm\">Photos</a></li><li><a href=\"../html/synced_photos.htm\">Synced Photos</a></li><li><a href=\"../html/videos.htm\">Videos</a></li><li><a href=\"../html/friends.htm\">Friends</a></li><li class=\"selected\">Messages</li><li><a href=\"../html/pokes.htm\">Pokes</a></li><li><a href=\"../html/events.htm\">Events</a></li><li><a href=\"../html/settings.htm\">Settings</a></li><li><a href=\"../html/security.htm\">Security</a></li><li><a href=\"../html/ads.htm\">Ads</a></li><li><a href=\"../html/mobile_devices.htm\">Mobile Devices</a></li><li><a href=\"../html/places.htm\">Places</a></li><li><a href=\"../html/survey_responses.htm\">Survey Responses</a></li></ul></div><div class=\"contents\"><h1>Maxamillion</h1><div>"
        #self.htmlHeader = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><title>Maxamillion - Messages</title><link rel=\"stylesheet\" href=\"../html/style.css\" type=\"text/css\" /></head><h1>5801606<BR>Exhibit 3411160/002<BR>Appendix A8-Facebook Download-Identified Chat Messages</h1><div>"
        self.htmlFooter = "<div class=\"footer\"></div></body></html>"

        self.dateParser=DateFormatConversions.dateFormatConversions()
        self.messagesHtml = None

        super().__init__()
        pass

    def setFBArchive(self, filepath):

        print ("setFBArchive(self, filepath):" + filepath)
        temp = filepath.rsplit('\\', 1)

        self.fb_archive_path = temp[0] + "\\"
        self.fbArchiveFile = temp[1]

        self.updateStatus("setFBArchive(self, filepath):" + filepath)
        self.updateResult("setFBArchive(self, filepath): arcchive = " + self.fbArchiveFile)

    def ParseFBArchive(self):

        print("ParseFBArchive:" + self.fbArchiveFile)
        self.updateStatus("ParseFBArchive:" + self.fbArchiveFile)
        self.updateResult("ParseFBArchive:" + self.fbArchiveFile)

        if self.fbArchiveFile == "":
            self.updateResult("Archive file not specified...")
        else:
            self.run(self.doProcessing)

    def doProcessing(self):
        self.updateStatus("doProcessing(self):")

        # read the zip files, isolate the messages.htm file
        self.findMessagesHtml()

        if self.messagesHtml == None:
            self.updateResult("Unable to locate messages.htm")
        else:
            self.updateResult("found messages.htm")
            self.updateStatus("..extracting messages")

            try:
                self.updateStatus("Parsing messages.htm, identifying message threads...")
                self.threads = self.messagesHtml.read().split(self.threadTag)

                self.htmlHeader = self.threads[0]
                self.threads = self.threads[1:]
                total_threads = len(self.threads)

                self.updateStatus("Parsing messages.htm, identifying message threads...done")
                self.updateResult("Done...identified " + str(total_threads) + " threads..")
            except Exception:
                self.updateStatus("Error parsing messages.htm, identifying message threads...")
                self.updateResult("Error...stop processing")


            thread_count = 0
            total_messages = 0

            for thread in self.threads:
                if thread_count > 101:
                    break

                thread_count += 1
                message_count = 0
                messages = thread.split(self.messageTag)
                participants = messages[0]
                messages=messages[1:]
                thread_messages = len(messages)

                # set up a mbox for the thread..
                try:
                    filename = self.returnFilename(participants)
                    self.FBmailbox = open(self.fb_archive_path + str(thread_count)+ "-" + filename, 'w', encoding='utf-8')

                except Exception as e:
                    self.updateStatus("unable to create mbox file at " + self.fb_archive_path)
                    self.updateResult("process failed, delete all created .mbox files and try again..")
                    break;

                for message in messages:
                    message_count += 1
                    messageID = str(thread_count) +"-" + str(100000+message_count)[1:]

                    self.updateStatus("Processing Thread " + str(thread_count) + " - " + filename + " parsing chat #" + str(message_count) + " of " +str(thread_messages))
                    message = message.replace("\n\n", "\n")
                    stripped = list(filter(None, re.split("<.*?>", message)))

                    #msgStr = "From FacebookArchiveParser " + datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y\n")
                    msgStr = "From FacebookArchiveParser " + self.dateParser.parseFrom_LineDate(stripped[1]) + "\n"
                    msgStr += "From: " + stripped[0] + "\n"
                    msgStr += "To: " + participants + "\n"
                    msgStr += "Date: " + self.dateParser.parseDateField(stripped[1]) + "\n"
                    msgStr += "Message-ID: " + messageID + "\n"
                    msgStr += "Messagehtml: " + message.replace("\n", "\n ") + "\n"

                    msgStr += "Nuixcontent: "

                    try:
                        nuixcontent = stripped[2].replace("\n", "\n ") + "\n"
                    except Exception:
                        #an empty message payload
                        nuixcontent = "\n"

                    msgStr += nuixcontent
                    msgStr += "Subject: " + "Parsed Chat Message ID " + messageID + "\n\n"

                    msgStr += nuixcontent + "\n\n\n"

                    self.FBmailbox.write(msgStr)

                self.updateResult("Processed " + str(thread_count) + " of " + str(total_threads) + " Threads, " + str(total_messages) + " total messages parsed")

                total_messages += message_count
                self.FBmailbox.close()

            self.updateResult("Finshed, processed " + str(thread_count) + " of " + str(total_threads) + " Threads, " + str(total_messages) + " messages")


    def returnFilename(self, raw):
        parties = raw.strip('<').split(", ", 4)
        if len(parties) >= 4:
            parties[3] = "etc"
            parties = parties[:4]
        key = ""
        for party in parties:
            key += "-" + party
        key = key.strip("<")
        keyFiltered = re.sub(r'[^a-zA-Z0-9\-]', '', key)
        return keyFiltered[1:] + ".mbox"

    def findMessagesHtml(self):

        try:
            self.zfile = zipfile.ZipFile(self.fb_archive_path + self.fbArchiveFile)

            try:
                self.updateStatus("..extracting messages.htm ")
                extractedPath = self.zfile.extract("html/messages.htm", path = self.fb_archive_path)
                self.messagesHtml = open(extractedPath, 'r', encoding='utf8')

            except Exception as e:
                self.updateStatus("")
                self.updateResult("unable to extract messages.htm " + str(e))

            self.updateStatus("")
            self.updateResult("open messages.htm success...")

        except FileNotFoundError:
            self.updateStatus("")
            self.updateStatus("unable to open zipfile " + str(FileNotFoundError))

    def returnKey(raw):
        parties = raw.strip('<').split(", ", 4)
        if len(parties) >= 4:
            parties[3] = "etc"
            parties = parties[:4]
        key = ""
        for party in parties:
            key += "-" + party
        key = key.strip("<")
        keyFiltered = re.sub(r'[^a-zA-Z0-9\-]', '', key)
        return keyFiltered[1:]

    def getNotifiers(self):
        cbs = {}

        cbs['SetFBArchive'] = self.setFBArchive
        cbs['ParseFBArchive'] = self.ParseFBArchive

        return cbs