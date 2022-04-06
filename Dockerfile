FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install python3 git firefox wget python3-pip -y
RUN cd /home && \
    git clone https://github.com/Vaib215/The_ABC_Bot.git && \
    cd ./The_ABC_Bot && \
    pip3 install -r requirements.txt && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar -xvf geckodriver-v0.26.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver
CMD python3 /home/The_ABC_Bot/abc.py
