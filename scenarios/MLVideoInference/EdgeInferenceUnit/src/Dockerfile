FROM ubuntu@sha256:3f7c2c6e153e218a10ff78b3868811795fa09cc5d01be28296390ac75ab018b0
RUN apt update
RUN apt install -y git wget make build-essential manpages-dev python2-dev

WORKDIR /inference

RUN git clone https://github.com/pjreddie/darknet.git
RUN cd darknet

WORKDIR /inference/darknet
RUN make

RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

#install web-server dependencies
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
COPY requirements.txt requirements.txt
RUN ["mkdir", "/inference/temp"]

RUN pip install -r requirements.txt
COPY . . 
# Injecting customized python version for calling the object detection

EXPOSE 4002
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:4002", "server:app"]