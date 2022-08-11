#!/bin/bash

sudo cp app.service /etc/systemd/system/ohmcontrol.service
sudo systemctl daemon-reload && sudo systemctl enable ohmcontrol && sudo systemctl start ohmcontrol --no-block
