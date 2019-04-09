#!/bin/bash

#
# spotify-fix-permissions-postinstall.sh
# Source: https://gist.github.com/hjuutilainen/dc6e8b77af0dced03271ef1a10471cb0
#

SPOTIFY_PATH="/Applications/Spotify.app"

if [[ ! -d "${SPOTIFY_PATH}" ]]; then
    echo "File not found: ${SPOTIFY_PATH}"
    exit 1
fi

echo "Fixing Spotify permissions..."

# Find every file executable by its owner
IFS=$'\n'
for EXECUTABLE in $(/usr/bin/find "${SPOTIFY_PATH}" -perm -u=x -type f); do
    PERMISSIONS=$(/usr/bin/stat -f "%Op" "${EXECUTABLE}")
    if [[ ${PERMISSIONS} != "100755" ]]; then
        /bin/chmod 755 "${EXECUTABLE}"
    fi
done

/bin/chmod -R go+rX "${SPOTIFY_PATH}"

exit 0
