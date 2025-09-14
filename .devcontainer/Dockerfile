FROM archlinux:multilib-devel

# === SYSTEM SETUP ===
# Update database files for 'core' and 'extra'
RUN pacman -Sy
COPY .bashrc /.bashrc

# === USER SETUP ===
# Create vscode user
RUN useradd -m -s /bin/bash -u 1000 -U vscode
# Make vscode user sudo
RUN usermod -aG wheel vscode
RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel
# Use vscode user
USER vscode

# === POST SETUP ===
# Copy init.sh file over
COPY init.sh /init.sh
RUN chmod +x /init.sh
# Run init script
RUN /init.sh
