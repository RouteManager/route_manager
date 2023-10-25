# syntax=docker/dockerfile:1

# Enable this to install OSMNX prior to installing requirements.txt
# This greatly speeds up rebuilding of the container if
# changes are made to requirements.txt during dev process
ARG BASE=-with-osmnx

ARG PYTHON_VERSION=3.11-bookworm
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE 6001

# Upgrade pip and create non-root user
ARG UID=10001
RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install --no-install-recommends -y dumb-init libgdal-dev \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" --uid "${UID}" appuser 

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
USER appuser

FROM base AS base-with-osmnx
RUN pip install --no-cache osmnx

FROM base${BASE} AS requirements
COPY  --chown=appuser:appuser ./requirements.txt ./
RUN pip install --no-cache -r requirements.txt

# The code base is share by ALL environmnets 
# to ensure the same code ships to prod as was
# developed and tested against.
FROM requirements as code
COPY  --chown=appuser:appuser . .
CMD python app.py

# Create PROD env from shared code environment
FROM code as prod
CMD python app.py

# Create DEV env from shared code environment
FROM code as dev
CMD python app.py