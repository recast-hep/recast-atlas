FROM fedora:28
RUN dnf install -y gcc gcc-c++ graphviz-devel ImageMagick python python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool redhat-rpm-config make; dnf clean all 
WORKDIR /code
COPY lxplus_reqs.txt /code/lxplus_reqs.txt
RUN pip install -r lxplus_reqs.txt
RUN curl https://download.docker.com/linux/static/stable/x86_64/docker-18.03.1-ce.tgz|tar -xzvf - && \
    cp docker/docker /usr/local/bin && \
    rm -rf docker
COPY . /code
ENV PACKTIVITY_DOCKER_CMD_MOD "-u root"
RUN pip install -e .
WORKDIR /work

