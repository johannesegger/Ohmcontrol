#!/bin/bash

sudo apt update && sudo apt install -y python3-pip
sudo pip install pyserial

sudo mkdir -p /opt/ohmcontrol && sudo cp app.py fn.py pwm.py /opt/ohmcontrol
sudo cp app.service /etc/systemd/system/ohmcontrol.service
sudo systemctl daemon-reload && sudo systemctl enable ohmcontrol && sudo systemctl start ohmcontrol --no-block
