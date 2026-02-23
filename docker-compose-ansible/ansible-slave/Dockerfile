FROM alpine:3.9

RUN apk update && \
    apk add --no-cache openssh python3 sudo

RUN adduser -D ansible && \
    echo "ansible:ansible" | chpasswd && \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN ssh-keygen -A

EXPOSE 22

CMD [ "/usr/sbin/sshd", "-D" ]