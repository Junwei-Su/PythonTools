#!/usr/bin/env python
# -*- coding:utf-8 -*-
#This is a simple web spider for
#the web page IMDB
#Author: little_town
#data: 2016-9-30

import string
import re
import urllib2
import matplotlib.pyplot as plt
import numpy as np

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
        self.cur_url = "https://www.zomato.com/vancouver/best-downtown-restaurants"
        self.datas = []
        self.top_num = 1
        print "Preparing for the crawler..."

    def get_page(self, cur_page) :
        """
        get the whole body of the current page
        """
        url = self.cur_url
        try :
            page = urllib2.urlopen(url)
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason

        page_content = page.read();
        return page_content;

    def extract_lister(self,my_page):
        """
        get the lister content
        """
        list = re.findall(r'<tbody class="lister-list">(.*?)</tbody>', my_page, re.S)
        list_string  = ''.join(str(e) for e in list)
        return list_string
    
    
    def get_Mtitle(self,list_string):
        """
        get all the movie titles from the current page
        """
        titles=[];
        titles_items = re.findall(r'<td class="titleColumn">(.*?)</td>', list_string, re.S)
        for item in titles_items:
            title = re.search('(?<=>).*?(?=</a>)', item).group(0)
            titles.append(str(title))
        return titles
    
    def get_years(self,list_string):
        """
        get the year the movies produced
        """
        years=[];
        year_items = re.findall(r'<td class="titleColumn">(.*?)</td>', list_string, re.S)
        for item in year_items:
            year = re.search('(?<=>).*?(?=</span>)', item).group(0)
            year = re.search('(?<=\()[0-9]{4}(?=\))',year).group(0)
            years.append(int(year))
        return years
    
    def get_top100years(self,list_string):
        """
            get the year the movies produced
            """
        years=[];
        year_items = re.findall(r'<td class="titleColumn">(.*?)</td>', list_string, re.S)
        for i in range(1,100):
            year = re.search('(?<=>).*?(?=</span>)', year_items[i]).group(0)
            year = re.search('(?<=\()[0-9]{4}(?=\))',year).group(0)
            years.append(int(year))
        return years
    
    def get_yearHist(self, years):
        plt.hist(years)
        plt.title("IMDB Top 250 Movies Year of production Histogram")
        plt.xlabel("Year")
        plt.ylabel("Frequency")
        fig = plt.gcf()
        plt.show()
    

    def start_spider(self) :
        """
        Entry of the crawling process
        """
        my_page = self.get_page(self.page)
        print(my_page)



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
    my_spider.start_spider()

if __name__ == '__main__':
    main()
