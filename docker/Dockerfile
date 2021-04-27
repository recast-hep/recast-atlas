FROM docker:20.10.5
RUN  apk add py-pip automake autoconf libtool \
             python3 python3-dev musl-dev libffi-dev tree \
             python3-dev musl-dev libffi-dev gcc \
             autoconf curl gcc ipset ipset-dev iptables iptables-dev libnfnetlink libnfnetlink-dev libnl3 libnl3-dev make musl-dev openssl openssl-dev \
             jq util-linux font-bitstream-type1 build-base graphviz-dev imagemagick graphviz gcc musl-dev python3-dev libffi-dev openssl-dev cargo libxml2-dev libxslt-dev
WORKDIR /code
COPY . /code
RUN pip3 install lxml cryptography jq
RUN pip3 install -e .[local,kubernetes]
RUN python3 -m venv reanaenv && \
    source reanaenv/bin/activate && pip install -U https://github.com/reanahub/reana-client/archive/refs/heads/maint-0.7.zip && \
    pip3 install -e .
ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /shared-mounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave
WORKDIR /work

