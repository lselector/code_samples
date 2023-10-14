#! /bin/bash

# function check_err usage:
#    check_err $? "some error message" $0 $LINENO
# where:
#   $? - special shell variable indicating error (if non-zero)
#   "some error message" - whatever you want to print when error happens
#   $0 - special shell variable containing the script name
#   $LINENO - special shell variable containing line number in the script
# This function checks the return code (first parameter).
# If it is non-zero - this indicates an error.
# If it's an error, then it prints err. message (including script and line#) 
# and calls "exit 1" causing the calling script to terminate.

function check_err {
    if [ $# -ne 4 ]
    then
        echo "Usage: $0 <ret code> <err msg> <file name> <line number>"
        return 1
    fi

    RET=$1
    ERR_MSG=$2
    FILE=$3
    LINE=$4

    if [ $RET -ne 0 ]
    then
        echo "Error in $FILE line $LINE: $ERR_MSG"
        exit 1
    fi

    return 0
}
