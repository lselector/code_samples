#!/bin/bash

# run query in MySQL database
# save results into a TAB-separated CSV file

mysql -h $host_ip --ssl-ca=$SSHDIR/prd-server-ca.pem --database=mydb \
  -u${MYUSER} -p${MYPSWD} >$DIR_DATA/myfile.csv <<EOF_MYSQL
select 
  id,
  status,
  date(last_update_time) as date_updated,
  date(created)          as date_created
from mytable
order by id
-- limit 3
;
EOF_MYSQL
