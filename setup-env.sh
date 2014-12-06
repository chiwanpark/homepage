#!/bin/bash

sudo apt-get -y install python-software-properties
sudo add-apt-repository -y ppa:fkrull/deadsnakes
sudo apt-add-repository -y ppa:chris-lea/node.js
sudo apt-get -y update
sudo apt-get -y install nodejs git python3.4-dev python3.4
npm config set strict-ssl false
npm install -g less
