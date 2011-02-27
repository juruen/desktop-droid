#! /bin/bash

# If $DEBIAN_PREFIX is set, it will be prepended to all locations.
# This is used when building the Debian package.

set -e


PREFIX=${PREFIX-/usr}
BIN=${BIN-$PREFIX/bin}
APPS=${APPS-$PREFIX/share}
ICONS=${ICONS-$PREFIX/share/pixmaps}
DESKTOP=${DESKTOP-$PREFIX/share/applications}
DESKTOP_DROID="$APPS/desktop-droid"

##

install_file () {
    # path/file path/dir -> path/dir/file
    install_file2 "$1" "$2/`basename $1`"
}

install_file2 () {
    # path/file path/dir/file2 -> path/dir/file2
    install -D -m `mode $1` "$1" "${DEBIAN_PREFIX%%/}/${2##/}"
}

install_symlink () {
    DEST="${DEBIAN_PREFIX%%/}/${2##/}"
    mkdir -p "`dirname $DEST`"
    ln -sf "$1" "$DEST"
}

##

install_icons () {
    ( cd "$1" && find -maxdepth 1 -name '*.png' ) | while read file; do
    	install_file2 "$1/$file" "$2/`echo $file | tr = /`"
    done
}

install_package () {
    for p in desktop-droid.py desktop_droid/*.py desktop_droid/ui/*.py; do
    	install_file "$p" "$PREFIX/share/desktop-droid/`dirname $p`"
    done
}


##

mode () {
    if [ -x "$1" ]; then
    	echo 755
    else
    	echo 644
    fi
}

##

case "$1" in
    install)
	install_package
	install_icons desktop_droid/icons "$ICONS"
	install_file config/desktop-droid.desktop "$DESKTOP"
	install_symlink "$PREFIX/share/desktop-droid/desktop-droid.py" "$BIN/desktop-droid"
	;;

    *)
	echo "Doing nothing, please pass 'install' as the first argument."
	;;
esac
