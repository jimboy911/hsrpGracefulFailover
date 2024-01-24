README.md

This script is intended for routers or layer 3 switches that are configured in HSRP pairs.
It is intended to log into a standby switch, grab its HSRP group(s) and creates a configuration file, that you can copy and paste, to gracefully failover the HSRP group to the secondary switch
(during a maintenance window on the primary router, for example).
It also provides configuration (in the same file) on restoring the original priority in order to gracefully fail back over to dis1.

Before you can run this script, you'll have to get python and netmiko installed.
in order to install netmiko, see the commands below (in this case I used a virtual environment in a folder called "netmiko_test").

If using Windows:

py -m pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" <<<< workaround for ssl cert error

py -m pip install --upgrade pip <<<< upgrades pip

py -m pip install virtualenv <<<< installs venv module

py -m venv netmiko_venv <<<< creates venv folder

./netmiko_venv/Scripts/activate <<<< jumps into virtual environment

py -m pip install netmiko <<<< installs netmiko

########################

./netmiko_venv/Scripts/activate

py hsrp.py

It will ask you for the IP address, username, and password.

It will then log into the switch and examine the standby configuration.

it will generate a Cisco IOS file with the hostname and date / time that you can open up in a text edtior, verify the configurations and copy and paste them into the switch.
