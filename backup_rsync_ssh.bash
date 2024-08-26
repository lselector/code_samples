#! /bin/bash

# --------------------------------------------------------------
# copies files from server to local computer via ssh
# --------------------------------------------------------------

export MYDATE=`date +%Y%m%d`

export DIR_LOCAL="$HOME/BACKUPS/${MYDATE}"

export uu='myuser@myserver.mydomain.com'
export uhome=$uu:/home/myuser

mkdir -p "$DIR_LOCAL"
mkdir -p "$DIR_LOCAL/mycode"
mkdir -p "$DIR_LOCAL/dot"
mkdir -p "$DIR_LOCAL/ipython_startup"
mkdir -p "$DIR_LOCAL/jupyter_config"
mkdir -p "$DIR_LOCAL/nginx"
mkdir -p "$DIR_LOCAL/etc_init_d"

# --------------------------------------------------------------
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
aa=$(ssh "$uu" ls -1 /path2code) # get lists of files and directories
aa=${aa//some-dir/}              # remove this directory from list
aa=${aa//OLD/}                   # remove this directory from list
aa=${aa//BACKUPS/}               # remove this directory from list

for ff in $aa; do 
  ff2="$ff"
  i=0
  false # Set just before while loop
  while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    echo "attempt # $i - syncing $ff"
    i=$(($i+1))
    rsync -avzh --exclude 'somedir/somedir2/*.csv'  \
                --exclude 'somedir3/temp*.csv'  \
                --exclude '*/.ipynb_checkpoint*'  \
                --exclude 'something/something_else.csv'  \
                --exclude '*/__pycache_*'  \
                -e ssh $uu:/path2code/$ff "$DIR_LOCAL/mycode/"
  done
  echo_if_failure
done

# --------------------------------------------------------------
echo "Syncing home dot files"

myfiles=(.bashrc .bashrc_crontab .bash_aliases)
myfiles+=(.bash_profile .inputrc .profile .vimrc)
myfiles+=(.gitconfig .gitexcludes)
# echo "${myfiles[@]}"

for ff in "${myfiles[@]}"; do 
  ff2="$ff"
  i=0
  false # Set just before while loop
  while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    echo "attempt # $i - syncing $ff"
    i=$(($i+1))
    rsync -avzhe ssh $uhome/${ff} "$DIR_LOCAL/dot/_${ff}.txt"
  done
  echo_if_failure
done
# --------------------------------------------------------------
i=0
ff2='ssh files'
false # Set just before while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    i=$(($i+1))
    echo "attempt # $i - syncing $ff2"
    rsync -avzhe ssh $uhome/.ssh/* "$DIR_LOCAL/dot/_ssh/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='ipython and jupyter startup and config'
false # Set just before while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    i=$(($i+1))
    echo "attempt # $i - Syncing $ff2"
    rsync -avzhe ssh $uhome/.ipython/profile_default/startup/*py       "$DIR_LOCAL/ipython_startup/"
    rsync -avzhe ssh $uhome/.ipython/profile_default/ipython_config.py "$DIR_LOCAL/"
    rsync -avzhe ssh $uhome/.jupyter/jupyter_notebook_config*          "$DIR_LOCAL/jupyter_config/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='nginx files'
false # Set just before while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    i=$(($i+1))
    echo "attempt # $i - Syncing $ff2"
    rsync -avzhe ssh $uu:/etc/nginx/* "$DIR_LOCAL/nginx/"
done
echo_if_failure
# --------------------------------------------------------------
i=0
ff2='/etc/init.d files'
false # Set just before while loop
while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]; do
    i=$(($i+1))
    echo "attempt # $i - Syncing $ff2"
    rsync -avzhe ssh $uu:/etc/init.d/gnu_unicorn_* "$DIR_LOCAL/etc_init_d/"
done
echo_if_failure
# --------------------------------------------------------------
echo "All done - saved into $DIR_LOCAL"
