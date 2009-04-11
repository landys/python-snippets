#!/usr/bin/env python
# coding=utf-8

import sys
import os
from xml.etree import ElementTree
from datetime import datetime
        
class Bookmark:
    def __init__(self, tags, title, url, abstract, updateTime):
        self.tags = tags
        self.title = title
        self.url = url
        self.abstract = abstract
        self.updateTime = updateTime
        
class Atom2BM:
    bmHead = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>"""
    bmTail = "</DL><p>"
    bmTemp = '<DT><A HREF="%(url)s" LAST_VISIT="%(updateTime)d" ADD_DATE="%(updateTime)d" TAGS="%(tags)s">%(title)s</A>\n'
    startTime = datetime(1970, 1, 1, 0, 0, 0)
    
    def __init__(self, atomFileName, bmFileName):
        self.atomFileName = atomFileName
        self.bmFileName = bmFileName

    # return the number of bookmark generated
    def go(self):
        # open result bookmark file and write the head of the file
        bmFile = open(self.bmFileName, "w")
        bmFile.write(Atom2BM.bmHead)
        
        # parse the atom file and write into the bookmark file
        tree = ElementTree.parse(self.atomFileName)
        ele = tree.getroot()
        count = 0
        xmlns = "{http://www.w3.org/2005/Atom}"
        for entry in ele.getiterator(xmlns + "entry"):
            link = entry.find(xmlns + "link")
            if (link == None or link.text == ""):
                continue
            title = link.get("title")
            url = link.get("href")
            content = entry.find(xmlns + "content").text
            updated = entry.find(xmlns + "updated").text
            tags = []
            for tag in entry.getiterator(xmlns + "category"):
                if (tag.get("scheme") == "http://schemas.google.com/g/2005/label"):
                    tags.append(tag.get("term"))
            
            self.printBookmark(Bookmark(tags, title, url, content, updated), bmFile)
            count += 1
        
        # write the tail of the bookmark file and close it.
        bmFile.write(Atom2BM.bmTail)
        bmFile.write("<!-- Totally %d bookmarks. -->" %(count))
        bmFile.close()
        
        return count
    
    def printBookmark(self, bm, bmFile):
        tdelta = datetime.strptime(bm.updateTime[:19], "%Y-%m-%dT%H:%M:%S") - Atom2BM.startTime
        updateTime = tdelta.days * 86400 + tdelta.seconds
        title = bm.title.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', '\'').replace('&amp;', '&')
        url = bm.url.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', '\'').replace('&amp;', '&')
        tags = ""
        for tag in bm.tags:
            if (tags != ""):
                tags += ","
            tags += tag
        strBm = Atom2BM.bmTemp %{"url":url, "updateTime":updateTime, "tags":tags, "title":title}
        if (bm.abstract != None and bm.abstract != ""):
            abstract = bm.abstract.replace('&lt;br&gt;', '\n').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', '\'').replace('&amp;', '&').replace('<br>', '\n')
            strBm += "<DD>" + abstract +"\n"
        
        bmFile.write(strBm.encode('utf-8'))
        
# main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        prog = os.path.basename(sys.argv[0])
        print "usage: python %s input-atom-xml output-bookmark-html" %(prog)
        print "eg. python %s \"c:\\my-atom.xml\" \"c:\\my-bookmark.html\"" %(prog)
        sys.exit()

    print 'Begin generate bookmark xml from atom xml file...'

    print 'Bookmarks generated: %d' %(Atom2BM(sys.argv[1], sys.argv[2]).go())

    print 'End successfully.'