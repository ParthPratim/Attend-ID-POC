FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
RUN add-apt-repository 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe'
RUN apt update
RUN apt install -y sawtooth

RUN python3 -m pip install tornado bigchaindb_driver
RUN apt-get install -y curl
RUN python3 -m pip install pyopenssl ipfshttpclient
RUN python3 -m pip install --upgrade protobuf grpcio-tools
RUN python3 -m pip install pillow imutils

RUN apt-get update
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
RUN curl -LO http://github.com/opencv/opencv/archive/master.zip
RUN apt-get install -y unzip
RUN unzip master.zip
WORKDIR opencv-master
RUN mkdir build
WORKDIR build
RUN cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
RUN make -j4
RUN make install
RUN python3 -m pip install dlib
RUN python3 -m pip install opencv-python
WORKDIR ../../
RUN python3 -m pip install scipy==1.0.0 scikit-learn tensorflow numpy==1.16.2
RUN python3 -m pip install supervisor
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs
