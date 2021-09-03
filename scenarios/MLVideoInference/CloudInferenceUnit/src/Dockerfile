FROM nvidia/cuda:10.1-devel-ubuntu18.04
RUN apt update
RUN apt install -y git wget make build-essential manpages-dev python

WORKDIR /inference

RUN git clone https://github.com/pjreddie/darknet.git
RUN cd darknet

WORKDIR /inference/darknet
RUN sed -i "1s/.*/GPU=1/" Makefile
RUN make

RUN wget https://pjreddie.com/media/files/yolov3.weights

#install web-server dependencies
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
COPY requirements.txt requirements.txt
RUN ["mkdir", "/inference/temp"]
RUN apt-get -o Dpkg::Options::='--force-confmiss' install --reinstall -y netbase

RUN pip install -r requirements.txt
COPY . . 
# Injecting customized python version for calling the object detection

EXPOSE 4000
CMD ["gunicorn", "--workers=2", "--timeout", "15", "-k", "eventlet", "-b", "0.0.0.0:4000", "server:app"]