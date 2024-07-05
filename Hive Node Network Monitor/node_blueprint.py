
class NodeBlueprint:
    """
    DEPRECATED

    Creates a service_list containing a dictionary of service_type: parameter key/value pairs

    { service_type: {"interval": param1, "address": param2, "port": param3} }

    simplified
    { type1: {params}, type2: {params} }

    Within the hive_node_manager object, where the list of NodeBlueprint objects is held in a dict,
    they have their associated profile name as their key
    """
    def __init__(self, service_list: dict = None):
        """
        Initializes a new instance of HiveNode.

        Parameters:
        ----------
        service_list : dict
            Initialize service_list with passed dictionary.
        """
        if service_list:
            self.service_list = service_list
        self.service_list: dict = {}

    def add_or_replace_service(self, service_type, param_list):
        """
        Adds or updates (overwrites) a dict {service: {parameters}} to the service_list dictionary

        parameters:
        ----------
        service_type
            The service_type
        param_list
            The three value long list of parameters - (interval, address, port)
            If any param not in use, set to None
        """
        p1, p2, p3 = param_list
        dict_param_list = {"interval": p1, "address": p2, "port": p3}
        self.service_list.update({service_type: dict_param_list})

    def remove_service(self, service_type):
        """
        Removes a service dict based on the service name

        parameters:
        ----------
        service_type
            The service_type
        """
        self.service_list.pop(service_type)

    def parse_object(self):
        """
        When called, returns service list.
        """
        return self.service_list

