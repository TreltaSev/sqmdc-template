FROM alpine:3.19

## Install Packages
RUN apk add --update --no-cache python3 git libpq-dev gcc py3-pip python3-dev g++ py3-virtualenv

RUN apk add --no-cache ca-certificates

ENV PIP_INDEX_URL=https://pypi.org/simple PIP_DEFAULT_TIMEOUT=60
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# Copy Project

WORKDIR /backend

COPY pyproject.toml requirements.txt pytest.ini ./

# Build venv using virtualenv (ensures pip is present)
RUN python3 -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir src
COPY src/utils ./src/utils

# Install "Self" as backend
RUN /opt/venv/bin/pip install -e .


# Install requirements using the venv's pip
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

COPY test.entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]