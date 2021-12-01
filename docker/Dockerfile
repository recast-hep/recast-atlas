FROM docker:20.10.5

RUN apk add --update && \
    apk add --no-cache \
        build-base \
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

WORKDIR /code
COPY . /code

RUN python3 -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
    python3 -m pip --no-cache-dir install \
        lxml \
        cryptography \
        jq && \
    python3 -m pip --no-cache-dir install .[local,kubernetes,reana]

ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /shared-mounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave

WORKDIR /work
