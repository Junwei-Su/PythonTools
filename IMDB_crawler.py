#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This is a simple web spider for
#the web page IMDB
#Author: little_town
#data: 2016-9-30

import string
import re
import urllib2

class webSpider(object) :
    
    """
        Attribute:
        page: current page being browsed
        cur_url:url for the current page
        data:stored the movie names on this page
        top_num: record the current top value
    """
    
    def __init__(self) :
        self.page = 1
        self.cur_url = "http://www.imdb.com/"
        self.datas = []
        self.top_num = 1
        print "Preparing for the crawler..."

    def get_page(self, cur_page) :
        """
        get the whole body of the current page
        """
        url = self.cur_url
        try :
            page = urllib2.urlopen(url);
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason

        page_content = page.read();
        return page_content;


def main() :
    print """
        ###############################
        A simple webpage crawler
        Author: little_town
        Version: 0.0.1
        Date: 2016-9-30
        ###############################
        """
    my_spider = webSpider()
    print(my_spider.get_page(my_spider.page));

if __name__ == '__main__':
    main()
