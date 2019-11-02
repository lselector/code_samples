#! /bin/bash
# ---------------------------------------------------------
# myrun2.bash
# starts scraping run
# ---------------------------------------------------------

myrun2_pid=$$
se_dir=$HOME/se_crawler
cd $se_dir
pwd
source utils.bash

# ---------------------------------------------------------
# step1 - cleanup
# ---------------------------------------------------------
echo "killing running processes (if any)"
./kill_w.bash
./kill_m.bash
rm -f pid/*
echo $$ > pid/m_$$

echo "cleaning output directories"
for dir_out in `ls -1d $elb_dir/data/files_out*`; 
do
    find $dir_out/  -type f -name '*.html'  -delete
done

find $se_dir/data/log/  -type f -name "log*.txt" -delete

echo "check redis"           # (re)start redis if needed XXXXXXXXXXXXXX
echo "clean redis"           # clean redis queues XXXXXXXXXXXXXX

# ---------------------------------------------------------
# step2 - run search, fill multi-queue
# ---------------------------------------------------------
myscript=se_st2_run_search.py
echo "starting $myscript"
python3 $myscript > data/log/se_st2.txt 2>&1
check_err $? "ERROR, script $myscript failed" $0 $LINENO

# ---------------------------------------------------------
# step3 - parse multi-pages to get URLs of single-pages
# ---------------------------------------------------------
n_workers=2
sec_sleep=1
myscript=se_st3_get_urls_of_listings.py
echo "starting $myscript"

for ii in `seq 1 $n_workers`;
do
    sleep $sec_sleep
    num=$(printf '%02d' "$ii")
    mycmd="python3 -uB $myscript --worker=${ii} > data/log/se_st3_${num}.txt 2>&1 &"
    echo $ii ": " $mycmd
    eval $mycmd
done

wait_sec=900
t1=`date +'%s'`           # epoch seconds, int
t2=$(($t1 + $wait_sec)) 
nn=`ps auxww | grep 'se_st3_get_urls' | grep -v grep | wc -l`
while [ $nn -gt 0 ] && [ $t1 -lt $t2 ]
do
  sleep 1
  t1=`date +'%s'`
  nn=`ps auxww | grep 'se_st3_get_urls' | grep -v grep | wc -l`
done

if [ $nn -gt 0 ]
then
  echo "ERROR - script $myscript is running too long"
  echo "killing and exiting"
  ./kill_w.bash
  exit 1    
fi
# ---------------------------------------------------------
# step4 - parse single-listing pages, save data into CSV
# ---------------------------------------------------------
n_workers=2
sec_sleep=1
myscript=se_st4_parse_listings.py
echo "starting $myscript"

for ii in `seq 1 $n_workers`;
do
    sleep $sec_sleep
    num=$(printf '%02d' "$ii")
    mycmd="python3 -uB $myscript --worker=${ii} > data/log/se_st4_${num}.txt 2>&1 &"
    echo $ii ": " $mycmd
    eval $mycmd
done

wait_sec=900
t1=`date +'%s'`           # epoch seconds, int
t2=$(($t1 + $wait_sec)) 
nn=`ps auxww | grep 'se_st4_parse' | grep -v grep | wc -l`
while [ $nn -gt 0 ] && [ $t1 -lt $t2 ]
do
  sleep 1
  t1=`date +'%s'`
  nn=`ps auxww | grep 'se_st4_parse' | grep -v grep | wc -l`
done

if [ $nn -gt 0 ]
then
  echo "ERROR - script $myscript is running too long"
  echo "killing and exiting"
  ./kill_w.bash
  exit 1    
fi

# ---------------------------------------------------------
# step5 - combine all outputs, email report
# ---------------------------------------------------------
myscript=se_st5_make_report.py
echo "starting $myscript"
python3 $myscript > data/log/se_st5.txt 2>&1
check_err $? "ERROR, script $myscript failed" $0 $LINENO

echo "All DONE"
