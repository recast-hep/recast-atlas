# FROM docker:20.10.5
# RUN  apk add py-pip automake autoconf libtool \
#              python3 python3-dev musl-dev libffi-dev tree \
#              python3-dev musl-dev libffi-dev gcc \
#              autoconf curl gcc ipset ipset-dev iptables iptables-dev libnfnetlink libnfnetlink-dev libnl3 libnl3-dev make musl-dev openssl openssl-dev \
#              jq util-linux font-bitstream-type1 build-base graphviz-dev imagemagick graphviz gcc musl-dev python3-dev libffi-dev openssl-dev cargo libxml2-dev libxslt-dev
FROM python:3.8-slim-bullseye as base

RUN apt-get update -y \
    && apt-get install -y \
        automake \
        autoconf \
        libtool \
        python3-dev \
        musl-dev \
        libffi-dev \
        tree \
        curl \
        gcc \
        ipset \
        iptables \
        libnfnetlink0 \
        libnfnetlink-dev \
        libnl-3-200 \
        libnl-3-dev \
        make \
        libssl-dev \
        jq \
        util-linux \
        ttf-bitstream-vera \
        build-essential \
        graphviz-dev \
        imagemagick \
        graphviz \
        cargo \
        libxml2-dev \
        libxslt-dev

WORKDIR /code
COPY . /code
# RUN pip3 install lxml cryptography jq
# RUN pip3 install -e .[local,kubernetes,reana]
RUN python -m pip --no-cache-dir install --upgrade pip 'setuptools<58.0.0' wheel \
    && python -m pip --no-cache-dir install \
        lxml \
        cryptography \
        jq \
    && python -m pip --no-cache-dir install .[local,kubernetes,reana] \
    && rm -rf /tmp/*

ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /shared-mounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave

WORKDIR /work
CMD [ "/bin/bash" ]

