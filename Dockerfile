FROM    ubuntu:latest

# Install Python
RUN     apt-get update -qq
RUN     apt-get install -y build-essential 
RUN     apt-get install -y git 
RUN     apt-get install -y python python-pip
RUN     apt-get install -y curl 
RUN     apt-get install -y ffmpeg
RUN     curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
RUN     chmod a+rx /usr/local/bin/youtube-dl
RUN     pip install --upgrade pip
RUN     git clone https://github.com/elderjoe/rest_flask.git
RUN     cp -R rest_flask /home \
        && rm -rf rest_flask
RUN     cd /home/rest_flask \
        && git pull \
        && chmod 777 .
RUN     cp /home/rest_flask/development.txt /tmp/ \
        && pip install -r /tmp/development.txt
RUN     pip install -U youtube-dl
RUN     apt-get install -y vsftpd
RUN     apt-get install -y ftp
RUN     apt-get install -y nano
RUN     cp /home/rest_flask/ftpconf/vsftpd /etc/init.d/vsftpd
RUN     cp /home/rest_flask/ftpconf/vsftpd.conf /etc/vsftpd
EXPOSE  5000
EXPOSE  20
