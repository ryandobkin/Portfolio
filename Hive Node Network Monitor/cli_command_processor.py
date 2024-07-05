from logger import Logger
from hive_node import HiveNode
from hive_message import HiveMessage
from message_queue import MessageQueue
from connect_message import ConnectMessage
from gossip_protocol_command_manager import GossipProtocolCommandManager
from heartbeat_protocol_command_manager import HeartbeatProtocolCommandManager
from blueprint_protocol_command_manager import BlueprintProtocolCommandManager
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
from hive_node_manager import HiveNodeManager
from typing import Dict, Callable


class CliCommandProcessor:
    """
    CliCommandProcessor processes CLI commands for managing the Hive network.

    Attributes:
    ----------
    logger : Logger
        An instance of the Logger class for logging messages.
    prompt : str
        The CLI prompt string.
    commands_help : Dict[str, str]
        A dictionary mapping command names to their help descriptions.
    commands : Dict[str, Callable]
        A dictionary mapping command names to their corresponding methods.
    hive_node_manager : HiveNodeManager
        Manages the nodes in the Hive network.
    outbound_message_queue : MessageQueue
        A queue for outbound messages.
    inbound_message_queue : MessageQueue
        A queue for inbound messages.
    """

    def __init__(self, hive_node_manager: HiveNodeManager, outbound_message_queue: MessageQueue, inbound_message_queue: MessageQueue):
        """
        Initializes a new instance of CliCommandProcessor.

        Parameters:
        ----------
        hive_node_manager : HiveNodeManager
            Manages the nodes in the Hive network.
        outbound_message_queue : MessageQueue
            A queue for outbound messages.
        inbound_message_queue : MessageQueue
            A queue for inbound messages.
        """
        self.logger: Logger = Logger()

        self.prompt: str = '> '
        self.commands_help: Dict[str, str] = {
            'list_nodes': 'Usage: list_nodes - List all nodes in the network',
            'list_outbound_messages': 'Usage: list_outbound_messages - List all messages in the outbound message queue',
            'list_inbound_messages': 'Usage: list_inbound_messages - List all messages in the inbound message queue',
            'connect': 'Usage: connect <ip_address> <port> - Connect to a new node in the network',
            'enable_gossip_protocol': 'Usage: enable_gossip_protocol - Enable the gossip protocol',
            'disable_gossip_protocol': 'Usage: disable_gossip_protocol - Disable the gossip protocol',
            'enable_heartbeat_protocol': 'Usage: enable_heartbeat_protocol - Enable the heartbeat protocol',
            'disable_heartbeat_protocol': 'Usage: disable_heartbeat_protocol - Disable the heartbeat protocol',
            'enable_blueprint_protocol': 'Usage: enable_blueprint_protocol - Enable the blueprint protocol',
            'disable_blueprint_protocol': 'Usage: disable_blueprint_protocol - Disable the blueprint protocol',
            'list_network_monitor': 'Usage: list_network_monitor - Logs tabular list of node status/config',
            'list_config': 'Usage: list_config - Prints a tabular list of the local nodes config',
            'change_profile_check_id': "Usage: change_profile_check_id <node_friendly_name> <new_check_id> - "
            "Changes profile check ID / changes checks to be run by the specified node's NetworkMonitor",
            'exit': 'Usage: exit - Shut down the node and exit application',
            'quit': 'Usage: quit - Shut down the node and exit application',
            'help': 'Usage: help - List all available commands',
            'edit_config': 'Usage: edit_config <action> <sub-action> <profile> <service> <param1> <param2> <param3> - '
                           'Only action, sub-action, and profile required, depending on usage.'
                           'If specifying service, its recommended to include the required parameters.'
                           'For example, to add a new service to the profile London, specify - '
                           'edit_config add profile London HTTP 4 www.google.com',
        }
        self.commands: Dict[str, Callable] = {
            'list_nodes': self.list_nodes,
            'list_outbound_messages': self.list_outbound_messages,
            'list_inbound_messages': self.list_inbound_messages,
            'connect': self.connect_to_node,
            'enable_gossip_protocol': self.enable_gossip_protocol,
            'disable_gossip_protocol': self.disable_gossip_protocol,
            'enable_heartbeat_protocol': self.enable_heartbeat_protocol,
            'disable_heartbeat_protocol': self.disable_heartbeat_protocol,
            'enable_blueprint_protocol': self.enable_blueprint_protocol,
            'disable_blueprint_protocol': self.disable_blueprint_protocol,
            'list_network_monitor': self.network_monitor_list,
            'list_config': self.list_config,
            'change_profile_check_id': self.change_profile_check_id,
            'edit_config': self.edit_config,
            'exit': self.process_command,
            'quit': self.process_command,
            'help': self.list_commands,
        }
        self.hive_node_manager: HiveNodeManager = hive_node_manager
        self.outbound_message_queue: MessageQueue = outbound_message_queue
        self.inbound_message_queue: MessageQueue = inbound_message_queue

        self.logger.debug("CliCommandProcessor", "CliCommandProcessor initialized...")

    def command_loop(self) -> None:
        """
        Starts the command loop, processing user input commands until 'exit' or 'quit' is received.
        """
        commands: list[str] = list(self.commands_help.keys())
        completer: WordCompleter = WordCompleter(commands, ignore_case=True)
        session: PromptSession = PromptSession(completer=completer)

        while True:
            try:
                with patch_stdout():
                    command: str = session.prompt(self.prompt)
                parts: list[str] = command.split()
                if not parts:
                    continue
                elif parts[0] in ['exit', 'quit']:
                    break
                elif parts[0] in ['help', '?']:
                    self.list_commands()
                elif parts[0] == 'list_nodes':
                    self.list_nodes()
                elif parts[0] == 'list_outbound_messages':
                    self.list_outbound_messages()
                elif parts[0] == 'list_inbound_messages':
                    self.list_inbound_messages()
                elif parts[0] == 'enable_gossip_protocol':
                    self.enable_gossip_protocol()
                elif parts[0] == 'disable_gossip_protocol':
                    self.disable_gossip_protocol()
                elif parts[0] == 'enable_heartbeat_protocol':
                    self.enable_heartbeat_protocol()
                elif parts[0] == 'disable_heartbeat_protocol':
                    self.disable_heartbeat_protocol()
                elif parts[0] == 'enable_blueprint_protocol':
                    self.enable_blueprint_protocol()
                elif parts[0] == 'disable_blueprint_protocol':
                    self.disable_blueprint_protocol()
                elif parts[0] == 'list_network_monitor':
                    self.network_monitor_list()
                elif parts[0] == 'list_config':
                    self.list_config()
                elif parts[0] == 'change_profile_check_id':
                    if len(parts) == 3:
                        self.change_profile_check_id(parts[1], parts[2])
                    else:
                        self.logger.info("CliCommandProcessor", self.commands_help['change_profile_check_id'])
                elif parts[0] == 'edit_config':
                    if len(parts) < 3:
                        self.logger.info("CliCommandProcessor", self.commands_help['edit_config'])
                    elif len(parts) == 4:
                        self.edit_config(parts[1], parts[2], parts[3])
                    elif len(parts) == 5:
                        self.edit_config(parts[1], parts[2], parts[3], parts[4])
                    elif len(parts) == 7:
                        self.edit_config(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
                    elif len(parts) == 8:
                        self.edit_config(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])
                    else:
                        self.logger.info("CliCommandProcessor", self.commands_help['edit_config'])
                elif parts[0] == 'connect':
                    if len(parts) < 3:
                        self.logger.info("CliCommandProcessor", self.commands_help['connect'])
                    else:
                        ip_address: str = parts[1]
                        port: str = parts[2]
                        self.connect_to_node(ip_address, port)
                else:
                    self.logger.info("CliCommandProcessor", f"Unknown command: {command}")

            except (EOFError, KeyboardInterrupt):
                break

    def process_command(self, command: str) -> None:
        """
        Processes a given command by splitting it into its name and arguments, and executing the corresponding method.

        Parameters:
        ----------
        command : str
            The command string to process.
        """
        parts: list[str] = command.split()
        if not parts:
            return
        command_name: str = parts[0]
        command_args: list[str] = parts[1:]
        if command_name in self.commands:
            self.commands[command_name](*command_args)
        else:
            self.logger.info("CliCommandProcessor", f"Unknown command: {command}")

    def list_commands(self) -> None:
        """
        Lists all available commands with their descriptions.
        """
        self.logger.info("CliCommandProcessor", "Available commands:")
        for command, description in self.commands_help.items():
            self.logger.info("CliCommandProcessor", f"{command:<15} - {description}")

    def set_prompt(self, prompt: str) -> None:
        """
        Sets the CLI prompt string.

        Parameters:
        ----------
        prompt : str
            The new prompt string.
        """
        self.prompt = prompt

    def set_node_manager(self, hive_node_manager: HiveNodeManager) -> None:
        """
        Sets the HiveNodeManager instance.

        Parameters:
        ----------
        hive_node_manager : HiveNodeManager
            The HiveNodeManager instance to set.
        """
        self.hive_node_manager = hive_node_manager

    def list_nodes(self) -> None:
        """
        Lists all nodes in the network by calling the HiveNodeManager's list_nodes method.
        """
        self.hive_node_manager.list_nodes()

    def list_outbound_messages(self) -> None:
        """
        Lists all messages in the outbound message queue by calling its list_messages method.
        """
        self.outbound_message_queue.list_messages()

    def list_inbound_messages(self) -> None:
        """
        Lists all messages in the inbound message queue by calling its list_messages method.
        """
        self.inbound_message_queue.list_messages()

    def connect_to_node(self, ip_address: str, port: str) -> None:
        """
        Connects to a new node in the network by creating a ConnectMessage and enqueueing it.

        Parameters:
        ----------
        ip_address : str
            The IP address of the node to connect to.
        port : str
            The port number of the node to connect to.
        """
        remote_node: HiveNode = HiveNode("remote_node", ip_address, int(port))
        connect_message: ConnectMessage = ConnectMessage(
            sender=self.hive_node_manager.local_node,
            recipient=remote_node,
            message='Hello'
        )
        new_hive_message: HiveMessage = HiveMessage(connect_message)
        self.outbound_message_queue.enqueue(new_hive_message)

    def enable_gossip_protocol(self) -> None:
        """
        Enables the gossip protocol by setting the appropriate flag in the GossipProtocolCommandManager.
        """
        GossipProtocolCommandManager.enable = True

    def disable_gossip_protocol(self) -> None:
        """
        Disables the gossip protocol by setting the appropriate flag in the GossipProtocolCommandManager.
        """
        GossipProtocolCommandManager.enable = False

    def enable_heartbeat_protocol(self) -> None:
        """
        Enables the heartbeat protocol by setting the appropriate flag in the HeartbeatProtocolCommandManager.
        """
        HeartbeatProtocolCommandManager.enable = True

    def disable_heartbeat_protocol(self) -> None:
        """
        Disables the heartbeat protocol by setting the appropriate flag in the HeartbeatProtocolCommandManager.
        """
        HeartbeatProtocolCommandManager.enable = False

    def enable_blueprint_protocol(self) -> None:
        """
        Enables the blueprint protocol by setting the appropriate flag in the BlueprintProtocolCommandManager.
        """
        BlueprintProtocolCommandManager.enable = True

    def disable_blueprint_protocol(self) -> None:
        """
        Disables the blueprint protocol by setting the appropriate flag in the BlueprintProtocolCommandManager.
        """
        BlueprintProtocolCommandManager.enable = False

    def edit_config(self, action, sub_action, profile, service=None, p1=None, p2=None, p3=None) -> None:
        """
        When called with parameters, allows the user to edit a node's
        config blueprint.

        Parameters:
        ----------
        action
            user can choose to 'add', 'remove', or 'edit'
        sub_action
            does the user want to add/remove/edit a profile or a service check?
                specified as 'profile', or 'service'
        profile
            name of profile to be added
        service
            for edit profile, acts as new name - otherwise:
            if passed as a string, details the service to be configured
            elif passed as a dictionary, pairs a starting dictionary to the profile.
                { service_check: { params }...}
        p1, p2, p3
            user must pass at least 2 parameters for a service check
                "interval", "address", "port"
        """
        if sub_action == 'profile':
            if action == 'add':
                if service is None:
                    self.hive_node_manager.create_service_profile(profile)
                elif service[0] != '{':
                    self.hive_node_manager.create_service_profile(profile, {service: {"interval": p1, "address": p2, "port": p3}})
                elif service[0] == '{':
                    self.hive_node_manager.create_service_profile(profile, service)
                else:
                    pass
            elif action == 'remove':
                self.hive_node_manager.remove_service_profile(profile)
            elif action == 'edit':
                self.hive_node_manager.edit_profile_name(profile, service)
            else:
                pass
        elif sub_action == 'service':
            if action == 'add' or action == 'edit':
                self.hive_node_manager.add_or_replace_service_check(profile, service, p1, p2, p3)
            elif action == 'remove':
                self.hive_node_manager.remove_service_check(profile, service)
            else:
                pass
        else:
            pass

    def network_monitor_list(self):
        """
        When called, dumps the current config+status list of NetworkMonitor as tabular list
        """
        self.hive_node_manager.print_tabular_network_monitor()

    def change_profile_check_id(self, node, new_profile_name):
        """
        When called, updates the profile name (check_id) of the node referenced

        Parameters:
        ----------
        node : str
            The node referenced
        new_profile_name : int
            The id to set the node's profile to
        """
        self.hive_node_manager.update_node_check_id(node, new_profile_name)

    def list_config(self):
        """
        When called, runs hive_node_manager.print_tabular_config_list()
        """
        self.hive_node_manager.print_tabular_config_list()
