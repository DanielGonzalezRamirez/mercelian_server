#!/bin/bash

# Be sure that this file is run as root
# Update and upgrade machine
apt update
apt upgrade

# Install nginx server and rsync for loading files
apt install nginx
apt install rsyn

# Install certbot
snap install core
snap refresh core

snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot

# After initial setup, next step is to setup web page and email server
