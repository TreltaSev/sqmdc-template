FROM alpine:3.19

## Install Packages
RUN apk add --update --no-cache python3 git libpq-dev gcc py3-pip python3-dev g++ py3-virtualenv

# Copy Project

WORKDIR /backend

# Copy requirements
COPY backend/requirements.txt ./

# Build venv using virtualenv (ensures pip is present)
RUN python3 -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements using the venv's pip
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

COPY backend/dev.entrypoint.sh /dev.entrypoint.sh
RUN chmod +x /dev.entrypoint.sh

ENTRYPOINT [ "/dev.entrypoint.sh" ]