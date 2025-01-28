#!/bin/bash

source /opt/wiz-sa-rotate/bin/wiz-auth.sh

FORCE_ROTATE="False"

while getopts ":f" opt; do
  case $opt in
    f)
      echo "Forcing rotation"
      FORCE_ROTATE="True"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

python /opt/wiz-sa-rotate/bin/rotate.py "${WIZ_CLIENT_ID}" "${WIZ_CLIENT_SECRET}" "${FORCE_ROTATE}"