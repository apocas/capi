#!/bin/bash

echo "Installing dependencies"
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py
easy_install pip
pip install redis
pip install argparse
pip install daemon
pip install ConfigParser

echo "Installing in /usr/local/capi"
mkdir /usr/local/capi
cp -r ./capi* /usr/local/capi/

echo "Installing init.d script /etc/init.d/capid"
cp ./files/capid /etc/init.d/
chmod +x /etc/init.d/capid