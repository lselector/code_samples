#! /bin/bash
# ---------------------------------------------------------
# saves output files to a directory named with current datestamp
# ---------------------------------------------------------

dtstamp=`date +%y%m%d-%H%M%S`
data_dir=$HOME/se_crawler/data
mkdir $data_dir/$dtstamp

dirs2move="log
  files_out
  files_out_bad_404
  files_out_bad_non200
  files_out_bad_not_found
  files_out_bad_robot_check
  files_out_bad_short"

for item in $dirs2move
do
  mv    $data_dir/$item   $data_dir/$dtstamp/$item
  mkdir $data_dir/$item
done
