#!/bin/bash

LOG_FILE="/root/installation.log"
IP_ADDRESS=$(curl ifconfig.me)

(
  cd /root

  apt-get update
  apt-get install -y curl
  apt-get install -y net-tools
  apt-get install -y zip unzip
  apt-get install -y python3-pip
  echo "-----> Packages installed."

  apt-get remove docker docker-engine docker.io containerd runc
  apt-get install -y ca-certificates gnupg lsb-release
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io
  echo "-----> Installation completed: docker"

  curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  echo "-----> Installation completed: docker-compose"

  git clone https://oguzhanagkus:5y5TNaQukGJyvn5DNH3h@bitbucket.org/musaade/entrance-system.git
  cd entrance-system
  echo "-----> Project cloned."

  docker-compose build
  docker-compose up -d
  echo "-----> System is running."

  curl --insecure -X POST -d "company_name={{company_name_placeholder}}&ip=$IP_ADDRESS" https://164.92.240.177/completed/

) 2>&1 | tee $LOG_FILE
