import sys
import urllib2
import re
import os
import Cheetah
import atomFile

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
    pageEncoding = 'utf-8'
    
    def __init__(self, csdnUser, gmail, title):
        self.atom = Atom(csdnUser, gmail, title, [])
    
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
        ro = re.compile(csdnWzRegex, re.DOTALL)
        notes = []
        for mo in ro.finditer(page):
            mo.group('tags')
            notes.append(WzNote(mo.group('tags'), mo.group('title'), mo.group('url'), mo.group('abstract')))
        return notes
    
    def go(self):
        '''Run to crawl, parse CSDN WZ, and generate atom xml file.'''
        # read page
        #page = crawlCsdnWzPage(self, csdnWzExportUrl)
        #page = readCsdnWzFile(self, 'E:\\temp\\tonywz.html')
        
        # parse page
        #notes = parsePage(page)
        
        #count = 0
        #for note in notes:
        #    print '%s\n%s\n%s\n%s\n' %(note.tags, note.title, note.url, note.abstract)
        #    count += 1
        #    if count == 10:
        #        break
        notes = self.atom.wzNotes
        notes.append(WzNote(['a', 'b'], 'abcd', 'http://www.google.com', 'hello world', 'aaaaa'))
        notes.append(WzNote(['a1', 'b1'], 'abcd1', 'http://www.google.com1', 'hello world1', 'aaaaa1'))
        notes.append(WzNote(['a2', 'b2'], 'abcd2', 'http://www.google.com2', 'hello world2', 'aaaaa2'))
        print atomFile.atomFile(searchList=[{'atom' : self.atom}])
# main
if __name__ == '__main__':
    if len(sys.argv) < 4:
        prog = os.path.basename(sys.argv[0])
        print "usage: python %s csdn-username gmail notebook-title" %(prog)
        print "eg. python %s tonywjd tonywjd@gmail.com \"csdn bookmarks\"" %(prog)
        sys.exit()

    print 'Begin generate atom xml from CSDN WZs...'

    CsdnWz2Atom(sys.argv[1], sys.argv[2], sys.argv[3]).go()

    print 'End successfully.'