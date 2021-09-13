FROM python@sha256:129e3d1bee00d9e915d49ded6a1103f567c9fb715c8e5fdc1113a6e71d12d3f9

WORKDIR /web-server
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
USER nobody
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:5000", "web_server:app"]
