#!/bin/bash

# Install Justfile
npm i -g rust-just

# Install Bun because we're not losers :)
npm i -g bun

# Make a file so we know we're not crazy
touch ./a.txt
echo "aaaa" > ./a.txt