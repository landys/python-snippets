#!/usr/bin/env python

import sys
import urllib2
import urllib  # urllib.unquote
import re
import os

class CrawlHelloKitty:
    # si = 0, 12, 24, ...
    hostUrl = "http://www.kaboodle.com"
    picHostUrl = "http://www.wetseal.com"
    itemPageTmp = "http://www.kaboodle.com/za/browse?startIndex=%(si)d&st=item&rti=AAAABEqonoUAAAAAAFH3Rg&rtt=CatalogItem&"
    regItems = "<p\\s+class=\"subject\">.*?<a\\s+href=\"(?P<uri>.*?)\">"
    regRedirectUrl = "<div\\s+id=\"bigImageContainer\">\\s*<a\\s+href=\".*?&redirect=(?P<url>.*?)\""
    regPicUri = "<div\\s+id=\"product-image\">\\s*<img\\s+src=\"(?P<uri>.*?)\""
    
    roItems = re.compile(regItems, re.DOTALL)
    roRedirectUrl = re.compile(regRedirectUrl, re.DOTALL)
    roPicUri = re.compile(regPicUri, re.DOTALL)
    
    def __init__(self, picdir):
        self.picdir = picdir
    
    def crawlPage(self, url):
        '''Read page from web through export url provided, return the contend string.'''
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
            try:
                f.close()
            except:
                print 'error to close url: ' + url
                
        return None
            
    # return redirect page list, or empty list
    def parseItemsPage(self, content):
        '''Parse page with regular expression matcher. Return the result list.'''
        uris = []
        for mo in CrawlHelloKitty.roItems.finditer(content):
            uris.append(mo.group('uri'))
        return uris
            
    def parseSingle(self, content, ro, gn):
        mo = ro.search(content)
        if mo != None:
            return mo.group(gn)
        return None;
    
    def go(self):
        nItem = 0 # 1392
        while True:
            itemUrl = CrawlHelloKitty.itemPageTmp %{'si':nItem}
            print "crawling: " + itemUrl
            content = self.crawlPage(itemUrl)
            if content != None:
                uris = self.parseItemsPage(content)
                if len(uris) == 0:
                    break
                for uri in uris:
                    content = self.crawlPage(CrawlHelloKitty.hostUrl + uri)
                    if content != None:
                        rurl = self.parseSingle(content, CrawlHelloKitty.roRedirectUrl, 'url')
                        if rurl != None:
                            content = self.crawlPage(urllib.unquote(rurl))
                            if content != None:
                                puri = self.parseSingle(content, CrawlHelloKitty.roPicUri, 'uri')
                                if puri != None:
                                    biguri = puri.replace("_lg.jpg", "_a1zm.jpg")
                                    i = biguri.rfind("/")
                                    urllib.urlretrieve(CrawlHelloKitty.picHostUrl + biguri, self.picdir + biguri[i+1:])
                                    
            nItem += 12
# main
if __name__ == '__main__':

    print 'Begin crawl...'

    CrawlHelloKitty("E:\\pic_skindetect\\clothtest\\hellokitty\\raw\\").go()
    
    #s = "/assets/ws/product_images/39490636100_lg.jpg".replace("_lg.jpg", "_a1zm.jpg")
    #i = s.rfind("/")
    #urllib.urlretrieve("http://www.wetseal.com" + s, "E:\\" + s[i+1:])

    print 'End successfully.'