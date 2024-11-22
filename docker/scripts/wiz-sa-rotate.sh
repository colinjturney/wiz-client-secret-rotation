#!/bin/bash

WIZ_ROTATE_DAYS=${1}

if ! [[ "${WIZ_ROTATE_DAYS}" =~ ^[0-9]+$ ]] || (( "${WIZ_ROTATE_DAYS}" < 0 )); then \
    echo "Error: WIZ_ROTATE_DAYS must be set to a non-negative integer." >&2; \
    exit 1; \
fi

source wiz_auth.sh

python rotate.py "${WIZ_CLIENT_ID}" "${WIZ_CLIENT_SECRET}"