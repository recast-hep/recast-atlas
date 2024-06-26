FROM docker:20.10.5

RUN apk add --update && \
    apk add --no-cache \
        build-base \
        git \
        gcc \
        make \
        automake \
        autoconf \
        curl \
        musl-dev \
        libtool \
        util-linux \
        ipset \
        ipset-dev \
        iptables \
        iptables-dev \
        libnfnetlink \
        libnfnetlink-dev \
        libnl3 \
        libnl3-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        openssl \
        openssl-dev \
        py-pip \
        python3 \
        python3-dev \
        cargo \
        tree \
        jq \
        graphviz \
        graphviz-dev \
        imagemagick \
        font-bitstream-type1 \
        ttf-freefont

COPY . /code

# Set PATH to pickup virtual environment by default
ENV PATH=/usr/local/venv/bin:"${PATH}"
RUN python3 -m venv /usr/local/venv && \
    . /usr/local/venv/bin/activate && \
    cd /code && \
    python -m pip --no-cache-dir install --upgrade uv && \
    uv --no-cache pip install --upgrade pip wheel && \
    uv --no-cache pip install \
        lxml \
        cryptography \
        jq && \
    uv --no-cache pip install '.[local,kubernetes,reana]' && \
    recast --help

ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /shared-mounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave

WORKDIR /work
