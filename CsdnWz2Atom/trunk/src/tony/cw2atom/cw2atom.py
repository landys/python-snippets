import sys
import urllib2
import re

# global constants
csdnWzUrl = 'http://wz.csdn.net/%(user)s/null/%(page)d/'
pageEncoding = 'urf-8'

class WzNote:
    def __init__(self, tags, title, url, abstract):
        self.tags = tags
        self.title = title
        self.url = url
        self.abstract = abstract
        
def crawlCsdnWzPages():
    '''Crawl web pages of the user name.'''
    pass

def crawlCsdnWzPage(url):
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
def readCsdnWzFile(fileName):
    '''Read CSDN WZ export file in file system, return the contend string.'''
    try:
        f = open(fileName, 'r')
        re = f.read()
        return re
    except:
        print 'read data error: ' + fileName
    finally:
        f.close()

def parsePage(page):
    '''Parse page with regular expression matcher. Return the result list.'''
    global csdnWzRegex
    ro = re.compile(csdnWzRegex, re.DOTALL)
    notes = []
    for mo in ro.finditer(page):
        mo.group('tags')
        notes.append(WzNote(mo.group('tags'), mo.group('title'), mo.group('url'), mo.group('abstract')))
    return notes

# main
if __name__ == '__main__':
    print 'Begin copy CSDN WZs to Google Notebook...'
    
    # read page
    #page = crawlCsdnWzExport(csdnWzExportUrl)
    page = readCsdnWzExportFile('E:\\temp\\tonywz.html')
    
    # parse page
    notes = parsePage(page)
    
    count = 0
    for note in notes:
        print '%s\n%s\n%s\n%s\n' %(note.tags, note.title, note.url, note.abstract)
        count += 1
        if count == 10:
            break

    print 'End successfully.'