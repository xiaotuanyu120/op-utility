#!/usr/bin/python

'''test access speed to the website indicated by url'''


import timeit
import urllib2


class UrlHandler(object):
    def __init__(self, tested_url):
        self.tested_url = tested_url

    def url_open(self):
        return urllib2.urlopen(self.tested_url)


class UrlProvider(object):
    def __init__(self, url_stored_file):
        self.url_stored_file = url_stored_file
        self.url_list = []

    def make_list(self):
        with open(self.url_stored_file) as f:
            for line in f:
                self.url_list.append(line[:-1])
        return self.url_list 

class UrlTestManager(object):
    def __init__(self, url_list):
        self.url_list = url_list
        self.url_access_speed = {}

    def test(self):
        for url in self.url_list:
            setup_str = 'from __main__ import UrlHandler; url_test_m = UrlHandler("%s")' % url
            url_test_t = timeit.Timer('url_test_m.url_open()', setup=setup_str)
            self.url_access_speed[url] = url_test_t.timeit(1)
        return self.url_access_speed


def main():
    url_file_path = "./urllist"
    url_get = UrlProvider(url_file_path).make_list()
    url_access_time = UrlTestManager(url_get).test()
    for url in url_get:
        print "%-40s%.2fs" % (url, url_access_time[url])

if __name__ == "__main__":
    main()
