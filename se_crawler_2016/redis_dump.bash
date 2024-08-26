#! /bin/bash

# dump redis to file dump.rdb
# move this file to subdirectory redis_dump
# remove old dumps

dump_dir=$HOME/se_crawler/redis_dump

redis-cli bgsave
sleep 60

MYDATE=`date +%Y%m%d`
mv dump.rdb $dump_dir/dump${MYDATE}.rdb

# delete old dumps
find ${dump_dir}/ -mtime +30 -delete
