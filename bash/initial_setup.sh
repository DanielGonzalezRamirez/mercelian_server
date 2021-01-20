#!/bin/bash

# Update and upgrade machine
apt update
apt upgrade

# Install nginx server, certbot for SSL and rsync for loading files
apt install nginx
apt install python3-certbot-nginx
apt install rsync

# After initial setup web page and email server should be set
