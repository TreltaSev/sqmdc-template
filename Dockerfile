# Use basic node image
FROM mcr.microsoft.com/devcontainers/javascript-node

# Make sure everything is up to date
RUN apt-get update

# Run initialize script
COPY ./.devcontainer/init.sh /tmp/scripts/init.sh
RUN bash /tmp/scripts/init.sh