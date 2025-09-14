#!/bin/bash

# Install Docker
curl -fsSL https://get.docker.com -o /tmp/scripts/get-docker.sh
sudo sh /tmp/scripts/get-docker.sh

# Install Bun because we're not losers :)
npm i -g bun

# Install Justfile
bun i -g rust-just

# Make a file so we know we're not crazy
touch ./a.txt
echo "aaaa" > ./a.txt