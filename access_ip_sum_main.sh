#!/bin/bash
# use access_ip_sum.py to analysis access ip count

LOGPATH=/web/log
ANALYSIS=$LOGPATH/analysis

mkdir $ANALYSIS
mv $ANALYSIS ${ANALYSIS}-`data +%F%H:%M:%S`
ls ${LOGPATH}/*.log|xargs -i python access_ip_sum.py {} {}.analysis
mv $LOGPATH/*.analysis $ANALYSIS
