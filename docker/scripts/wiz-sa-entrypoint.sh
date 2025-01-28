#!/bin/bash

# Validate WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET. Write to file.
if [ "${WIZ_INITIAL_CLIENT_ID}" = "client_id" ] || [ "${WIZ_INITIAL_CLIENT_SECRET}" = "client_secret" ]; then \
    echo "Error: WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET environment variables must be set." >&2; \
    exit 1; \
fi

echo "export WIZ_CLIENT_ID=${WIZ_INITIAL_CLIENT_ID}" > /opt/wiz-sa-rotate/bin/wiz-auth.sh
echo "export WIZ_CLIENT_SECRET=${WIZ_INITIAL_CLIENT_SECRET}" >> /opt/wiz-sa-rotate/bin/wiz-auth.sh
chmod 0600 /opt/wiz-sa-rotate/bin/wiz-auth.sh

# Run rotation to rotate from WIZ_INITIAL_CLIENT_SECRET
/opt/wiz-sa-rotate/bin/wiz-sa-rotate.sh -f >> /opt/wiz-sa-rotate/log/wiz-rotate.log 2>&1

# Write cronjob for daily check

crontab -l 2>/dev/null; echo "@daily /opt/wiz-sa-rotate/bin/wiz-sa-rotate.sh >> /opt/wiz-sa-rotate/log/wiz-rotate.log 2>&1" | crontab -

tail -f /dev/null