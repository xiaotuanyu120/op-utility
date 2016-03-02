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

    def urlopen(self, test_url)

    def test(self, test_url):
        setup_str = "\
            import urllib2
            
"
        url_test_t = timeit.Timer('urllib2.urlopen(test_url)', setup=setup_str)
        return url_test_t.timeit(1)


class TestThread(threading.Thread):
    def __init__(self, threadID, test_q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = test_q

    def run(self):
        while not exitFlag:
            queue_lock.acquire()
            if not work_queue.empty():
                url = self.q.get()
                url_access_time = UrlHandler().test(url)
                print "%-40s%.2fs" % (url, url_access_time)
                queue_lock.release()
            else:
                queue_lock.release()


url_file_path = "./urllist"
url_list = UrlHandler().make_list(url_file_path)
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

    while threadID <= 5:
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
