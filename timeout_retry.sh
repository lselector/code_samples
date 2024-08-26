#!/bin/bash -x

# template to run script with timeout and retry

export MYDIR=/my/path/
export MYDATE=$(date +%Y%m%d)
export MYDT=$(date +"%Y%m%d_%H%M%S")
echo "MYDATE= $MYDATE"
echo "MYDT = $MYDT"
export PYTHONUNBUFFERED=TRUE

echo "=========================================================="
echo "run myscript.py"
nmax=5         # max number of attempt
n=1            # 1st attempt
until [ $n -gt $nmax ]
do
    echo "-------------------------------------------------"
    echo "attempt $n"
    echo $(date)
    /usr/bin/timeout --preserve-status 600 python $MYDIR/myscript.py 2>&1
    retcode=$?
    echo "retcode = $retcode"
    [[ retcode -eq 0 ]] && break
    ((n++))
    if [[ $n -le $nmax ]]
    then
        echo "Sleeping 90 seconds before retry..."
        sleep 90
    fi
done

echo $(date)

if [[ retcode -ne 0 ]]
then
    echo "=========================================================="
    echo "ERROR: Failed to get data after $n attempts, now exiting"
    exit
fi

echo $(date)