FROM library/python:3.7.4-alpine3.9

RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONPATH=/usr/lib/python3.7/site-packages

COPY requirements.txt requirements.txt
RUN pip3.7 install -r requirements.txt

COPY . .

CMD ["/bin/bash"]
