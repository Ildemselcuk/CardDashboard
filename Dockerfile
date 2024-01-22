FROM python:3.11-alpine3.19
RUN mkdir /workspace
WORKDIR /workspace
ADD requirements.txt /workspace
RUN apk update && apk add --no-cache python3-dev \
                        gcc \
                        g++ \
                        libc-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . .


RUN chmod 0700 /workspace/gunicorn.sh
CMD /workspace/gunicorn.sh
