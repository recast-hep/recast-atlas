FROM alpine
RUN  apk add py-pip automake autoconf libtool \
             python-dev musl-dev libffi-dev \
             python-dev musl-dev libffi-dev gcc \
             autoconf curl gcc ipset ipset-dev iptables iptables-dev libnfnetlink libnfnetlink-dev libnl3 libnl3-dev make musl-dev openssl openssl-dev \
             jq util-linux font-bitstream-type1 build-base graphviz-dev imagemagick graphviz
ADD . /code
WORKDIR /code
RUN pip install -e .[local,kubernetes]
RUN curl https://download.docker.com/linux/static/stable/x86_64/docker-18.03.1-ce.tgz|tar -xzvf - && \
    cp docker/docker /usr/local/bin && \
    rm -rf docker
COPY . /code
ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
ENV PACKTIVITY_CVMFS_LOCATION /cvmfsmounts/cvmfs
ENV PACKTIVITY_CVMFS_PROPAGATION rslave
WORKDIR /work

