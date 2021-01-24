FROM library/python:3.7.4-alpine3.9

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY requirements.txt requirements.txt
RUN pip3.7 install -r requirements.txt

COPY . .

CMD ["/bin/bash"]
