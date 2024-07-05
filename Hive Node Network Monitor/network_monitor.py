# Ryan Dobkin
# CS 372
# Last Modified - 6/2/24
# Socket Programming Project 3 - Transient Services

import time
import datetime
import socket
import network_monitoring_examples as nme
import select
import threading
import json
from logger import Logger


DEFAULT_IP, DEFAULT_PORT = '127.0.0.1', 50


class NetworkMonitor:

    def __init__(self, hive_node_manager, profile):
        """
        Init method

        Parameters:
        ----------
        hive_node_manager
            Local Hive Node object
        """
        self.hive_node_manager = hive_node_manager
        self.profile = str(profile)
        self.config = self.hive_node_manager.blueprint_dict
        self.recent_update = {}
        self.logger = Logger()

    def tcp_server(self, ip=DEFAULT_IP, port=DEFAULT_PORT) -> None:
        """
        Establishes TCP server at params: ip; port.
        Temporarily Deprecated
        """
        # Config/timer stuff
        current_config = None
        current_server = None
        #start_time = time.time()
        interval = 0
        # Opens a tcp socket
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind tcp socket to ip and port
        server_sock.bind((ip, port))
        server_sock.setblocking(False)
        # listen for incoming connections
        server_sock.listen(5)
        # Create a 'socket list' for non blocking socket checker
        socket_list = [server_sock]
        print(f"[Server] TCP Server listening on port {port} at {ip}...")

        try:
            while True:
                read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
                for notified_socket in read_sockets:
                    try:
                        if notified_socket == server_sock:
                            # Accept a new connection
                            client_socket, client_address = server_sock.accept()
                            print(f"[Server] Accepted connection from {client_address}")
                            socket_list.append(client_socket)
                            start_time = time.time()
                        else:
                            end_time = time.time()
                            if end_time - start_time >= interval and interval != 0:
                                # make json, send file
                                print("\n[Server] Running specified tests...")
                                self.update(current_config,  notified_socket, current_server)
                                start_time = time.time()

                            # Receive data from client
                            message = notified_socket.recv(1024)

                            if message:
                                # If socket has data
                                print(f"[Server] Received message from {notified_socket.getpeername()}")
                                if message == "KEEPALIVE":
                                    continue
                                elif message.decode()[0] == '{':
                                    # Takes sent config JSON and sets interval, stores config json for update()
                                    # Starts module interval timer
                                    print("[Server] Received Config JSON")
                                    data = message.decode('utf-8')
                                    parsed_data = json.loads(data)
                                    current_server = self.check_server(parsed_data, 1)
                                    specific_config_data = parsed_data[current_server]
                                    interval = specific_config_data["interval"]
                                    current_config = specific_config_data
                                    start_time = time.time()
                            else:
                                # if socket has no data
                                print(f"[Server] Closing socket {notified_socket.getpeername()}")
                                print(f"[Server] Awaiting new connection")
                                socket_list.remove(notified_socket)
                                notified_socket.close()

                        for notified_socket in exception_sockets:
                            socket_list.remove(notified_socket)
                            notified_socket.close()

                    except ConnectionResetError:
                        #print(f"[Server] Lost connection to {notified_socket.getpeername()}. Waiting for Reconnection...")
                        print(f"[Server] Closing socket {notified_socket.getpeername()}")
                        print(f"[Server] Awaiting new connection")
                        socket_list.remove(notified_socket)
                        notified_socket.close()
                        continue
        except KeyboardInterrupt:
            print("Program Stopped")
        finally:
            server_sock.close()

    def check_server(self, data, flag):
        """
        Temporarily Deprecated
        """
        # Checks the JSON to see what config dict the server should read
        current_element = 0
        for _ in data:
            current_element += 1
            if data[_]["server_address"] == DEFAULT_IP and data[_]["server_port"] == DEFAULT_PORT:
                if flag == 1:
                    return f"{_}"
                return current_element

    def update(self, config, socket, current_server):
        """
        Temporarily Deprecated
        """
        # Takes specified config data, socket, and current_server number
        # Gets relevant data from config, runs tests, then sends data to make_json()
        function_list = {"icmp": self.icmp, "http": self.http, "https": self.https,
                         "dns": self.dns, "ntp": self.ntp, "tcp": self.tcp, "udp": self.udp}
        item_dict = {}
        url = config["url"]
        checklist = config["checklist"]
        udp_port = config["udp_port"]
        tcp_port = config["tcp_port"]
        ntp_server = config["ntp_address"]
        dns_server = config["dns"]
        url_and_dns = url, dns_server
        addr = self.dns(url_and_dns)[1]
        addr = addr[0]
        # print(f"[Server] Update - URL: {url}, Addr: {addr}")
        # Takes 7th char of 'Server_n' string, then adds to data json for client to identify server
        item_dict.update({"server": int(current_server[7])-1})
        # gets list of elements needing to be checked, gets return data in form of arrays, then puts data into item_list[]
        for item in checklist:
            function = function_list[item]
            # For item array [X, X, X] - [STATUS | RESULT | TIME]
            if item == 'icmp':
                param = addr
            elif item == 'udp':
                param = addr, udp_port
            elif item == 'tcp':
                param = url, tcp_port
            elif item == 'ntp':
                param = ntp_server
            elif item == 'dns':
                param = url_and_dns
            else:
                param = url
            result = function(param)
            final_result = {"status": result[0], "result": result[1], "time": result[2]}
            item_dict.update({item: final_result})
        self.make_json(item_dict, socket, current_server)

    def make_json(self, item_list, socket, current_server):
        """
        Temporarily Deprecated
        """
        # From data passed by update(), creates and sends json to via socket
        with open(f"data{int(current_server[7])-1}.json", "w") as outfile:
            json.dump(item_list, outfile)
        f = open(f'data{int(current_server[7])-1}.json', 'rb')
        file = f.read(1024)
        while file:
            socket.send(file)
            file = f.read(1024)
        print("[Server] Sent results JSON to client")
        # print(item_list)

    def run(self):
        """
        Starts threads for all check managers
        """
        self.logger.info("NetworkMonitor", "Starting Network Monitor Service...")
        # ICMP Manager
        icmp_service_thread = threading.Thread(target=self.icmp_manager, daemon=True)
        icmp_service_thread.start()
        # HTTP Manager
        http_service_thread = threading.Thread(target=self.http_manager, daemon=True)
        http_service_thread.start()
        # HTTPS Manager
        https_service_thread = threading.Thread(target=self.https_manager, daemon=True)
        https_service_thread.start()
        # DNS Manager
        dns_service_thread = threading.Thread(target=self.dns_manager, daemon=True)
        dns_service_thread.start()
        # NTP Manager
        ntp_service_thread = threading.Thread(target=self.ntp_manager, daemon=True)
        ntp_service_thread.start()
        # TCP Manager
        tcp_service_thread = threading.Thread(target=self.tcp_manager, daemon=True)
        tcp_service_thread.start()
        # UDP Manager
        udp_service_thread = threading.Thread(target=self.udp_manager, daemon=True)
        udp_service_thread.start()
        # Handles all other services
        updater_thread = threading.Thread(target=self.updater, daemon=True)
        updater_thread.start()

    def updater(self):
        """
        Handles dump_tabular_list, dump_config, and update_profile
        """
        while True:
            if self.hive_node_manager.print_tabular is True:
                self.hive_node_manager.print_tabular = False
                self.dump_tabular_list()
            if self.hive_node_manager.incoming_update_check_id:
                check_id = self.hive_node_manager.incoming_update_check_id[self.hive_node_manager.local_node.friendly_name]
                self.hive_node_manager.incoming_update_check_id.pop(self.hive_node_manager.local_node.friendly_name)
                self.update_profile(check_id)
            time.sleep(1)

    def update_profile(self, profile):
        """
        When called, updates the local node's profile to be checked in the config dict

        Parameters:
        profile : int
            the name, or number, of the profile
        """
        self.profile = str(profile)

    def dump_tabular_list(self):
        """
        When called, prints/logs a tabular list of config info,
        as well as current service status and last check time.
        For example:
        | Service | Interval | Parameters | Timestamp | Up/Down |
        | HTTP    | 4        | URL, DNS   | 20:32:11  | UP      |
        """
        profile = self.get_profile_config()
        if profile is None:
            self.logger.info("NetworkMonitor", f"This profile ({profile}) has no config information")
        else:
            self.logger.info("NetworkMonitor", "----------------------------------------------------------------------")
            self.logger.info("NetworkMonitor", " SERVICE | INTERVAL | PARAM 2         | PARAM 3      | LAST CHECKED | STATUS")
            for service in self.recent_update:
                profile_services = self.get_config(service)
                if profile_services is not None:
                    param1, param2, param3 = profile_services["interval"], profile_services["address"], profile_services["port"]
                else:
                    param1, param2, param3 = "NA", "NA", "NA"
                if self.recent_update[service][0] is True:
                    status = "Up"
                else:
                    status = "Down"
                time = self.recent_update[service][1]
                sp1 = (len("SERVICE") - len(service)) * " "
                sp2 = (len("INTERVAL") - (len(str(param1)))) * " "
                sp3 = (15 - len(str(param2))) * " "
                sp4 = (12 - len(str(param3))) * " "
                sp5 = (12 - len(str(time))) * " "
                self.logger.info("NetworkMonitor",
                 f" {service}{sp1} | {param1}{sp2} | {param2}{sp3} | {param3}{sp4} | {time}{sp5} | {status}")
            self.logger.info("NetworkMonitor", "----------------------------------------------------------------------")

    def get_profile_config(self):
        """
        When called, returns config for profile is possible.
        If not possible, returns False
        """
        for profiles in self.config:
            if profiles == self.profile:
                return self.config[self.profile]
        #print(f"{self.profile}\n {self.config}\n\n")
        return None

    # ----------------------------------------------------------------------------------------------------

    def get_config(self, protocol):
        """
        Based on the passed protocol, returns the dict of services of the local profile

        Parameters:
        ----------
        protocol
            The protocol to be checked
        """
        config = self.get_profile_config()
        if config is not None:
            for service in config:
                if service == protocol:
                    return config[protocol]
        return None

    def icmp_manager(self):
        """
        Manages the icmp test method
        Takes the config for icmp and calls based on interval parameter
        """
        while True:
            if self.get_config("ICMP") is not None:
                params = self.get_config("ICMP")
                interval = params["interval"]
                address = params["address"]
                result = self.icmp(address)
                self.recent_update.update({"ICMP": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def icmp(self, address):
        """
        Takes two parameters; service_name - host name; service_addr - host ip address.
        Calls 'nme.ping()' with passed parameters and prints protocol, timestamp, host, ip, and round trip time in ms.
        """
        protocol = "ICMP"
        prefix_pass, prefix_fail = f" {protocol}  | PASS | TIME: ", f" {protocol}  | FAIL | TIME: "
        ping_addr, ping_time = nme.ping(address)
        start_check_time = self.get_time()
        if ping_addr and ping_time is not None:
            self.logger.info("NetworkMonitor", f"{prefix_pass}{start_check_time} | Latency to {address} - {ping_time} ms")
            return [True, start_check_time]
        else:
            self.logger.info("NetworkMonitor", f"{prefix_fail}{start_check_time} | Request timed out of no response received")
            return [False, start_check_time]

    def http_manager(self):
        """
        Manages the http test method
        Takes the config for http and calls based on interval parameter
        """
        while True:
            if self.get_config("HTTP") is not None:
                params = self.get_config("HTTP")
                interval = params["interval"]
                url = params["address"]
                result = self.http(url)
                self.recent_update.update({"HTTP": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def http(self, url):
        """
        Takes one parameter; service_name - host name.
        Calls 'nme.check_server_http()' with the passed parameter and prints protocol, timestamp, host, URL, and status code.
        """
        protocol = "HTTP"
        prefix_pass, prefix_fail = f" {protocol}  | PASS | TIME: ", f" {protocol}  | FAIL | TIME: "
        http_url = "http://" + url
        http_server_status, http_server_response_code = nme.check_server_http(http_url)
        start_check_time = self.get_time()
        if http_server_status is False:
            self.logger.info("NetworkMonitor",
             f"{prefix_fail}{start_check_time} | Request timed out or no reply received")
            return [False, start_check_time]
        else:
            self.logger.info("NetworkMonitor",
             f"{prefix_pass}{start_check_time} | Received status code: "
             f"{http_server_response_code if http_server_response_code is not None else f'N/A'}")
            return [True, start_check_time]

    def https_manager(self):
        """
        Manages the https test method
        Takes the config for https and calls based on interval parameter
        """
        while True:
            if self.get_config("HTTPS") is not None:
                params = self.get_config("HTTPS")
                interval = params["interval"]
                url = params["address"]
                result = self.https(url)
                self.recent_update.update({"HTTPS": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def https(self, service_name):
        """
        Takes one parameter; service_name - host name.
        Calls
        """
        protocol = "HTTPS"
        prefix_pass, prefix_fail = f" {protocol} | PASS | TIME: ", f" {protocol} | FAIL | TIME: "
        https_url = "https://" + service_name
        https_server_status, https_server_response_code, description = nme.check_server_https(https_url)
        start_check_time = self.get_time()
        if https_server_status is False:
            self.logger.info("NetworkMonitor",
             f"{prefix_fail}{start_check_time} | Status: {https_server_status} | Response Code: "
             f"{https_server_response_code if https_server_response_code is not None else 'N/A'}"
             f" | Description: {description}")
            return [False, start_check_time]
        else:
            self.logger.info("NetworkMonitor",
             f"{prefix_pass}{start_check_time} | Status: {https_server_status} | Response Code: "
             f"{https_server_response_code if https_server_response_code is not None else 'N/A'}"
             f" | Description: {description}")
            return [True, start_check_time]

    def dns_manager(self):
        """
        Manages the dns test method
        Takes the config for dns and calls based on interval parameter
        """
        while True:
            if self.get_config("DNS") is not None:
                params = self.get_config("DNS")
                interval = params["interval"]
                url = params["address"]
                dns = params["port"]
                result = self.dns(url, dns)
                self.recent_update.update({"DNS": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def dns(self, url, dns):
        """
        Takes two parameters; service_name - host name; service_addr - host address.
        Generates an array of tuples based off the dns_queries list of DNS types.
        Calls 'nme.check_dns_server_status()' using passed and generated parameters and prints:
        protocol, timestamp, ip address, dns record type, and the dns results or 'answer'.
        """
        protocol = "DNS"
        prefix_pass, prefix_fail = f" {protocol}   | PASS | TIME: ", f" {protocol}   | FAIL | TIME: "
        url_addr, dns_server = url, dns
        service_addr, dns_query, dns_record_type = dns_server, url, 'A'
        dns_server_status, dns_query_results = nme.check_dns_server_status(service_addr, dns_query, dns_record_type)
        start_check_time = self.get_time()
        if dns_server_status is False:
            self.logger.info("NetworkMonitor",
             f"{prefix_fail}{start_check_time} | DNS: {service_addr} | Type: {dns_record_type} | Results: {dns_query_results}")
            return [False, start_check_time]
        else:
            self.logger.info("NetworkMonitor",
             f"{prefix_pass}{start_check_time} | DNS: {service_addr} | Type: {dns_record_type} | Results: {dns_query_results}")
            return [True, start_check_time]

    def ntp_manager(self):
        """
        Manages the ntp test method
        Takes the config for ntp and calls based on interval parameter
        """
        while True:
            if self.get_config("NTP") is not None:
                params = self.get_config("NTP")
                interval = params["interval"]
                address = params["address"]
                result = self.ntp(address)
                self.recent_update.update({"NTP": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def ntp(self, ntp_server):
        """
        Takes one parameter; ntp_server - ntp server address.
        Calls 'nme.check_ntp_server()' and prints out the protocol, timestamp, ntp server address (as well as status), and server time.
        """
        protocol = "NTP"
        prefix_pass, prefix_fail = f" {protocol}   | PASS | TIME: ", f" {protocol}   | FAIL | TIME: "
        ntp_server_status, ntp_server_time = nme.check_ntp_server(ntp_server)
        start_check_time = self.get_time()
        if ntp_server_status:
            self.logger.info("NetworkMonitor", f"{prefix_pass}{start_check_time} | Time: {ntp_server_time}")
            return [True, start_check_time]
        else:
            self.logger.info("NetworkMonitor", f"{prefix_fail}{start_check_time} | Time: NA")
            return [False, start_check_time]

    def tcp_manager(self):
        """
        Manages the tcp test method
        Takes the config for tcp and calls based on interval parameter
        """
        while True:
            if self.get_config("TCP") is not None:
                params = self.get_config("TCP")
                interval = params["interval"]
                address = params["address"]
                port = params["port"]
                result = self.tcp(address, port)
                self.recent_update.update({"TCP": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def tcp(self, address_in, port_in):
        """
        Takes two parameter; server address, and server port
        Calls 'nme.check_tcp_port()' and prints protocol, timestamp, server name, server tcp port, and port description.
        """
        protocol = "TCP"
        prefix_pass, prefix_fail = f" {protocol}   | PASS | TIME: ", f" {protocol}   | FAIL | TIME: "
        address, port = address_in, port_in
        tcp_port_status, tcp_port_description = nme.check_tcp_port(address, port)
        start_check_time = self.get_time()
        if tcp_port_status is False:
            self.logger.info("NetworkMonitor",
             f"{prefix_fail}{start_check_time} | Description: {tcp_port_description} | Status: {tcp_port_status}")
            return [False, start_check_time]
        else:
            self.logger.info("NetworkMonitor",
             f"{prefix_pass}{start_check_time} | Description: {tcp_port_description} | Status: {tcp_port_status}")
            return [False, start_check_time]

    def udp_manager(self):
        """
        Manages the udp test method
        Takes the config for udp and calls based on interval parameter
        """
        while True:
            if self.get_config("UDP") is not None:
                params = self.get_config("UDP")
                interval = params["interval"]
                address = params["address"]
                port = params["port"]
                result = self.udp(address, port)
                self.recent_update.update({"UDP": result})
                time.sleep(int(interval))
            else:
                time.sleep(1)

    def udp(self, address_in, port_in):
        """
        Takes one parameter; service_addr - host address.
        Calls 'nme.check_udp_port()', prints out protocol, timestamp, server ip, server udp port, and port description.
        """
        protocol = "UDP"
        prefix_pass, prefix_fail = f" {protocol}   | PASS | TIME: ", f" {protocol}   | FAIL | TIME: "
        address, port = address_in, port_in
        udp_port_status, udp_port_description = nme.check_udp_port(address, port)
        start_check_time = self.get_time()
        if udp_port_status is False:
            self.logger.info("NetworkMonitor",
             f"{prefix_fail}{start_check_time} | Description: {udp_port_description} | Status: {udp_port_status}")
            return [False, start_check_time]
        else:
            self.logger.info("NetworkMonitor",
                             f"{prefix_pass}{start_check_time} | Description: {udp_port_description} | Status: {udp_port_status}")
            return [True, start_check_time]

    def get_time(self):
        """
        Returns time in form of hour:minute:second:microsecond when called.
        """
        time_test = datetime.datetime.now()
        # microsecond = time_test.microsecond / 10000
        # microsecond = '%.0f' % microsecond
        # .{microsecond}
        return f"{time_test.hour}:{time_test.minute}:{time_test.second}"

    def enable_network_monitor(self):
        """
        When called, enables the network monitor
        """
        self.logger.debug("NetworkMonitor", "Enabling Network Monitor...")
        NetworkMonitor.enable = True

    def disable_network_monitor(self):
        """
        When called, disables network monitor
        """
        self.logger.debug("NetworkMonitor", "Disabling Network Monitor...")
        NetworkMonitor.enable = False

