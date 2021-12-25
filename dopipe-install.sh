#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# file: dopipe.service
# Service unit-file
#
echo -e \
'[Unit]
Description=Latbot named pipe service
After=multi-user.target
[Service]
User='$USER'
Type=idle
ExecStart='$SCRIPT_DIR'/dopipe.sh
[Install]
WantedBy=multi-user.target
' > ./dopipe.service


# file: dopipe.sh
# Main executable file
#
echo -e \
'#!/bin/bash

rm '$SCRIPT_DIR'/host/commandpipe
mkfifo '$SCRIPT_DIR'/host/commandpipe

while true;
  do eval "$(cat '$SCRIPT_DIR'/host/commandpipe)" &> '$SCRIPT_DIR'/host/output;
done
' > ./dopipe.sh

sudo chmod u=rwx,go= ./dopipe.sh

## Service installation
##
##
sudo systemctl disable dopipe.service
sudo rm -rf /lib/systemd/system/dopipe.service
sudo mv ./dopipe.service /lib/systemd/system/
sudo chmod u=rw,go=r /lib/systemd/system/dopipe.service
sudo systemctl daemon-reload
sudo systemctl enable dopipe.service
sudo systemctl restart dopipe
