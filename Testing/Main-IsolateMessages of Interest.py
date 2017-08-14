__author__ = 'cf21578'

from collections import defaultdict
import re


resourcesPath = "C:\\Users\\cf21578\\Documents\\FBParse-DICTIONARY\\resources\\"
outputPath = "C:\\Users\\cf21578\\Documents\\FBParse-DICTIONARY\\tempOutput-revised\\"

threadTag = "<div class=\"thread\">"
messageTag = "<div class=\"message\">"

testThread = "Multiple Test.html"

#htmlHeader = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><title>Maxamillion - Messages</title><link rel=\"stylesheet\" href=\"../html/style.css\" type=\"text/css\" /></head><body><div class=\"nav\"><img src=\"../photos/profile.jpg\" /><ul><li><a href=\"../index.htm\">Profile</a></li><li><a href=\"../html/contact_info.htm\">Contact Info</a></li><li><a href=\"../html/wall.htm\">Wall</a></li><li><a href=\"../html/photos.htm\">Photos</a></li><li><a href=\"../html/synced_photos.htm\">Synced Photos</a></li><li><a href=\"../html/videos.htm\">Videos</a></li><li><a href=\"../html/friends.htm\">Friends</a></li><li class=\"selected\">Messages</li><li><a href=\"../html/pokes.htm\">Pokes</a></li><li><a href=\"../html/events.htm\">Events</a></li><li><a href=\"../html/settings.htm\">Settings</a></li><li><a href=\"../html/security.htm\">Security</a></li><li><a href=\"../html/ads.htm\">Ads</a></li><li><a href=\"../html/mobile_devices.htm\">Mobile Devices</a></li><li><a href=\"../html/places.htm\">Places</a></li><li><a href=\"../html/survey_responses.htm\">Survey Responses</a></li></ul></div><div class=\"contents\"><h1>Maxamillion</h1><div>"
htmlHeader = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><title>Maxamillion - Messages</title><link rel=\"stylesheet\" href=\"../html/style.css\" type=\"text/css\" /></head><h1>5801606<BR>Exhibit 3411160/002<BR>Appendix A8-Facebook Download-Identified Chat Messages</h1><div>"
htmlFooter = "<div class=\"footer\"></div></body></html>"

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

def processBookmarks():
    bmFile = open(resourcesPath + "Bookmarks-working copy.txt", encoding='utf-8')
    lines = bmFile.read().splitlines()
    bms = defaultdict(list)
    key = ""
    for line in lines:
        # I pre-pended lines from the bookmarks text files describing which thread subsequent date/times are from with a '>'
        # If that char is the first of a line, its from a new thread and change the key
        if line[0] == '>':
            key = line[1:line.rfind('-')]
        else:
            bms[key].append(line)
    return bms


# teststring = "<div class=\"thread\"> --------------------Mitch Deigan<div class=\"thread\"><div class=\"thread\"> --------------------The Pope<div class=\"thread\">"
#contactFile = open(resourcesPath + "Contacts-all.txt", encoding='utf-8', errors='ignore')
contactFile = open(resourcesPath + "Contacts-all.txt")
contactlist = contactFile.read().split("\n")

#FBdownload = open(resourcesPath+"messages.htm",encoding='utf-8', errors='replace')
FBdownload = open(resourcesPath+"messages.htm")

threads = FBdownload.read().split(threadTag)
threads = threads[1:]

print ("collecting threads...total" + str(len(threads)))
threadDict = defaultdict(set)

print ("processing Bookmarks File...")
bookmarks = processBookmarks()
print ("done, " + str(len(bookmarks)) + " threads containing bookmarked dates identified..")

totalMessages = 0
totalThreads = 0

print ("Isolating messages containing dates of interest...")
for thread in threads:
    #for contact in contactlist:

    threadParties = thread.split("<div class=\"message\">")[0]
    key = returnKey(threadParties)
    print ("key...")
    #does the key exist in the bookmarks dictionary? Only process if it does
    if key in bookmarks:
        print("_____found bookmark " + key)
        totalThreads += 1

        #Start re-building the thread, only adding individual messages if they contain a "date of interest" (stored in bookmarks)
        ofInterest = []
        ofInterest.append("Participants: " + threadParties)

        messages = thread.split(messageTag, -1)[1:]

        #threadBMs = bookmarks[key]
        threadBMs=bookmarks[key][::-1]

        bms = iter(threadBMs)
        print(key + "_____..new bms")

        if key == "AngusSmith-Maxamillion":
            print("AngusSmith-Maxamillion: " + str(len(messages)) + " messages.  Last: " + messages[len(messages)-1])
            print("")

        while len(threadBMs) > 0:
            fromDT = threadBMs.pop()
            toDT = threadBMs.pop()

            print ("_____ _____ from " + fromDT + " - to: " + toDT)

            #find the first instance of a message carrying the fromDT
            messageIter = iter(messages)
            message = next(messageIter, None)

            if "Friday, October 3, 2014 at 10:00am UTC+10" in message:
                print("here")

            while message is not None and toDT not in message:
                message = next(messageIter, None)

            #copy all messages to ofInterest until the toDT is identified
            while message is not None and not fromDT in message:
                ofInterest.append(messageTag + message)
                message = next(messageIter, None)

            #copy all messages to ofInterest with the toDT
            while message is not None and fromDT in message:
                ofInterest.append(messageTag + message)
                message = next(messageIter, None)


            # while message is not None and datetime in message:
            #     # the "date/time" of interest has been identified in this message, add the message
            #     # to the ofInterest string
            #
            #     ofInterest.append(messageTag + message)
            #     message = next(messageIter, None)

            # Messages in the FB download are sequential according to date/time, so subsequent messages are likely to have the same date/time
            # there is no need to search for them again.  While this is true, add the messages to ofInterest
            # once we identify a date/time, we dont need to continue to search for it as messages are incremental. remove it
            # if fromDT in bookmarks[key]:
            #     bookmarks[key]=[x for x in bms if x != fromDT]
            #     print(key + "________________________ dropped From bm :" + datetime)
            #
            # if toDT in bookmarks[key]:
            #     bookmarks[key]=[x for x in bms if x != toDT]
            #     print(key + "________________________ dropped To bm :" + datetime)
            #
            # if len(bookmarks[key]) == 0:
            #     break
            # else:
            #     datetime = next(bms)

            # Add the rebuilt thread containing only messages of interest to the Thread Dictionary

        totalThreads += 1
        threadDict[key].add("".join(ofInterest))

       # print("________________done...identified " + str((before - after) * len(ofInterest)) + " new messages")


print ("..done" + str(totalThreads) + " total threads involving " + str(totalMessages) + " potential messages of interest")

print ("...rebuilding threads at " + outputPath)
totalThreadsWrite = 0

for key, value in threadDict.items():
    filename = key + "-" + str(len(set(threadDict[key]))) + "_threads.html"

    print("writing: " + filename)
    output = open(outputPath + filename, "w", encoding="utf-8", errors="replace")
    output.write(htmlHeader + "\n" + threadTag)


    for value in threadDict[key]:
        totalThreadsWrite += 1
        output.write(value + "\n")


    output.write(htmlFooter)
    output.close()

print (str(totalThreadsWrite) + " total messages involving parties of interest")

