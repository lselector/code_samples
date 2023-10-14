#! /bin/bash

# --------------------------------------------------------------
# backup_rsync_simple.bash
# copy one USB drive to another
#   rsync -a /Volumes/Seagate4TB/   /Volumes/SandDisk4TB
# --------------------------------------------------------------
# -a, --archive          archive mode; same as -rlptgoD (no -H)
# --------------------------------------------------------------
# -r, --recursive        recurse into directories
# -l, --links            copy symlinks as symlinks
# -p  --perms            preserve permissions
#     -t, --times        preserve times
#     -g, --group        preserve group
#     -o, --owner        preserve owner (super-user only)
#     -D, --devices --specials
#     -H, --hard-links
# --------------------------------------------------------------
# -v, --verbose          increase verbosity
# -z, --compress         compress file data during the transfer
# -h, --human-readable   output numbers in a human-readable format
# --------------------------------------------------------------

export MYDATE=`date +%Y%m%d`
echo "started" $(date)
rsync -a /Volumes/Seagate4TB/   /Volumes/SanDisk4TB/
echo "finished" $(date)

