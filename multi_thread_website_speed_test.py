#!/usr/bin/python

'''test access speed to the website indicated by url'''


import timeit
import urllib2
import Queue
import threading


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
    def __init__(self, url_t):
        self.url_t = url_t

    def test(self):
        setup_str = 'from __main__ import UrlHandler; url_test_m = UrlHandler("%s")' % self.url_t
        url_test_t = timeit.Timer('url_test_m.url_open()', setup=setup_str)
        return url_test_t.timeit(1)


class TestThread(threading.Thread):
    def __init__(self, threadID, test_q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.test_q = test_q

    def run(self):
        main(self.test_q)


def main(q):
    while not exitFlag:
        queue_lock.acquire()
        if not work_queue.empty():
            url = q.get()
            url_access_time = UrlTestManager(url).test()
            print "%-40s%.2fs" % (url, url_access_time)
            queue_lock.release()
        else:
            queue_lock.release()


url_file_path = "./urllist"
url_list = UrlProvider(url_file_path).make_list()
exitFlag = 0
queue_lock = threading.Lock()
work_queue = Queue.Queue()
threads = []
threadID = 1


if __name__ == "__main__":
    queue_lock.acquire()
    for url in url_list:
        work_queue.put(url)
    queue_lock.release()

    while threadID <= 3:
        thread = TestThread(threadID, work_queue)
        thread.start()
        threads.append(thread)
        threadID += 1

    while not work_queue.empty():
        pass 

    exitFlag = 1

    for t in threads:
        t.join()
    print "finish"
