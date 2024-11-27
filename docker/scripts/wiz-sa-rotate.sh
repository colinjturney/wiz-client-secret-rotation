#!/bin/bash

source /opt/wiz-sa-rotate/bin/wiz-auth.sh

python rotate.py "${WIZ_CLIENT_ID}" "${WIZ_CLIENT_SECRET}"