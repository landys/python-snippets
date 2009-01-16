#!/usr/bin/env python
# coding=utf-8

import sys
import urllib2
import re
import os
import Cheetah
import atomFile
import cvdt

class WzNote:
    def __init__(self, tags, title, url, abstract, updateTime):
        self.tags = tags
        self.title = title
        self.url = url
        self.abstract = abstract
        self.updateTime = updateTime

class Atom:
    def __init__(self, csdnUser, gmail, title, wzNotes):
        self.csdnUser = csdnUser
        self.gmail = gmail
        self.title = title
        self.wzNotes = wzNotes

class CsdnWz2Atom:
    csdnWzUrl = 'http://wz.csdn.net/%(user)s/null/%(page)d/'
    message = 'Totally %(nPages)d pages, %(nNotes)d notes, including %(nWarnNotes)d warning notes.'
    pageEncoding = 'utf-8'
    # "<div\\s+class='fl'>\\s*<h1>\\s*<a\\s+href='(.*?)'.*?>\\s*(.*?)\\s*<.*?<p\\s*class='silver'>\\s*<a.*?</a>(.*?)时间：\\s*(.*?)\\s*\\|.*?<p>\\s*(.*?)\\s*</p>"
    regexWzNotes = "<div\\s+class='fl'>\\s*<h1>\\s*<a\\s+href='(?P<url>.*?)'.*?>\\s*(?P<title>.*?)\\s*<.*?<p\\s*class='silver'>\\s*<a.*?</a>(?P<tags>.*?)时间：\\s*(?P<rawtime>.*?)\\s*\\|.*?<p>\\s*(?P<abstract>.*?)\\s*</p>"
    # "<a.*?>\\s*(.*?)\\s*</a>"
    regexTags = "<a.*?>\\s*(?P<tag>.*?)\\s*</a>"
    regexNextPage = "<a\\s+href='/\\S+/null/\\d+/'>\\s*下一页\\s*</a>"
    
    roWzNotes = re.compile(regexWzNotes, re.DOTALL)
    roTags = re.compile(regexTags, re.DOTALL)
    roNextPage = re.compile(regexNextPage, re.DOTALL)
    
    def __init__(self, csdnUser, gmail, title, atomFileName):
        self.atom = Atom(csdnUser, gmail, title, [])
        self.atomFileName = atomFileName
        self.nNotes = 0
        self.nWarnNotes = 0
    
    def crawlCsdnWzPage(self, url):
        '''Read CSDN WZ from web through export url provided, return the contend string.'''
        try:
            f = urllib2.urlopen(url)
            if f.code == 200:
                re = f.read()
                return re
        except urllib2.URLError:
            print 'error to get page: ' + url
        except:
            print 'read data error: ' + url
        finally:
            f.close()
    
    @DeprecationWarning
    def readCsdnWzFile(self, fileName):
        '''Read CSDN WZ export file in file system, return the contend string.'''
        try:
            f = open(fileName, 'r')
            re = f.read()
            return re
        except:
            print 'read data error: ' + fileName
        finally:
            f.close()
    
    # return true if has next page.
    def parsePage(self, content):
        '''Parse page with regular expression matcher. Return the result list.'''
        notes = self.atom.wzNotes
        for mo in CsdnWz2Atom.roWzNotes.finditer(content):
            tags = []
            for moT in CsdnWz2Atom.roTags.finditer(mo.group('tags')):
                tags.append(moT.group('tag'))
            rawUrl = mo.group('url')
            rawAbs = mo.group('abstract')
            # google notebook not allow '%u' in the url, so it will be eliminated
            # and the url will not work as well.
            # i.e. http://www.i918.cn/200709/20070920.html?stra=%u6797%u632F%u5B87=%u7A0B%u7EA2%u82F1
            if rawUrl.find('%u') != -1 or rawUrl.find('%U') != -1:
                rawAbs = rawUrl + '<br><br>' + rawAbs
                print 'waring: problem url: ' + rawUrl
                rawUrl = rawUrl.replace('%u', '').replace('%U', '')
                self.nWarnNotes += 1
            
            tAbs = rawAbs.replace('&', '&amp;amp;').replace('<br>', '&lt;br&gt;').replace('<', '&amp;lt;').replace('>', '&amp;gt;').replace('"', '&amp;quot;').replace('\'', '&amp;#39;')
            tTitle = mo.group('title').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('\'', '&apos;')
            tUrl = rawUrl.replace(' ', '%20').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('\'', '&apos;')
            tTime = cvdt.convert_datetime(dt=mo.group('rawtime'), tz='UTC', dest_fmt='%Y-%m-%dT%H:%M:%S.000Z')
            notes.append(WzNote(tags, tTitle, tUrl, tAbs, tTime))
            self.nNotes += 1
            
        return CsdnWz2Atom.roNextPage.search(content) != None
    
    def printAtom(self, atomContent):
        atomFile = open(self.atomFileName, "w")
        atomFile.write(atomContent)
        atomFile.close()
    
    # return the message about the situation
    def go(self):
        '''Run to crawl, parse CSDN WZ, and generate atom xml file.'''
        
        hasNext = True
        nPages = 0
        while hasNext:
            # read page
            nPages += 1
            content = self.crawlCsdnWzPage(CsdnWz2Atom.csdnWzUrl %{'user':self.atom.csdnUser, 'page':nPages})
            #page = readCsdnWzFile(self, 'E:\\temp\\tonywz.html')
        
            # parse page
            hasNext = self.parsePage(content)
            print "Page %d finished." %(nPages),
            if (hasNext):
                print "Begin to crawl page %d..." %(nPages + 1)
        print        
        self.printAtom(atomFile.atomFile(searchList=[{'atom' : self.atom}]).__str__())
        
        return CsdnWz2Atom.message %{'nPages' : nPages, 'nNotes' : self.nNotes, 'nWarnNotes' : self.nWarnNotes}
# main
if __name__ == '__main__':
    if len(sys.argv) < 5:
        prog = os.path.basename(sys.argv[0])
        print "usage: python %s csdn-username gmail notebook-title result-atom-xml" %(prog)
        print "eg. python %s tonywjd tonywjd@gmail.com \"csdn bookmarks\" \"c:\\tonywjd-atom.xml\"" %(prog)
        sys.exit()

    print 'Begin generate atom xml from CSDN WZs...'

    print CsdnWz2Atom(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).go()

    print 'End successfully.'