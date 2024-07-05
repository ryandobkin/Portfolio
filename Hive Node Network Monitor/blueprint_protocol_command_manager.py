import time
from logger import Logger
from hive_message import HiveMessage
from message_queue import MessageQueue
from app_settings import AppSettings
from blueprint_message import BlueprintMessage
from hive_node_manager import HiveNodeManager
from typing import Dict


class BlueprintProtocolCommandManager:
    """
    BlueprintProtocolCommandManager manages the blueprint protocol for the network.

    Attributes:
    ----------
    enable : bool
        A class-level flag to enable or disable the gossip protocol.
    logger : Logger
        An instance of the Logger class for logging messages.
    hive_node_manager : HiveNodeManager
        Manages the config blueprint.
    outbound_message_queue : MessageQueue
        A queue for outbound messages.
    """

    enable: bool = True

    def __init__(self, hive_node_manager: HiveNodeManager, outbound_message_queue: MessageQueue):
        """
        Initializes a new instance of BlueprintProtocolCommandManager.

        Parameters:
        ----------
        hive_node_manager : HiveNodeManager
            Manages the config blueprint.
        outbound_message_queue : MessageQueue
            A queue for outbound messages.
        """
        self.logger: Logger = Logger()
        self.hive_node_manager: HiveNodeManager = hive_node_manager
        self.outbound_message_queue: MessageQueue = outbound_message_queue

        self.logger.debug("BlueprintProtocolCommandManager", "BlueprintProtocolCommandManager initialized...")

    def run(self) -> None:
        """
        Starts the blueprint protocol by periodically sending blueprint messages to *next node in the network.
        Sets next_node to the last element of deprecated_node_list.
        """
        deprecated_node_list = [0]
        while True:
            if BlueprintProtocolCommandManager.enable:
                self.logger.debug("BlueprintProtocolCommandManager", "Running...")

                # Picks the next node
                deprecated_node_list = self.hive_node_manager.get_next_live_node(deprecated_node_list)
                next_node = deprecated_node_list[len(deprecated_node_list) - 1]

                if deprecated_node_list != [0]:
                    blueprint_message: BlueprintMessage = BlueprintMessage(
                        sender=self.hive_node_manager.local_node,
                        recipient=next_node,
                        blueprint=self.hive_node_manager.blueprint_dict,
                        last_update=self.hive_node_manager.last_update,
                        update_id_dict=self.hive_node_manager.outgoing_update_check_id,
                    )
                    # self.logger.info("BlueprintProtocolCommandManager", f"blueprint_message {blueprint_message}")
                    new_hive_message: HiveMessage = HiveMessage(blueprint_message)
                    self.outbound_message_queue.enqueue(new_hive_message)
                    self.logger.info("BlueprintProtocolCommandManager", f"Sending blueprint to {next_node.friendly_name}")
                else:
                    self.logger.debug("BlueprintProtocolCommandManager", "No live nodes found...")

            time.sleep(AppSettings.BLUEPRINT_PROTOCOL_FREQUENCY_IN_SECONDS)

    def enable_blueprint_protocol(self) -> None:
        """
        Enables the blueprint protocol by setting the appropriate flag.
        """
        self.logger.debug("BlueprintProtocolCommandManager", "Enabling blueprint protocol...")
        BlueprintProtocolCommandManager.enable = True

    def disable_blueprint_protocol(self) -> None:
        """
        Disables the blueprint protocol by setting the appropriate flag.
        """
        self.logger.debug("BlueprintProtocolCommandManager", "Disabling blueprint protocol...")
        BlueprintProtocolCommandManager.enable = False
