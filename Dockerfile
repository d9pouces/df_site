FROM python:3.12-slim AS base
# generate the package in a first image
FROM base AS builder
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_NO_INTERACTION=1 \
  PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/df_site/.local/bin
RUN adduser --disabled-password --gecos "df_site" df_site
COPY ./pyproject.toml /src/pyproject.toml
COPY ./README.md /src/README.md
COPY ./LICENSE /src/LICENSE
COPY CHANGELOG.md /src/CHANGELOG
COPY ./df_site /src/df_site
WORKDIR /src
USER df_site
RUN python3 -m pip install poetry \
    && python3 -m poetry build
# install the package without the build dependencies
FROM base AS runtime
LABEL org.opencontainers.image.authors="github@19pouces.net"
LABEL description="Proof of concept for a modern Django website"
RUN adduser --disabled-password --gecos "Modersite" df_site \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --allow-downgrades --allow-remove-essential --allow-unauthenticated -fuy dist-upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes -qq --no-install-recommends uglifyjs \
    && rm -rf /var/lib/apt/lists/* && mkdir -p /data /usr/local/var/df_site /home/df_site/.local/bin
COPY --from=builder /src/dist /tmp/dist
RUN chown -R df_site:df_site /usr/local/var/df_site /data /tmp/dist /home/df_site
USER df_site
RUN /bin/sh -c "/usr/local/bin/python3 -m pip install --no-warn-script-location --no-cache-dir /tmp/dist/*.tar.gz" \
    && rm -rf /tmp/dist \
    && /usr/local/bin/python3 -m df_site collectstatic --noinput
