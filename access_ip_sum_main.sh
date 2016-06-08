#!/bin/bash
# use access_ip_sum.py to analysis access ip count

LOGPATH=/web/log
ANALYSIS=$LOGPATH/analysis

mv $ANALYSIS ${ANALYSIS}-`date +%F%H:%M:%S` 2>/dev/null
mkdir $ANALYSIS
ls ${LOGPATH}/*.log|xargs -i python access_ip_sum.py {} {}.analysis
mv $LOGPATH/*.analysis $ANALYSIS
