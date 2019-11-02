#! /bin/bash
# ---------------------------------------------------------
# prints stats from
#     /mydir/files_out*/
#     /mydir/log/
# ---------------------------------------------------------

LC_NUMERIC=en_US
elb_dir=$HOME/mydir/bulk_parser
cd $elb_dir
echo "=============================================="

# current time
echo "Time                      :" `date +%H:%M:%S`
# run time as difference between first and last good files
cd /mydir/files_out
nn=`ls -t1 |wc -l`
hrs=0.0001
t1=`date +'%s'`
t2=`date +'%s'`
if (( $nn >= 1 )); then 
  t1=`ls -t1  | tail -n 1 | xargs stat --format=%Y`
  t2=`ls -tr1 | tail -n 1 | xargs stat --format=%Y`
  hrs=`python -c "print '%.4f' % (1.0*($t2-$t1)/60.0) ,"`
  echo "run time (mins)            : $hrs"
fi
cd $elb_dir

export logpre=/dw_data/log/log40
echo "amz*_get processes        :" ` ps auxww | grep -P 'amz\d_get' | grep -v grep | wc -l `
echo "---------------------------------"
n_req=` grep 'starting proxy : url' ${logpre}*.txt | wc -l `
req_per_sec=`python -c "print '%6.2f' % (1.0*$n_req/$hrs/3600.0) ,"`
printf "Requested URLs            : %'9.f (%6.2f / sec)\n" $n_req $req_per_sec
# ---------------------------------------------------------
n_files_out=` find /dw_data/files_out/               -type f -name '*.html' -print 2>&1 | grep html | wc -l `
n_files_out_bad_404=` find /dw_data/files_out_bad_404/       -type f -name '*.html' -print 2>&1 | grep html | wc -l `
out_per_sec=`python -c "print '%6.2f' % (1.0*$n_files_out/$hrs/3600.0) ,"`
printf "files_out                 : %'9.f (%6.2f / sec)\n" $n_files_out $out_per_sec
printf "files_out_bad_404         : %'9.f\n" $n_files_out_bad_404
# ---------------------------------------------------------
n_files_out_bad_robot_check=` find /dw_data/files_out_bad_robot_check/     -type f -name '*.html' -print 2>&1 | grep html | wc -l `
pct_robot_check=`python -c "print '%.2f' % (100.0*$n_files_out_bad_robot_check/(0.1+$n_req)) ,"`
printf "files_out_bad_robot_check : %'9.f (%5.2f%%)\n" $n_files_out_bad_robot_check $pct_robot_check 
# ---------------------------------------------------------
# instant robot check using a separate python script to print the results
python2.7 $elb_dir/s_instant_robot_check.py
echo "---------------------------------"
n_files_out_bad_no_title=` find /dw_data/files_out_bad_no_title/    -type f -name '*.html' -print 2>&1 | grep html | wc -l `
n_files_out_bad_non200=` find /dw_data/files_out_bad_non200/    -type f -name '*.html' -print 2>&1 | grep html | wc -l `
n_files_out_bad_not_found=` find /dw_data/files_out_bad_not_found/ -type f -name '*.html' -print 2>&1 | grep html | wc -l `
n_files_out_bad_short=` find /dw_data/files_out_bad_short/     -type f -name '*.html' -print 2>&1 | grep html | wc -l `
printf "files_out_bad_no_title    : %'9.f\n" $n_files_out_bad_no_title
printf "files_out_bad_non200      : %'9.f\n" $n_files_out_bad_non200
printf "files_out_bad_not_found   : %'9.f\n" $n_files_out_bad_not_found
printf "files_out_bad_short       : %'9.f\n" $n_files_out_bad_short
# ---------------------------------------------------------
echo "---------------------------------"
n_chunked=` cat ${logpre}*.txt | grep -i Error | grep -vP 'Terror|starting proxy|sec_per_url=|starting url|finished url' | grep ChunkedEncodingError | grep raise | wc -l `
pct_chunked=`python -c "print '%.2f' % (100.0*$n_chunked/(0.1+$n_files_out)) ,"`
printf "err_ChunkedEncoding       : %'9.f (%5.2f%%)\n" $n_chunked $pct_chunked
# ---------------------------------------------------------
n_proxy=` cat ${logpre}*.txt | grep -i Error | grep -vP 'Terror|starting proxy|sec_per_url=|starting url|finished url' | grep ProxyError | grep raise | wc -l `
pct_proxy=`python -c "print '%.2f' % (100.0*$n_proxy/(0.1+$n_files_out)) ,"`
printf "err_ProxyError            : %'9.f (%5.2f%%)\n" $n_proxy $pct_proxy
# ---------------------------------------------------------
n_ssl=` cat ${logpre}*.txt | grep -i Error | grep -vP 'Terror|starting proxy|sec_per_url=|starting url|finished url' | grep SSLError | grep raise | wc -l `
pct_SSLError=`python -c "print '%.2f' % (100.0*$n_ssl/(0.1+$n_files_out)) ,"`
printf "err_SSLError              : %'9.f (%5.2f%%)\n" $n_ssl $pct_SSLError
# ---------------------------------------------------------
n_con=` cat ${logpre}*.txt | grep -i Error | grep -vP 'Terror|starting proxy|sec_per_url=|starting url|finished url' | grep ConnectionError | grep raise | wc -l `
pct_ConnectionError=`python -c "print '%.2f' % (100.0*$n_con/(0.1+$n_files_out)) ,"`
printf "err_ConnectionError       : %'9.f (%5.2f%%)\n" $n_con $pct_ConnectionError
# ---------------------------------------------------------
n_parse_err=` cat ${logpre}*.txt | grep 'My_Parsing_Error' | wc -l `
printf "err_My_Parsing_Error      : %'9.f \n" $n_parse_err
# ---------------------------------------------------------
n_other_err=` cat ${logpre}*.txt | grep -i Error | grep -viP 'terror|starting proxy|sec_per_url=|starting url|finished url|ChunkedEncodingError|ProxyError|SSLError|ConnectionError|myfailure|myencoding|My_Parsing_Error' | wc -l `
pct_other=`python -c "print '%.2f' % (100.0*$n_other_err/(0.1+$n_files_out)) ,"`
printf "err_other_err             : %'9.f (%5.2f%%)\n" $n_other_err $pct_other
# ---------------------------------------------------------
# echo "Not retrieved      :"
for filename in ${logpre}*.txt; do
    cat $filename | grep 'not retrieved' | grep 'pages' | grep -v 'not retrieved 0 pages'
done
# ---------------------------------------------------------
