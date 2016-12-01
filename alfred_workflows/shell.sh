#!/bin/bash

full_prog="${SCRIPT_DIR}/${1}.${SCRIPT_EXT}"
back_text="${SCRIPT_DIR}/${SCRIPT_LOG}"

echo ":: $(date "+%Y-%m-%d %H:%M:%S") [{query}]" >> "${back_text}" 2>&1
/usr/local/bin/bash "${full_prog}" >> "${back_text}" 2>&1
