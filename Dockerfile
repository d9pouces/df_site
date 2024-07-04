FROM python:3.12-slim AS base
# generate the package in a first image
FROM base AS builder
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_NO_INTERACTION=1
COPY ./pyproject.toml /src/pyproject.toml
COPY ./README.md /src/README.md
COPY ./LICENSE /src/LICENSE
COPY CHANGELOG.md /src/CHANGELOG
COPY ./modersite /src/modersite
WORKDIR /src
RUN adduser --disabled-password --gecos "Modersite" modersite
USER modersite
RUN python3 -m pip install poetry \
    && python3 -m poetry build
# install the package without the build dependencies
FROM base AS runtime
LABEL org.opencontainers.image.authors="github@19pouces.net"
LABEL description="Proof of concept for a modern Django website"
COPY --from=builder /src/dist /tmp/dist
RUN adduser --disabled-password --gecos "Modersite" modersite \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --allow-downgrades --allow-remove-essential --allow-unauthenticated -fuy dist-upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes -qq --no-install-recommends uglifyjs \
    && rm -rf /var/lib/apt/lists/* && mkdir -p /data /usr/local/var/modersite /home/modersite/.local/bin \
    && chown -R modersite:modersite /usr/local/var/modersite /data /tmp/dist /home/modersite
USER modersite
RUN /bin/sh -c "/usr/local/bin/python3 -m pip install --no-warn-script-location --no-cache-dir /tmp/dist/*.tar.gz" \
    && rm -rf /tmp/dist \
    && /usr/local/bin/python3 -m modersite collectstatic --noinput
