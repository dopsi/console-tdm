#! /bin/sh

# $1 is the binaries directory
# $2 is the symlinks directory

if [ -f "$2/$1" ] ; then exit 1 ; fi
if [ -f "$2/$2" ] ; then exit 1 ; fi

ln -sf "$1/enlightenment_start" "$2/E17"
ln -sf "$1/gnome-session" "$2/GNOME"
ln -sf "$1/icewm-session" "$2/ICEWM"
ln -sf "$1/openbox-session" "$2/openbox"
ln -sf "$1/pekwm" "$2/PekWM"
ln -sf "$1/startfluxbox" "$2/Fluxbox"
ln -sf "$1/startxfce4" "$2/XFCE4"
ln -sf "$1/xmonad" "$2/xmonad"
