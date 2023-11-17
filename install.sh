#!/bin/bash

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install tmux
sudo apt update
sudo apt install linux-headers-$(uname -r)
sudo apt-get install build-essential
make -f script/Makefile