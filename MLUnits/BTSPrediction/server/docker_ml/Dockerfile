FROM minhtribk12/arm_tfx2:1.0
MAINTAINER tri.m.nguyen@aalto.fi

RUN apt-get install -y vim dnsutils curl iputils-ping
COPY ./docker_ml/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 uninstall -y futures
RUN pip3 install qoa4ml==0.0.59
# RUN pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime 
ADD ../docker_ml/ /home/task_dir
ADD ../task_template/utilities /home/task_dir/utilities
ADD ../exported_models/ /home/task_dir/exported_models
ADD ../task_template/*.py /home/task_dir
RUN chmod +x /home/task_dir/task.py
RUN chmod +x /home/task_dir/run.sh
RUN echo "export OPENBLAS_CORETYPE=ARMV8" >> ~/.bashrc

WORKDIR /home/task_dir

# ENTRYPOINT ["tail", "-f", "/dev/null"]
# ENTRYPOINT ["python3", "task.py"]
CMD /bin/bash run.sh