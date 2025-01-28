# Use the latest stable Ubuntu base image
FROM python:3.13-bullseye

# Define environment variables and defaults
ENV WIZ_INITIAL_CLIENT_ID="client_id"
ENV WIZ_INITIAL_CLIENT_SECRET="client_secret"

# Install cron
RUN apt-get update && apt-get install -y cron

# Make directories for wiz-sa-rotate and copy scripts to this location
RUN mkdir -p /opt/wiz-sa-rotate/bin
RUN mkdir -p /opt/wiz-sa-rotate/log

COPY scripts/rotate.py /opt/wiz-sa-rotate/bin/rotate.py
COPY scripts/wiz-auth.sh /opt/wiz-sa-rotate/bin/wiz-auth.sh
COPY scripts/wiz-sa-entrypoint.sh /opt/wiz-sa-rotate/bin/wiz-sa-entrypoint.sh
COPY scripts/wiz-sa-rotate.sh /opt/wiz-sa-rotate/bin/wiz-sa-rotate.sh

# Make the scripts executable
RUN chmod 0777 "/opt/wiz-sa-rotate/bin/wiz-sa-entrypoint.sh"
RUN chmod +w "/opt/wiz-sa-rotate/bin/wiz-auth.sh"
RUN chmod +x "/opt/wiz-sa-rotate/bin/wiz-sa-rotate.sh"
RUN chmod +x "/opt/wiz-sa-rotate/bin/rotate.py"

# Python dependencies
RUN apt-get update && apt-get install -y python3-pip
COPY scripts/requirements.txt /opt/wiz-sa-rotate/bin

RUN pip3 install -r /opt/wiz-sa-rotate/bin/requirements.txt

# Command to run when the container starts

ENTRYPOINT ["/opt/wiz-sa-rotate/bin/wiz-sa-entrypoint.sh"]