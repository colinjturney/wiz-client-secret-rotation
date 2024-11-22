# Use the latest stable Ubuntu base image
FROM ubuntu:24.10

# Define environment variables and defaults
ENV WIZ_ROTATE_HOME="/opt/wiz-sa-rotate"
ENV WIZ_ROTATE_OPTION="monthly"
ENV WIZ_INITIAL_CLIENT_ID="client_id"
ENV WIZ_INITIAL_CLIENT_SECRET="client_secret"

# Install cron
RUN apt-get update && apt-get install -y cron

# Make directory for wiz-sa-rotate and copy scripts to this location
RUN mkdir -p "${WIZ_ROTATE_HOME}/bin"
COPY scripts/rotate.py "${WIZ_ROTATE_HOME}/bin"
COPY scripts/wiz-auth.sh "${WIZ_ROTATE_HOME}/bin"
COPY scripts/wiz-sa-rotate.sh "${WIZ_ROTATE_HOME}/bin"

# Make the scripts executable
RUN chmod +x "${WIZ_ROTATE_HOME}/bin/wiz-sa-rotate.sh"
RUN chmod +x "${WIZ_ROTATE_HOME}/bin/rotate.py"

# Validate WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET. Write to file.
RUN if [ "${WIZ_INITIAL_CLIENT_ID}" = "client_id" ] || [ "${WIZ_INITIAL_CLIENT_SECRET}" = "client_secret" ]; then \
        echo "Error: WIZ_INITIAL_CLIENT_ID and WIZ_INITIAL_CLIENT_SECRET environment variables must be set." >&2; \
        exit 1; \
    fi

RUN echo "export WIZ_CLIENT_ID=${WIZ_CLIENT_ID}" > ${WIZ_ROTATE_HOME}/bin/wiz-auth.sh
RUN echo "export WIZ_CLIENT_SECRET=${WIZ_CLIENT_SECRET}" >> ${WIZ_ROTATE_HOME}/bin/wiz-auth.sh

# Validate WIZ_ROTATE_DAYS and set up the cron job
RUN if [[ ! " @yearly @monthly @weekly @daily @hourly @reboot " =~ " ${CRON_SHORTCUT} " ]]; then \
        echo "Invalid WIZ_ROTATE_OPTION set: ${CRON_SHORTCUT}. Choose from yearly, monthly, weekly, daily, hourly, reboot."; \
        exit 1; \
    fi

RUN (crontab -l 2>/dev/null; echo "@${WIZ_ROTATE_OPTION} ${WIZ_ROTATE_HOME}/bin/wiz-sa-rotate.sh >> /var/log/cron.log 2>&1") | crontab -

# Python dependencies
COPY scripts/requirements.txt ${WIZ_ROTATE_HOME}/bin

RUN pip install --no-cache-dir -r ${WIZ_ROTATE_HOME}/bin/requirements.txt

# Command to run when the container starts
CMD ["cron", "-f"]