# Socket Programming Project 3 - Transient Services
### Ryan Dobkin - CS 372
Hive Node + Network Monitor Application
This network monitor service uses a dictionary configuration sent in the form of config profile: config.\
Each node is assigned an ID, and runs network checks based on their assignment.\
Each node can have its identity and configuration changed through console commands,
as documented by typing 'help'.

Each network node will start with a base blueprint of:
<pre>
{'0': 
 {'ICMP': {'interval': 15, 'address': '192.168.41.27', 'port': None},
 'HTTP': {'interval': 20, 'address': 'www.google.com', 'port': None}, 
 'HTTPS': {'interval': 22, 'address': 'www.google.com', 'port': None},
 'DNS': {'interval': 25, 'address': 'www.google.com', 'port': '8.8.8.8'},
 'NTP': {'interval': 30, 'address': '128.138.140.211', 'port': None},
 'TCP': {'interval': 28, 'address': '1.1.1.1', 'port': 50},
 'UDP': {'interval': 24, 'address': '8.8.4.4', 'port': 50}}}
</pre>
Note that this can be overwritten or edited using the edit_config command.
When editing the config, be sure to follow one of the following structures:
<pre>
edit_config [action] [sub-action] [profile] [service] [parameter 1=interval] [parameter 2=address] [parameter 3=port]
edit_config remove profile 1
edit_config add service 0 DNS 12 www.oregonstate.edu 8.8.4.4
edit_config remove service 0 TCP
edit_config edit service 0 DNS 20 www.cloudflare.com 1.1.1.1
</pre>
The default can also be changed or removed via the DEFAULT CONFIG section in the __init__ section of hive_node_manager.py\
Numbers are not required to be used as check IDs, however they are set as such in the default.

Note that, due to test requirements, address and port fields are not exclusive.

Refer to the following list when adding, editing, or replacing the config services:
<pre>
'ICMP'  - parameters: [interval] [address]
'HTTP'  - parameters: [interval] [URL]
'HTTPS' - parameters: [interval] [URL]
'DNS'   - parameters: [interval] [URL] [DNS server address]
'NTP'   - parameters: [interval] [NTP server address]
'TCP'   - parameters: [interval] [address] [port]
'UDP'   - parameters: [interval] [address] [port]
</pre>

To start the program, enter a variation of the following startup command:
<pre>
python [directory] -ip [ip address] -port [server port] -friendly_name [profile name] -check_id [check ID]
python .\app_main.py -ip 127.0.0.1 -port 54321 -friendly_name Oregon 0
</pre>

Below is a list of all added custom commands. They are also available by typing 'help' in the console.
<pre>
enable_blueprint_protocol - Enables the BlueprintProtocolCommandManager
disable_blueprint_protocol - Disables the BlueprintProtocolCommandManager
list_network_monitor - Prints a tabular list of results pertaining to the NetworkMonitor, with the following headers:
    SERVICE | INTERVAL | PARAM 2 | PARAM 3 | LAST CHECKED | STATUS
list_config - Prints a tabular list of the config dictionary held by the local node, with the following headers:
    CHECK ID | SERVICE | INTERVAL | PARAM 2 | PARAM 3
change_profile_check_id [node_profile_name] [new_check_id] - Changes the specified node's check ID
edit_config - refer to the edit_config section
</pre>

The following requirements can also be found in requirements.txt:\
dnspython==2.6.1\
ntplib==0.4.0\
prompt_toolkit==3.0.43\
Requests==2.32.3
