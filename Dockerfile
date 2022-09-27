FROM debian:buster-slim

ENV BUILD_PACKAGES="\
        build-essential \
        python3-dev \
        cmake \
        tcl-dev \
        xz-utils \
        zlib1g-dev \
        git \
        curl \
	pkg-config \
        unzip" \
    APT_PACKAGES="\
        ca-certificates \
        openssl \
        bash \
        graphviz \
        fonts-noto \
        libpng16-16 \
        libfreetype6 \
        libjpeg62-turbo \
        libgomp1 \
	libhdf5-dev \
        python3 \
        python3-pip" \
    LANG=C.UTF-8

# get system packages
RUN set -ex; \
    apt-get update -y; \
    apt-get install -y --no-install-recommends ${APT_PACKAGES}; \
    apt-get install -y --no-install-recommends ${BUILD_PACKAGES};


# get python packages
COPY requirements-cpu.txt /opt/requirements-cpu.txt
RUN set -ex; \
    pip3 install -U wheel setuptools; \
    pip3 install -r /opt/requirements-cpu.txt;

# get source code
COPY . /opt/DeepCreamPy

WORKDIR /opt/DeepCreamPy

ENTRYPOINT [ "/usr/bin/python3", "decensor.py" ]
