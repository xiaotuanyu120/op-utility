#!/bin/bash
# use access_ip_sum.py to analysis access ip count

LOGPATH=/web/www

ls ${LOGPATH}/*.log|xargs -i python access_ip_sum.py {} {}.analysis
