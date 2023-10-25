# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11-slim-bookworm
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
    && adduser --disabled-password --gecos "" --uid "${UID}" appuser


# Install gcc and osmnx package, which depends on gdal. Gdal has
# complex dependancies and take a long time to install so is done 
# in a separate layer to speed up installation of other deps during
# develoment. Remove gcc after osmnx is installed
RUN apt-get update \
    && apt-get install --no-install-recommends -y dumb-init libgdal-dev gcc g++ \
    && pip install osmnx \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get remove -y gcc g++ \
    && apt-get -y autoremove

USER appuser

# Install the remainder of the dependancies
COPY --chown=appuser:appuser  ./requirements.txt ./
RUN python -m pip install --no-cache -r requirements.txt
    
# Switch to non-root user
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# The code base is share by ALL environmnets 
# to ensure the same code ships to prod as was
# developed and tested against.
FROM base as code
COPY  --chown=appuser:appuser . .
CMD python app.py

# Create prod env from shared code environment
FROM code as prod
CMD python app.py
