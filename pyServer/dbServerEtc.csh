#!/bin/csh
#
# Start/Stop script for dbServerEtc.py
# 
# Usage: dbServerEtc.csh [start/stop] port
#        dbServerEtc.csh start 50001
#

# Verify inputs

if ($#argv != 2) then
    echo "Usage: dbServerEtc.csh [start/stop] port"
        exit
endif

set cmd = $1
if ("$cmd" != "start" && "$cmd" != "stop") then
    echo "Usage: dbServerEtc.csh [start/stop] port"
        echo "Incorrect start/stop command"
        exit
endif

set port = $2
if ($port < 50000 || $port > 59999) then
    echo "Usage: dbServerEtc.csh [start/stop] port"
        echo "Incorrect port number"
        exit
endif

# run the desired command

set python = "/usr/local/anaconda/bin/python"
set script = `echo $0 | sed 's/.csh/.py/g'`
set test = `ps -elf | grep dbServerEtc.py | grep $port | awk '{print $4}'`

# Start dbServerEtc

if ("$cmd" == "start") then
    if ($#test > 0) then
        echo "dbServerEtc.py is already running on port $port"
        exit
    else
        echo "Starting dbServerEtc.py on port $port"
        #$python $script $port > /dev/null &
        $python $script $port &
        exit
    endif
endif

# Stop dbServerEtc

if ("$cmd" == "stop") then
    if ($#test == 0) then
        echo "No dbServerEtc.py processes running on port $port"
        exit
    else
        echo "Stopping dbServerEtc.py on port $port"
        foreach p ($test)
            echo "kill -9 $p"
            kill -9 $p
        end
    endif
endif