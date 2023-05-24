#!/bin/bash

pgrep firefox && pkill firefox
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon cunyFirst
cd /home/gmatz/Code/cunyFirst
/home/gmatz/Code/cunyFirst/cunyGrades.py $*
pgrep firefox && pkill firefox
