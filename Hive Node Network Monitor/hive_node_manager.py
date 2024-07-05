import time
from typing import List, Optional
from logger import Logger
from hive_node import HiveNode
from app_settings import AppSettings


class HiveNodeManager:
    """
    HiveNodeManager is responsible for managing the list of nodes in the network.
    It provides methods to add, remove, and list nodes, as well as to get random live nodes.

    In addition, it also is responsible for managing the blueprint list (config) for the local node.
    It provides methods to add/update and remove profiles,
        as well as add/update and remove specific service checks per profile.

    Attributes:
    ----------
    logger : Logger
        An instance of the Logger class for logging messages.
    hive_nodes : List[HiveNode]
        The list of nodes in the network.
    local_node : HiveNode
        The local node instance managed by this manager.
    hive_blueprint : Dict
        The config dictionary for the network
    """

    def __init__(self, local_node: HiveNode):
        """
        Initializes a new instance of HiveNodeManager.

        Parameters:
        ----------
        local_node : HiveNode
            The local node instance managed by this manager.
        """
        self.logger: Logger = Logger()
        self.hive_nodes: List[HiveNode] = []
        self.local_node: HiveNode = local_node
        self.add_node(local_node)
        self.blueprint_dict = {}
        self.last_update = None
        self.print_tabular = False
        self.incoming_update_check_id = {}
        self.outgoing_update_check_id = {}

        self.logger.info("HiveNodeManager", "HiveNodeManager initialized...")

        # --------------------------------- DEFAULT CONFIG --------------------------------- #
        self.create_service_profile("0")
        self.add_or_replace_service_check("0", "ICMP", 15, '192.168.41.27')
        self.add_or_replace_service_check("0", "HTTP", 20, 'www.google.com')
        self.add_or_replace_service_check("0", "HTTPS", 22, 'www.google.com')
        self.add_or_replace_service_check("0", "DNS", 25, 'www.google.com', '8.8.8.8')
        self.add_or_replace_service_check("0", "NTP", 30, '128.138.140.211')
        self.add_or_replace_service_check("0", "TCP", 28, '1.1.1.1', 50)
        self.add_or_replace_service_check("0", "UDP", 24, '8.8.4.4', 50)
        # --------------------------------- DEFAULT CONFIG --------------------------------- #

    def update_node_check_id(self, node, profile):
        """
        When called, sets self.update_node to a list of {node.friendly_name: profile}
        If local node, append dict to incoming. If foreign, append to outgoing.

        Parameters:
        ----------
        node : str
            The node to update
        profile : str
            The new profile (check ID) name
        """
        for node_in in self.hive_nodes:
            if node_in.friendly_name == node:
                if node_in == self.local_node:
                    self.incoming_update_check_id.update({self.local_node.friendly_name: profile})
                    self.logger.info("HiveNodeManager", "UpdateNodeCheckID - Locally Updated")
                    return None
                self.outgoing_update_check_id.update({node_in.friendly_name: profile})
                self.logger.info("HiveNodeManager", "UpdateNodeCheckID - Update ready to propagate")
                return None
        # print(f"{self.local_node.friendly_name} || {profile}")
        self.logger.info("HiveNodeManager", "UpdateNodeCheckID - Specified Node not recorded")

    def print_tabular_network_monitor(self):
        """
        Flips the self.print_tabular flag to let network_monitor know to dump
        """
        self.print_tabular = True

    def print_tabular_config_list(self):
        """
        When called, prints a tabular list of the configuration list for this node.
        """
        self.logger.info("HiveNodeManager", "-------------------------------------------------------------------------")
        self.logger.info("HiveNodeManager", "CHECK ID | SERVICE | INTERVAL | PARAM 2         | PARAM 3")
        for profile in self.blueprint_dict:
            for service_check in self.blueprint_dict[profile]:
                service = self.blueprint_dict[profile][service_check]
                sp1 = (len("CHECK ID") - len(str(profile))) * " "
                sp2 = (len("SERVICE") - len(service_check)) * " "
                sp3 = (len("INTERVAL") - len(str(service['interval']))) * " "
                sp4 = (len("PARAM 2        ") - len(str(service['address']))) * " "
                sp5 = (len("PARAM 3") - len(str(service['port']))) * " "
                self.logger.info("HiveNodeManager",
                 f"{profile}{sp1} | {service_check}{sp2} | {service['interval']}{sp3} | {service['address']}{sp4} | {service['port']}{sp5}")
        self.logger.info("HiveNodeManager", "-------------------------------------------------------------------------")

    def update_profile(self, new_profile_name):
        """
        Updates the hive_node friendly name, inadvertently changing the checks performed locally

        Parameters:
        ----------
        new_profile_name: str
            Name to set the profile/friendly_name to
        """
        self.local_node.friendly_name = new_profile_name

    def add_or_replace_service_check(self, profile, service_type, p1, p2, p3=None):
        """
        Adds or updates (overwrites) a dict {service: {parameters}} to the service_list dictionary

        parameters:
        ----------
        profile
            The specified service profile
        service_type
            The service_type
        param_list
            The three value long list of parameters - (interval, address, port)
            If any param not in use, set to None
        """
        dict_param_list = {"interval": p1, "address": p2, "port": p3}
        self.blueprint_dict[profile].update({service_type: dict_param_list})
        self.update_last_update()

    def remove_service_check(self, profile, service_type):
        """
        Removes a service dict based on the service name

        parameters:
        ----------
        profile
            The specified service profile
        service_type
            The service_type
        """
        self.blueprint_dict[profile].pop(service_type)
        self.update_last_update()

    def create_service_profile(self, profile, service_dict_setup=None):
        """
        Creates a new service profile in blueprint_dict

        Parameters:
        ----------
        profile
            name of the service profile
        service_dict_setup
            A dictionary containing the initial parameters for the NodeBlueprint object
            should be passed as:
                {service_type: {"interval": param, "address": param, "port": param}, {...}, ...}
        """
        if service_dict_setup is None:
            self.add_or_replace_service_profile(profile, {})
        else:
            self.add_or_replace_service_profile(profile, service_dict_setup)
        self.update_last_update()

    def add_or_replace_service_profile(self, profile: str, service_dict) -> None:
        """
        Adds a service profile to the blueprint_dict

        Parameters:
        ----------
        profile
            name of the service profile
        service_dict
            service_profile_dict for profile pair
        """
        self.blueprint_dict.update({profile: service_dict})
        self.update_last_update()

    def remove_service_profile(self, profile) -> None:
        """
        Removes a service profile from the blueprint_dict

        Parameters:
        ----------
        profile
            name of the service profile
        """
        self.blueprint_dict.pop(profile)
        self.update_last_update()

    def remove_service_dict_check(self, profile, service):
        """
        Removes a service from a profile's service_dict

        Parameters:
        ----------
        profile
            name of service profile
        service
            name of service to be removed
        """
        self.blueprint_dict[profile].pop(service)
        self.update_last_update()

    def edit_profile_name(self, profile, new_name):
        """
        Renames profiles

        Parameters:
        ----------
        profile
            name of service profile
        new_name
            new name of service profile
        """
        dict_value = self.blueprint_dict[profile]
        new_dict = {new_name: dict_value}
        self.blueprint_dict[profile].pop()
        self.blueprint_dict.update(new_dict)
        self.update_last_update()

    def update_last_update(self):
        """
        Updates the HiveNodeManager last_update timer, that removes race conditions for
        blueprint updates
        """
        self.last_update = time.time()


