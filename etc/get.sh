#!/usr/bin/env bash

for script in \
    "/Volumes/Großhirn/disk_mirror.sh" \
    "/Volumes/Kleinhirn/disk_fetch.sh" \
; do
    [ ! -f "$script" ] && { echo "MISSING: $script"; continue; }
    cp -v "$script" .
done
