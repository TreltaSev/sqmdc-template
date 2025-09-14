FROM archlinux:multilib-devel

# Update database files for 'core' and 'extra'
RUN pacman -Sy

# Copy bashrc file over to image
COPY .bashrc /.bashrc

# Copy init.sh file over
COPY init.sh /init.sh
RUN chmod +x /init.sh

RUN /init.sh
