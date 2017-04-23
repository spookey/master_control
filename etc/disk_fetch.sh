#!/usr/bin/env bash

TARGET=${TARGET-"/Volumes/Kleinhirn/Großhirn"}
SOURCE=${SOURCE-"/Volumes/Großhirn"}

BFSOURCE=${BFSOURCE-"$SOURCE/_buffer"}
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
        "$src" "$tgt"
    return $?
}

msg "$(basename "$0")"
replicate "$ITSOURCE" "$TARGET" && \
replicate "$PISOURCE" "$TARGET" && \
replicate "$BFSOURCE" "$TARGET" && \
msg "all done!!1!" && \
exit 0
