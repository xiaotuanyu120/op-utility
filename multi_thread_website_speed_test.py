#!/usr/bin/python

'''test access speed to the website indicated by url'''


import timeit
import urllib2
import Queue
import threading


class UrlHandler(object):
    def __init__(self):
        self.url_list = []

    def make_list(self, url_stored_file):
        with open(url_stored_file) as f:
            for line in f:
                self.url_list.append(line[:-1])
        return self.url_list 

    def url_open(self, url):
        return urllib2.urlopen(url)


class UrlTest(object):
    def __init__(self, test_url):
        self.test_url = test_url

    def test_access_time(self):
        setup_str = '''\
from __main__ import UrlHandler
url_h = UrlHandler()
test_url = "%s"''' % self.test_url
        url_test_t = timeit.Timer('url_h.url_open(test_url)', setup=setup_str)
        return url_test_t.timeit(1)


class ThreadControl(threading.Thread):

    def __init__(self, test_q):
        threading.Thread.__init__(self)
        self.q = test_q

    def run(self):
        while not exitFlag:
            queue_lock.acquire()
            if not self.q.empty():
                url = self.q.get()
                url_access_time = UrlTest(url).test_access_time()
                print "%-40s%.2fs" % (url, url_access_time)
                queue_lock.release()
            else:
                queue_lock.release()
        return

    def queue_prepare(self):
        return


url_file_path = "./urllist"
url_list = UrlHandler().make_list(url_file_path)
exitFlag = 0
queue_lock = threading.Lock()
work_q = Queue.Queue()
threads = []
threadID = 1


if __name__ == "__main__":
    queue_lock.acquire()
    for url in url_list:
        work_q.put(url)
    queue_lock.release()

    while threadID <= 5:
        thread = ThreadControl(work_q)
        thread.start()
        print "thread: %s is ready" % threadID
        threads.append(thread)
        threadID += 1

    while not work_q.empty():
        pass 

    exitFlag = 1

    for t in threads:
        t.join()
    print "finish"
