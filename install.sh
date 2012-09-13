#!/bin/bash

if [ ! -f /usr/bin/python ];
then
	echo "ERROR: python not installed!"
	exit 1
fi

echo "Installing dependencies"
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py
easy_install pip
pip install redis
pip install argparse
pip install daemon
pip install ConfigParser
rm -rf ez_setup.py

echo "Installing in /usr/local/capi"
if [ -d "/usr/local/capi" ]; then
	mkdir /usr/local/capi
fi
cp -rf ./capi* /usr/local/capi/

echo "Installing init.d script"
if [ ! -f /etc/capid.conf ];
then
	cp ./files/capid.conf /etc/capid.conf
fi
cp -f ./files/capid /etc/init.d/capid
chmod +x /etc/init.d/capid

echo "Edit /etc/capid.conf to fit your needs and then start the service: service capid restart"