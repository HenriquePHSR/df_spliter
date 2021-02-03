FROM python:3.8.3-slim

RUN apt-get update
RUN apt-get install --no-install-recommends -y sudo
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip install pandas xlrd==1.2.0 openpyxl

RUN groupadd -g 1000 app \
    && useradd -u 1000 -g app -s /bin/bash -m app \
    && usermod -aG sudo app \
    && echo 'app    ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    # && mkdir -p /usr/src/app \
    && chown -R app:app /usr/src 
    # && chmod -R 777 /usr/src/app

WORKDIR /script

COPY . /script/

CMD /bin/bash
