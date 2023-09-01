FROM ubuntu:latest

ARG app_dir_name

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y git python3 openssh-server python3-pip systemd

# Generate a random password for the root user (you can change this)
RUN PASSWORD=$(openssl rand -base64 12) && echo "root:${PASSWORD}" | chpasswd

# Set the timezone to America/Sao_Paulo
RUN ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN echo "America/Sao_Paulo" > /etc/timezone

RUN mkdir /run/sshd
RUN chown root.root /run/sshd
RUN chmod 0755 /run/sshd

# Generate SSH host keys
RUN ssh-keygen -A

# Copy the public key into the container
COPY ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN chown root:root /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

# Configure SSH to allow key-based authentication and disable password authentication
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication no/PasswordAuthentication no/' /etc/ssh/sshd_config

COPY $app_dir_name/config/ubuntu-packages.txt /root
RUN cat /root/ubuntu-packages.txt | xargs apt install -y

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY $app_dir_name/config/requirements.txt /root
RUN pip3 install -r /root/requirements.txt

WORKDIR /root/$app_dir_name

RUN echo "git config --global --add safe.directory /root/$app_dir_name" >> /root/.profile
RUN chmod 600 /root/.profile

EXPOSE 22
EXPOSE 5000
EXPOSE 6000

RUN echo "#!/bin/bash" > /root/startup.sh \
    && echo "/usr/sbin/sshd -D &" >> /root/startup.sh \
    && echo "tail -f /dev/null" >> /root/startup.sh \
    && chmod +x /root/startup.sh

# Start the startup script when the container starts
ENTRYPOINT ["/bin/bash", "/root/startup.sh"]
