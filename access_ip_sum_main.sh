#!/bin/bash
# use access_ip_sum.py to analysis access ip count

LOGPATH=/web/www
ANALYSIS=$LOGPATH/analysis

mv $ANALYSIS ${ANALYSIS}-`data +%F%H:%M:%S`
ls ${LOGPATH}/*.log|xargs -i python access_ip_sum.py {} {}.analysis
