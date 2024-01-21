FROM python:3.9-alpine
RUN mkdir /workspace
WORKDIR /workspace
ADD requirements.txt /workspace
RUN apk update && apk add --no-cache python3-dev \
                        gcc \
                        g++ \
                        libc-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN sh -c "sed -i 's/from\ flask\._compat\ import\ with_metaclass/from\ six\ import\ with_metaclass/g' /usr/local/lib/python3.9/site-packages/flask_allows/requirements.py"
ADD . .

# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade
CMD exec gunicorn main:app --bind 0.0.0.0:8000 --workers 3 \
--timeout 120 \
--log-level=debug
