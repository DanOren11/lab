FROM alpine:3.9

RUN apk update && \
    apk add ansible openssh-client sshpass python3 && \
    apk add openssh-server

RUN adduser -D ansible && \
    echo "ansible:ansible" | chpasswd && \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN ssh-keygen -A

WORKDIR /home/ansible

EXPOSE 22

CMD [ "/usr/sbin/sshd", "-D" ]