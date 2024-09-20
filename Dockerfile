FROM sickp/alpine-sshd:latest
ADD tests/keys/id_rsa.pub /home/sshreader/.ssh/authorized_keys
RUN \
  passwd -d root && \
  adduser -D -s /bin/sh sshreader && \
  echo "sshreader:sunshine" | chpasswd && \
  chown -R sshreader:sshreader /home/sshreader && \
  ssh-keygen -A