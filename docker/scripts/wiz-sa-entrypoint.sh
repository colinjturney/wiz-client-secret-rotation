#!/bin/bash

# Validate WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET. Write to file.
if [ "${WIZ_INITIAL_CLIENT_ID}" = "client_id" ] || [ "${WIZ_INITIAL_CLIENT_SECRET}" = "client_secret" ]; then \
    echo "Error: WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET environment variables must be set." >&2; \
    exit 1; \
fi

echo "export WIZ_CLIENT_ID=${WIZ_INITIAL_CLIENT_ID}" > /opt/wiz-sa-rotate/bin/wiz-auth.sh
echo "export WIZ_CLIENT_SECRET=${WIZ_INITIAL_CLIENT_SECRET}" >> /opt/wiz-sa-rotate/bin/wiz-auth.sh
chmod 0600 /opt/wiz-sa-rotate/bin/wiz-auth.sh

# Validate WIZ_ROTATE_DAYS and set up the cron job
if [[ ! " @yearly @monthly @weekly @daily @hourly @reboot " =~ "${WIZ_ROTATE_OPTION}" ]]; then \
    echo "Invalid WIZ_ROTATE_OPTION set: ${WIZ_ROTATE_OPTION}. Choose from yearly, monthly, weekly, daily, hourly, reboot."; \
    exit 1; \
fi

crontab -l 2>/dev/null; echo "@${WIZ_ROTATE_OPTION} /opt/wiz-sa-rotate/bin/wiz-sa-rotate.sh >> /var/log/cron.log 2>&1" | crontab -

tail -f /dev/null