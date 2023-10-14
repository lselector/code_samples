# Examples of renaming multiple files in bash

# ---------------------------
ls -1 *.png | perl -nle '$old=$_; s/pat1/word1/; rename($old, $_);' -
# ---------------------------
ls -1 *.mp3 | perl -nle '$old=$_; s/^(d\d\d).*\.mp3/$1.mp3/; rename($old, $_);' -
# ---------------------------
for ii in *.mkv *.mp4; do 
    mv "$ii" "${ii/_27-01-2017/}"; 
done
# ---------------------------
for f in *-SD\ for\ Apple\ Devices.m4v ; do
    mv "$f" "${f/-SD\ for\ Apple\ Devices/}"; 
done
# ---------------------------
# changing spaces to underscores in file names:
for f in *\ *; do 
    mv "$f" "${f// /_}"; 
done
# ---------------------------
# combining files into one
for fname in *.txt; do 
    echo "$fname"
    cat $fname; 
    echo;
    echo "-------------------";
    echo; 
done > all.txt