# ------------------------------------------------------------------------------------
#   ||  v HIVE NODE LIST MANAGER v  ||  ^ HIVE BLUEPRINT LIST MANAGER ^  ||
# ------------------------------------------------------------------------------------

    def add_node(self, new_node: HiveNode) -> None:
        """
        Adds a new node to the list of nodes. If the node already exists, it updates the node's friendly name.

        Parameters:
        ----------
        new_node : HiveNode
            The node to be added to the list.
        """
        existing_node: Optional[HiveNode] = self.get_node_by_ip_address_and_port(new_node.ip_address, new_node.port_number)

        if existing_node:
            self.logger.info("HiveNodeManager", f"Node {new_node.friendly_name} already exists in the node list...")
            self.logger.debug("HiveNodeManager", f"Updating node {existing_node.ip_address}:{existing_node.port_number} from {existing_node.friendly_name} to {new_node.friendly_name}...")
            existing_node.friendly_name = new_node.friendly_name
        else:
            self.logger.info("HiveNodeManager", f"Node {new_node.friendly_name} does not exist in the node list...")
            self.hive_nodes.append(new_node)

    def remove_node(self, node_to_remove: HiveNode) -> None:
        """
        Removes a node from the list of nodes.

        Parameters:
        ----------
        node_to_remove : HiveNode
            The node to be removed from the list.
        """
        self.hive_nodes = [node for node in self.hive_nodes if not (node.ip_address == node_to_remove.ip_address and node.port_number == node_to_remove.port_number)]

    def list_nodes(self) -> None:
        """
        Logs the list of nodes in the network, including their details.
        """
        col_widths = {
            'friendly_name': max(len(HiveNode.headers['friendly_name']), max(len(node.friendly_name) for node in self.hive_nodes)) + 1, # +1 for * indicating local node
            'ip_address': max(len(HiveNode.headers['ip_address']), max(len(node.ip_address) for node in self.hive_nodes)),
            'port': max(len(HiveNode.headers['port']), max(len(str(node.port_number)) for node in self.hive_nodes)),
            'status': max(len(HiveNode.headers['status']), max(len(node.status) for node in self.hive_nodes)),
            'last_heartbeat': max(len(HiveNode.headers['last_heartbeat']), max(len(str(node.last_heartbeat_timestamp)) for node in self.hive_nodes)),
            'Failed Connections': max(len('Failed Connections'), max(len(str(node.failed_connection_count)) for node in self.hive_nodes)),
        }

        self.logger.info("HiveNodeManager", "-" * AppSettings.LOG_LINE_WIDTH)
        self.logger.info("HiveNodeManager", self.local_node.get_node_list_row_header_as_str(col_widths))
        self.logger.info("HiveNodeManager", self.local_node.get_node_list_row_separator_as_str(col_widths))

        for node in self.hive_nodes:
            self.logger.info("HiveNodeManager", node.get_node_list_row_as_str(col_widths))
        self.logger.info("HiveNodeManager", "-" * AppSettings.LOG_LINE_WIDTH)

    def get_next_live_node(self, node_list: list) -> list:
        """
        Returns the 'next' live node from the list of nodes, excluding the local node.
        Will pick a node in the list not in the passed array. If all nodes in array, clears array, appends first node.

        Parameters:
        ----------
        deprecated_node_list : list
            the list of already picked nodes sent.

        Returns:
        -------
        updated node list
            the passed node_list array, updated to have the final element be the node to be used
            if passed list and hive_nodes list are equal, clear array and append first element of hive_nodes list
        """
        if len(self.hive_nodes) < 2:
            return node_list
        else:
            # looks for valid node
            for live_node in self.hive_nodes:
                if live_node not in node_list and live_node.status == "Live" and live_node != self.local_node:
                    node_list.append(live_node)
                    return node_list
            # If lists have all same elements - look for first valid node
            for live_node in self.hive_nodes:
                if live_node.status == "Live" and live_node != self.local_node:
                    # the 0 is a sentinel type addition at index [0] that lets me search how I am
                    return [0, live_node]

    def get_node_by_ip_address_and_port(self, source_ip_address: str, source_port: int) -> Optional[HiveNode]:
        """
        Returns the node with the specified IP address and port, or None if no such node exists.

        Parameters:
        ----------
        source_ip_address : str
            The IP address of the node to be retrieved.
        source_port : int
            The port number of the node to be retrieved.

        Returns:
        -------
        Optional[HiveNode]
            The node with the specified IP address and port, or None if no such node exists.
        """
        source_node: HiveNode = HiveNode("temp", source_ip_address, source_port)

        for node in self.hive_nodes:
            if node == source_node:
                return node
        return None

    def get_all_live_nodes(self) -> List[HiveNode]:
        """
        Returns a list of all live nodes in the network.

        Returns:
        -------
        List[HiveNode]
            A list of all live nodes.
        """
        return [node for node in self.hive_nodes if node.status == "Live"]
