FROM sickp/alpine-sshd:latest
MAINTAINER Jesse Almanrode
ADD tests/keys/id_rsa.pub /home/sshreader/.ssh/authorized_keys
RUN \
  passwd -d root && \
  adduser -D -s /bin/ash sshreader && \
  echo "sshreader:sunshine" | chpasswd && \
  chown -R sshreader:sshreader /home/sshreader && \
  ssh-keygen -A