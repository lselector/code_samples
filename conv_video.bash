#! /bin/bash
# set -x #echo on
# ---------------------------------------------------
# script conv.bash to convert multiple videos
# using ffmpeg command
#   https://github.com/FFmpeg/FFmpeg
#   https://ffmpeg.org
#   https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
# ---------------------------------------------------
# Note: working directory is hardcoded - change it as needed
# ---------------------------------------------------
# Usage:
#     # make sure you are running bash shell
#     bash
#     # start as background process
#     nohup bash conv.bash > /tmp/log.txt 2>&1 &
# ---------------------------------------------------
# Example of the command I am using:
#    vstream=0   # video stream index - usually zero
#    astream=0   # audio stream index - can be 0 or different - depends which
#                # to figure out which audio track to extract, use "vidinfo" function
#                # described below ( ffprobe $1 2>&1 | grep Stream )
#
#    ffmpeg -hide_banner -nostats -nostdin -loglevel panic -y \
#           -i $fname_in \
#           -s hd720 -c:v libx265 -tag:v hvc1 -crf 28 \
#           -c:a aac -ac 2 \
#           -map 0:v:$vstream -map 0:a:$astream \
#           $fname_out > ${fname_out}.log.txt 2>&1
#
# where:
# -nostdin           # do not listen to stdin - need it to run in the background
# -loglevel panic    # reduce output
# -y                 # automatically answer "yes" to prompts
# -i input_file
# -vf                # provide custom scaling
# -s hd720           # provide output size
# -c:v  libx265      # provide encoding library
# -tag:v hvc1        # necessary for QuickTime Player to play this format
#                    # as described here: https://brandur.org/fragments/ffmpeg-h265
# -crf 28            # Constant Rate Factor (0..51, default 23)
# -map 0:v:0         # take first (0th) video tack
# -map 0:a:1         # take 2nd (1st) audio track
# -ac 2              # downmix audio from 5.1 to only 2 stereo audio channels
# -c:a aac           # downmix audio to aac
# ---------------------------------------------------
# Optionally instead of "-s hd720" you can specify resolution manually:
#    -s 1280x720
# ---------------------------------------------------
# Optionally instead of "-s hd720" you can have custom scaling:
#  -vf "scale=trunc(iw/8)*2:trunc(ih/8)*2"
# ---------------------------------------------------
# Optionally (for testing) specify start/end time:
#   https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
#   -ss 00:10:00 -to 00:10:30
# Or starting time and duration
#   -ss 00:10:00 -t 00:00:30
# ---------------------------------------------------
# To simply trim the video you can do this:
# ffmpeg -i $fname_in -ss 00:00:15 -to 00:00:25 -c copy $fname_out
# or
# ffmpeg -i $fname_in -ss 00:00:15 -to 00:00:25 -acodec copy -vcodec copy $fname_out
# ---------------------------------------------------
# You can use ffprobe to get info about the file, for example:
#   ffprobe test2.mkv 2>&1 |grep Stream
# ---------------------------------------------------
# You can add a tag without re-encoding like that:
#   https://aaron.cc/ffmpeg-hevc-apple-devices/
#   ffmpeg -i input.mp4 -vcodec copy -acodec copy -tag:v hvc1 output.mp4
# ---------------------------------------------------
# You can use vidinfo function:
# --------------------------------
# bash:
#
# vidinfo () {
#    ffprobe $1 2>&1 | grep Stream
# }
# --------------------------------
# fish
#
# function vidinfo
#   ffprobe $argv 2>&1 | grep Stream
# end
# ---------------------------------------------------
# Some commands on Mac:
# find files bigger than 5 GB using fd search
#   https://github.com/sharkdp/fd
#     fd -t f -S +5G 2>&1
# print vidinfo for many files:
#     for f in *.avi; echo $f; vidinfo $f; echo " "; end;
# ---------------------------------------------------

src_root="$HOME/_myconvert/myvideos"

cd $src_root

t1=$(date +%s)
# export MYDATE=$(date +%Y%m%d)
# export MYDT=$(date +"%Y%m%d_%H%M%S")
# export logfile=log_${MYDT}.txt

#for fname_in in \
#    somefile \
#;

for fname_in in $(ls -1 *mkv); 
do
    echo " ";
    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
    date;
    fname_out="conv_${fname_in%.mkv}.mp4"
#    fname_out="conv_${fname_in}"

    echo "$fname_in";
    echo "$fname_out";

    vstream=0
    astream=1

    ffmpeg -hide_banner -nostats -nostdin -loglevel panic -y \
           -i $fname_in \
           -s hd720 -c:v libx265 -tag:v hvc1 -crf 28 \
           -c:a aac -ac 2 \
           -map 0:v:$vstream -map 0:a:$astream \
           $fname_out > ${fname_out}.log.txt 2>&1 ;

    echo " ";

done;

echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++";

# --------------------------------------------------------------
convertsecs() {
 ((h=${1}/3600))
 ((m=(${1}%3600)/60))
 ((s=${1}%60))
 printf "%02dh %02dm %02ds\n" $h $m $s
}
# --------------------------------------------------------------
date
t2=$(date +%s)
t3=$(($t2-$t1))
echo "run time was" $(convertsecs $t3)
echo "ALL DONE"
echo " "
