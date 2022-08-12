#!/bin/bash

sudo mkdir -p /opt/ohmcontrol && sudo cp app.py /opt/ohmcontrol
sudo cp app.service /etc/systemd/system/ohmcontrol.service
sudo systemctl daemon-reload && sudo systemctl enable ohmcontrol && sudo systemctl start ohmcontrol --no-block
