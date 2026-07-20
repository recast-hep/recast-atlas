# NOTE: docker:27-cli (Alpine 3.20) is the newest base with Python 3.12;
# the yadage stack (packtivity) needs the 'pipes' module removed in Python 3.13
FROM docker:27-cli

RUN apk add --update && \
    apk add --no-cache \
        apptainer \
        bash \
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
        py3-pip \
        python3 \
        python3-dev \
        cargo \
        tree \
        jq \
        graphviz \
        graphviz-dev \
        imagemagick \
        font-bitstream-type1 \
        ttf-freefont \
        tzdata && \
    # apptainer bind-mounts /etc/localtime, which Alpine does not ship by default
    cp /usr/share/zoneinfo/UTC /etc/localtime

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
    # graphviz plugin libs live outside the default linker path on Alpine
    LDFLAGS="-L/usr/lib/graphviz -Wl,-rpath,/usr/lib/graphviz" \
        uv --no-cache pip install '.[local,kubernetes,reana]' 'setuptools<81' && \
    recast --help

# snakemake lives in its own virtual environment as reana-client pins an
# incompatible snakemake version; recast only invokes the snakemake CLI
RUN python3 -m venv /usr/local/snakemake-venv && \
    /usr/local/venv/bin/uv --no-cache pip install \
        --python /usr/local/snakemake-venv/bin/python 'snakemake>=8.0' && \
    ln -sf /usr/local/snakemake-venv/bin/snakemake /usr/local/venv/bin/snakemake && \
    [ "$(snakemake --version | cut -d. -f1)" -ge 8 ] && \
    apptainer version

ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /shared-mounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave

WORKDIR /work
