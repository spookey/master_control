#!/usr/bin/env bash

REMOTE=${REMOTE-"r300:/tank"}
TARGET=${TARGET-"$REMOTE/disk_mirror"}

SOURCE=${SOURCE-"/Volumes/Großhirn"}
ITSOURCE=${ITSOURCE-"$SOURCE/iTunes"}
PISOURCE=${PISOURCE-"$SOURCE/Pictures"}


msg() { echo "###"; echo "# $*"; echo; }
replicate() {
    local src=$1
    local tgt=$2
    if [ ! -d "$src" ]; then
        msg "ERROR: No such source: $src"
        return 1
    fi

    msg "$(basename "$src")" "=>" "$(basename "$tgt")"
    rsync \
        -avHh --delete-during --stats --progress \
        -e "ssh -T -c arcfour256 -o Compression=no -x" \
        "$src" "$tgt"
    return $?
}

msg "$(basename "$0")"
replicate "$ITSOURCE" "$TARGET" && \
replicate "$PISOURCE" "$TARGET" && \
msg "all done!!1!" && \
exit 0
