from base_message import BaseMessage
from hive_node import HiveNode
from typing import Dict


class BlueprintMessage(BaseMessage):
    """
    GossipMessage represents a message for gossip protocol in the Hive network.

    Attributes:
    ----------
    sender : HiveNode
        The sender node of the message.
    recipient : HiveNode
        The recipient node of the message.
    blueprint : Dict[str, dict]
        A dictionary containing the config blueprint
    """

    def __init__(self, sender: HiveNode, recipient: HiveNode, blueprint: dict, last_update, update_id_dict):
        """
        Initializes a new instance of GossipMessage.

        Parameters:
        ----------
        sender : HiveNode
            The sender node of the message.
        recipient : HiveNode
            The recipient node of the message.
        blueprint : Dict[str, dict]
            A dictionary containing the config blueprint
        last_update
            Time of local array last update
        update_id_dict : dict
            The outgoing update ID dict to update the (NetworkMonitor) of the intended hive node
        """
        super().__init__(sender, recipient, 'blueprint')
        self.blueprint: dict = blueprint
        self.last_update = last_update
        self.update_id_dict = update_id_dict

    def to_dict(self) -> Dict[str, dict]:
        """
        Converts the BlueprintMessage instance to a dictionary representation.
        Also appends a last_update float to the base_message dict

        Returns:
        -------
        Dict[str, dict]
            A dictionary representing the BlueprintMessage instance.
        """
        base_dict: Dict[str, dict] = super().to_dict()
        base_dict.update({'blueprint': self.blueprint})
        base_dict.update({'last_update': self.last_update})
        base_dict.update({'update_id_dict': self.update_id_dict})
        return base_dict
