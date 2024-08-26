#! /bin/bash
# set -x #echo on
# ---------------------------------------------------
# script conv_images.bash to convert multiple images
# using convert command from imagemagic 
# on MacOS install using brew:  
#      brew install imagemagic
# Here are some commands you will get:
#   animate, compare, composite, conjure, convert,
#   display, identify, import, magick, magick-script
#   mogrify, montage, stream
#   https://www.howtogeek.com/109369/how-to-quickly-resize-convert-modify-images-from-the-linux-terminal/
#   https://imagemagick.org/
#   https://github.com/ImageMagick/ImageMagick
# ---------------------------------------------------
# Note: working directory is hardcoded - change it as needed
# ---------------------------------------------------
# Usage:
#     # make sure you are running bash shell
#     bash
#     # start as background process
#     nohup bash conv_images.bash > /tmp/log_conv_image.txt 2>&1 &
# ---------------------------------------------------
# Identify sizes and resolutions of several images:
#   magick identify rose.jpg
#   for f in *jpg; du -sh $f; magick identify $f; echo " "; end;
#   https://imagemagick.org/script/identify.php
#   https://stackoverflow.com/questions/1555509/can-imagemagick-return-the-image-size
# 
# Resize image by providing width or xhight or both:
#   http://www.imagemagick.org/script/command-line-processing.php#geometry
#   https://www.smashingmagazine.com/2015/06/efficient-image-resizing-with-imagemagick/
#
#   convert input.jpg -resize 300 output.jpg         # w
#   convert input.jpg -resize x400 output.jpg        # h
#   convert input.jpg -resize 300x400 output.jpg     # w & h
#   convert input.jpg -resize 300x400! output.jpg    # w & h force (change aspect ratio)
#   convert input.jpg -resize 300x400 -quality 75 output.jpg
#   mogrify -path output/ -resize 300 *.jpg
#
#   mogrify -path $OUTPUT_PATH -filter Triangle -define filter:support=2 \
#     -thumbnail $OUTPUT_WIDTH -unsharp 0.25x0.25+8+0.065 -dither None \
#     -posterize 136 -quality 82 -define jpeg:fancy-upsampling=off \
#     -define png:compression-filter=5 -define png:compression-level=9 \
#     -define png:compression-strategy=1 -define png:exclude-chunk=all \
#     -interlace none -colorspace sRGB -strip $INPUT_PATH
#
# ---------------------------------------------------

src_root="$HOME/_myconvert/myimages"

cd $src_root

t1=$(date +%s)
# export MYDATE=$(date +%Y%m%d)
# export MYDT=$(date +"%Y%m%d_%H%M%S")
# export logfile=log_${MYDT}.txt

#for fname_in in \
#    somefile \
#;

for fname_in in $(ls -1 *png); 
do
    echo " ";
    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
    date;
    fname_out="../conv_images/s_${fname_in%.png}.jpg"
#    fname_out="conv_${fname_in}"

    echo "$fname_in";
    echo "$fname_out";

    width=300

    convert $fname_in -resize $width -quality 75 $fname_out > /tmp/${fname_in}.log.txt 2>&1 ;

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
