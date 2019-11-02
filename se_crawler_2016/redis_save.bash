#!/bin/bash

# save redis every 5 min

while :
do
    sleep 300
    redis-cli BGSAVE
done
