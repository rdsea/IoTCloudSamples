FROM minhtribk12/light-ubuntu:1.0
MAINTAINER tri.m.nguyen@aalto.fi

RUN apt update
RUN apt install -y python3-pip 
RUN apt-get install -y vim dnsutils curl iputils-ping
# RUN pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime 
COPY ./docker_data_proc/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install qoa4ml==0.0.59
ADD ../docker_data_proc /home/task_dir
ADD ../task_template/utilities /home/task_dir/utilities
ADD ../task_template/*.py /home/task_dir
# ADD ../exported_models /home/exported_models
RUN chmod 777 /home/task_dir/task.py
WORKDIR /home/task_dir



CMD python3 task.py
# ENTRYPOINT ["tail", "-f", "/dev/null"]
