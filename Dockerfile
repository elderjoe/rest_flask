FROM    ubuntu:latest

# Install Python
RUN     apt-get update -qq
RUN     apt-get install -y build-essential 
RUN     apt-get install -y git 
RUN     apt-get install -y python python-pip
RUN     apt-get install -y curl 
RUN     curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
RUN     chmod a+rx /usr/local/bin/youtube-dl
RUN     pip install --upgrade pip
RUN     git clone https://github.com/elderjoe/rest_flask.git
RUN     cp -R rest_flask /home \
        && rm -rf rest_flask
RUN     cp /home/rest_flask/requirements.txt /tmp/ \
        && pip install requirements.txt