FROM library/python:3.8.7-buster

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY requirements.txt requirements.txt
RUN pip3.8 install -r requirements.txt

COPY . .

CMD ["/bin/bash"]
