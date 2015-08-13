#! /bin/sh

# $1 is the binaries directory
# $2 is the symlinks directory

if [ -z "$2/$1" ] ; then exit 1 ; fi
if [ -z "$2/$2" ] ; then exit 1 ; fi

ln -s "$1/enlightenment_start" "$2/E17"
ln -s "$1/startfluxbox" "$2/Fluxbox"
ln -s "$1/gnome-session" "$2/GNOME"
ln -s "$1/icewm-session" "$2/ICEWM"
ln -s "$1/pekwm" "$2/PekWM"
ln -s "$1/startxfce4" "$2/XFCE4"
ln -s "$1/openbox-session" "$2/openbox"
