# global
#if [ -f /etc/bashrc ]; then
#	. /etc/bashrc
#fi

## editor for crontab, cvs
EDITOR=vi
export EDITOR

## pager for man
PAGER=less
export PAGER

alias ls="ls -F --color=auto "
alias la="ls -a --color=auto "
alias l="ls -a "
alias sl="ls"
alias less="less -x4 -r "
alias rm="rm -i "
alias mv="mv -i "
alias cp="cp -i "
#alias ct="date +%Y%m%d-%H%M%S"
alias ct="cleartool"
alias kt="kterm -km euc -sb -sl 2000"
alias c="clear"
#alias emacs="meadow "   # for cygwin
#alias mule="meadow "    # for cygwin


#path variables

#clearcase
PATH=${PATH}:/auto/cwtools/perl/focus/bin/lnx/:/usr/atria/bin/:/sbin/
CWTOOLS=/auto/cwtools/;export CWTOOLS


#For maven
MAVEN_HOME=/vob/enm_jdk/maven-2.0.9; export MAVEN_HOME;
PATH=${PATH}:${MAVEN_HOME}/bin/:
JAVA_HOME=/usr/java/jdk1.6.0_22; export JAVA_HOME;
PATH=${PATH}:"$JAVA_HOME"
MAVEN_OPTS="-Xms256m -Xmx1024m" 

#ACS related

#For quantify and purify
. /sw/licensed/rational/products/purifyplus_setup.sh

#prompt
PS1="[\u@\h:\d:\w]\$ "

#scripts to path
PATH=${PATH}:~/work/scripts/:~/work/scripts/python/util:~/work/scripts/util/:~/work/scripts/sed/:~/work/scripts/perl/util


source ~/.aliases

#set vi prompt mode, for emacs mode (default) use, set -o emacs
set -o vi
bind '"\t":menu-complete'

#For centrify adjoin
PATH=${PATH}:/usr/sbin:

#for python v 2.5
PATH=${PATH}:/auto/nmtg-acs-img/bin/python2.5.1.1/linux_x86/bin:
alias python='/auto/nmtg-acs-img/bin/python2.5.1.1/linux_x86/bin/python'

#wxwidgets libs
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib:/usr/X11R6/lib:
alias rsync='/usr/cisco/bin/rsync'

#Set tmp dir
TMPDIR="$HOME/tmp"

#Python
PYTHONSTARTUP=~/.pythonrc
export PYTHONSTARTUP

#Alerts from cron etc
export MAILTO="yizaq@cisco.com"
