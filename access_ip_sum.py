#!/usr/bin/python

'''collect nginx log and get the access ip and analysis it'''

import sys
import json


def ip_get(log_file):
    ip_list = []
    try:
        with open(log_file) as f:
            for line in f:
                ip_list.append(line.split(' ')[0])
    except IOError as e:
        print e
    return ip_list

def ip_count(ip_list):
    if not isinstance(ip_list, list):
        raise InputError('input is bad!')
    ip = {}
    for i in ip_list:
        if ip.get(i, 0):
            ip[i] += 1
        else:
            ip[i] = 1
    return ip

def save_ipcount(count_file, dest_file):
    if not isinstance(count_file, dict):
        raise InputError('input is bad!')
    try:
        with open(dest_file, 'a') as f:
            for k,v in sorted(count_file.items(), key=lambda x:x[1]):
                str_ip_count = "%-15s%-d\n" % (k,v)
                f.write(str_ip_count)
    except IOError as e:
        print e
    return

if __name__ == '__main__':
    log_file = sys.argv[1]
    analysis_file = sys.argv[2]

    ip_l = ip_get(log_file)
    ip_c = ip_count(ip_l)
    save_ipcount(ip_c, analysis_file)
