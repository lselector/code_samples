#! /bin/bash

# --------------------------------------------------------------
# copies files to BACKUPS/YYYYMMDD/ directory on server
# --------------------------------------------------------------

export MYDATE=`date +%Y%m%d`
export DIR_BACKUP="/somepath/BACKUPS/${MYDATE}"

export uhome=/home/myuser

mkdir -p "$DIR_BACKUP"
mkdir -p "$DIR_BACKUP/mycode"
mkdir -p "$DIR_BACKUP/dot"
mkdir -p "$DIR_BACKUP/ipython_startup"
mkdir -p "$DIR_BACKUP/jupyter_config"
mkdir -p "$DIR_BACKUP/nginx"
mkdir -p "$DIR_BACKUP/etc_init_d"

trap "echo Exited!; exit;" SIGINT SIGTERM
MAX_RETRIES=5
i=0
ff2=_
# --------------------------------------------------------------
echo_if_failure() {
  if [ $i -eq $MAX_RETRIES ]; then
    echo "$ff2 - failed, hit maximum number of retries"
  fi
}

# --------------------------------------------------------------
echo "Syncing mycode"
aa=$(ls -1 /path2code) # get lists of files and directories
aa=${aa//0-test-DE/}   # remove this directory from list
aa=${aa//OLD/}         # remove this directory from list
aa=${aa//BACKUPS/}     # remove this directory from list

for ff in $aa; do
  ff2="$ff"
  i=0
  false # Set the initial return value to failure
  while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    echo "attempt # $i - syncing $ff"
    i=$(($i+1))
    rsync -avzh --exclude 'somedir/somedir2/*.csv'  \
                --exclude 'somedir3/temp*.csv'  \
                --exclude '*/.ipynb_checkpoint*'  \
                --exclude 'something/something_else.csv'  \
                --exclude '*/__pycache_*'  \
                /path2code/$ff "$DIR_BACKUP/mycode/"
  done
  echo_if_failure
done

# --------------------------------------------------------------
echo "Syncing home dot files"
i=0
myfiles=(.bashrc .bashrc_crontab .bash_aliases)
myfiles+=(.bash_profile .inputrc .profile .vimrc)
myfiles+=(.gitconfig .gitexcludes)
# echo "${myfiles[@]}"

for ff in "${myfiles[@]}"; do
  ff2="$ff"
  i=0
  false # Set the initial return value to failure
  while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    echo "attempt # $i - syncing $ff"
    i=$(($i+1))
    rsync -avzh $uhome/${ff} "$DIR_BACKUP/dot/_${ff}.txt"
  done
  echo_if_failure
done
# --------------------------------------------------------------
i=0
ff2='ssh files'
false # Set just before the while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
  echo "attempt # $i - syncing $ff2"
  i=$(($i+1))
  rsync -avzh $uhome/.ssh/* "$DIR_BACKUP/dot/_ssh/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='ipython and jupyter startup and config'
false # Set just before the while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
  i=$(($i+1))
  echo "attempt # $i - Syncing $ff2"
  rsync -avzh $uhome/.ipython/profile_default/startup/*py       "$DIR_BACKUP/ipython_startup/"
  rsync -avzh $uhome/.ipython/profile_default/ipython_config.py "$DIR_BACKUP/"
  rsync -avzh $uhome/.jupyter/jupyter_notebook_config*          "$DIR_BACKUP/jupyter_config/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='nginx files'
false # Set just before the while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
  i=$(($i+1))
  echo "attempt # $i - Syncing $ff2"
  rsync -avzh /etc/nginx/* "$DIR_BACKUP/nginx/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='/etc/init.d files'
false # Set just before the while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
  i=$(($i+1))
  echo "attempt # $i - Syncing $ff2"
  rsync -avzh /etc/init.d/gnu_unicorn_* "$DIR_BACKUP/etc_init_d/"
done
echo_if_failure
# --------------------------------------------------------------
echo "All done - saved into $DIR_BACKUP"

