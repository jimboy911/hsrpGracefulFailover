#This Python script checks the standby configuration on the standby router for a pair of routers configured with HSRP
#it then creates a config file that you can copy and paste into the secondary router to gracefully failover the interfaces to the standby router
#it also provides configurations, in the same file, that you can use to fail back over the standby groups to the primary router.

from netmiko import ConnectHandler
import json, getpass
from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# convert datetime obj to string
str_current_datetime = str(current_datetime)

my_commands = []
IP_ADDRESS = input("Please enter the IP address: ")
USERNAME = input("Please enter your username: ")
PASSWORD = getpass.getpass()

cisco_9500 = {
    'device_type': 'cisco_ios',
    'host':   IP_ADDRESS,
    'username': USERNAME,
    'password': PASSWORD,
}

net_connect = ConnectHandler(**cisco_9500)
standby_output = net_connect.send_command('show standby | e FE80', use_textfsm=True) #excluding FE80 so that textfsm can parse through the output generated by the show standby command without crashing

output_json = json.dumps(standby_output, indent=2) #converts my python dictionary into json format / makes it pretty
#print(output_json) #for testing

def get_hostname():
	output = net_connect.send_command('show ver', use_textfsm=True)
	for item in output:
            hostname = f"{item['hostname']}"
            return hostname

hostname = get_hostname()

file_name = "hsrp_graceful_configs-" + hostname + "-" + str_current_datetime + ".ios"
w = open(file_name, 'a')

def new_hsrp(svi):
	my_interface = "interface " + f"{svi['interface']}" + "\n" #grabs interface
	group = f"{svi['group']}" #grabs group value from svi
	original_priority = f"{svi['priority']}" #grabs priority value
	new_priority = int(original_priority) + 15
	new_priority_command = "standby " + group + " priority " + str(new_priority) + "\n" #builds the command for interface description
	w.writelines(my_interface) #writes out config
	w.writelines(new_priority_command)
	
def old_hsrp(svi):
	my_interface = "interface " + f"{svi['interface']}" + "\n" #grabs interface
	group = f"{svi['group']}" #grabs group value from svi
	original_priority = f"{svi['priority']}" #grabs priority value
	priority_command = "standby " + group + " priority " + str(original_priority) + "\n" #builds the command for interface description
	w.writelines(my_interface) #writes out config
	w.writelines(priority_command)

header = "HSRP Graceful Failover Configs for " + hostname + "\n\n"
header2 = "conf t\n"
header3 = "end\n\n\n"
w.writelines(header)
w.writelines(header2)

for svi in standby_output:
	new_hsrp(svi)

w.writelines(header3)

###

header4 = "HSRP Original Configs for " + hostname + "\n\n"
header5 = "conf t\n"
header6 = "end\n\n\n"
w.writelines(header4)
w.writelines(header5)

for svi in standby_output:
	old_hsrp(svi)

w.writelines(header6)
w.close()
print("finished!")
