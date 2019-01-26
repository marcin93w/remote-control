#!/bin/bash
#
ssh pi@$1 "kill $(ssh pi@$1 \"ps -e | grep python3 | awk '{print $1}'\")" 