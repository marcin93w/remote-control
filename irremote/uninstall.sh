#!/bin/bash
#
kill $(ps -e | grep python3 | awk '{print $1}')
cd ..
rm -r irremote