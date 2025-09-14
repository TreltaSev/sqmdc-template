#!/bin/bash

# Ensure bashrc
source /.bashrc

# === USER SETUP ===

# # Docker user
# groupadd -g 998 docker || true
# usermod -aG docker vscode

# copy bashrc file over
cp /.bashrc /home/vscode/.bashrc