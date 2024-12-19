from typing import List
import random
import uuid
from entities import Customer, Node, Bearer
from factories import MSISDNFactory, IMSIFactory, IMEIFactory, BearerFactory
from interfaces import CustomerRepository, NodeRepository, BearerRepository

class CustomerService:
    def __init__(self, config: dict, customer_repository: CustomerRepository):
        """
        Initializes the CustomerService with configuration and a customer repository.

        Args:
            config (dict): The configuration dictionary containing MSISDN and network data.
            customer_repository (CustomerRepository): The repository to store and manage customers.
        """
        self.config = config
        self.repository = customer_repository

    def generate_msisdn(self, msisdn_type: str) -> List[str]:
        """
        Generates MSISDNs based on the type and configuration.
        
        Args:
            msisdn_type (str): The type of MSISDN to generate (home, national, international).

        Returns:
            List[str]: A list of generated MSISDNs.
        """
        msisdn_config = self.config['msisdn'].get(msisdn_type)
        if not msisdn_config:
            raise ValueError(f"Invalid MSISDN type: {msisdn_type}")

        country_code = msisdn_config.get('country_code', None)
        ndc_ranges = msisdn_config.get('ndc_ranges', None)
        prefixes = msisdn_config.get('prefixes', None)
        digits = msisdn_config.get('digits', 6) 
        count = msisdn_config.get('count', 1)  

        msisdns = []
        for _ in range(count):
            # Update this line to properly pass the required parameters
            msisdn = MSISDNFactory.generate(
                msisdn_type,  # msisdn type (home, national, international)
                country_code=country_code,  # Country code, if needed
                ndc_ranges=ndc_ranges,  # NDC range, if needed
                prefixes=prefixes,  # Prefixes for international MSISDNs
                digits=digits  # Number of digits
            )
            msisdns.append(msisdn)
        return msisdns

    def generate_customers(self) -> List[Customer]:
        """
        Generates a list of customers based on the configuration.
        
        Returns:
            List[Customer]: A list of generated Customer objects.
        """
        customers = []
        for msisdn_type in self.config['msisdn']:
            msisdns = self.generate_msisdn(msisdn_type)
            for msisdn in msisdns:
                customer = Customer(
                    customer_type=msisdn_type,
                    msisdn=msisdn,
                    imsi=IMSIFactory.generate(),  
                    imei=IMEIFactory.generate()  
                )
                customers.append(customer)
        return customers

    def save_customers(self) -> None:
        """
        Saves generated customers into the repository.
        """
        customers = self.generate_customers()
        for customer in customers:
            customer_key = f"CUS{uuid.uuid4().hex[:8]}"
            try:
                self.repository.add(customer_key, customer)
            except Exception as e:
                print(f"Error saving customer {customer.msisdn}: {e}")

class NodeService:
    def __init__(self, config: dict, node_repository: NodeRepository):
        """
        Initializes the NodeService with configuration and a node repository.

        Args:
            config (dict): The configuration dictionary containing network data.
            node_repository (NodeRepository): The repository to store and manage nodes.
        """
        self.config = config
        self.repository = node_repository

    def generate_addresses(self, network_type: str) -> dict:
        """
        Generates network-specific addresses for 3G or 4G nodes.

        Args:
            network_type (str): The type of network ("3G" or "4G").

        Returns:
            dict: A dictionary of generated addresses.
        """
        if network_type == "3G":
            return {
                "MSC_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "SGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "GGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            }
        elif network_type == "4G":
            return {
                "SGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "PGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "MME_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            }
        else:
            raise ValueError(f"Invalid network_type: {network_type}")

    def generate_node(self, network_type: str) -> Node:
        """
        Generates a single Node based on the network type.

        Args:
            network_type (str): The type of network ("3G" or "4G").

        Returns:
            Node: A generated Node object.
        """
        mcc = self.config["network"]["mcc"]
        mnc = self.config["network"]["mnc"].zfill(3)  # Ensure MNC is zero-padded
        plmn = f"{mcc}{mnc}"

        if network_type == "3G":
            rnc_id = random.randint(1, 65535)
            lac = random.randint(1, 65535)
            cell_id = random.randint(1, 65535)
            addresses = self.generate_addresses("3G")
            return Node(
                network_type="3G",
                plmn=plmn,
                rnc_id=str(rnc_id),
                lac=str(lac),
                cell_id=str(cell_id),
                tac="",
                gNB_ID="",
                NR_Cell_ID="",
                MSC_Address=addresses["MSC_Address"],
                SGSN_Address=addresses["SGSN_Address"],
                GGSN_Address=addresses["GGSN_Address"],
            )
        elif network_type == "4G":
            tac = random.randint(1, 65535)
            addresses = self.generate_addresses("4G")
            return Node(
                network_type="4G",
                plmn=plmn,
                rnc_id="",
                lac="",
                cell_id="",
                tac=str(tac),
                gNB_ID="",
                NR_Cell_ID="",
                SGW_Address=addresses["SGW_Address"],
                PGW_Address=addresses["PGW_Address"],
                MME_Address=addresses["MME_Address"],
            )

    def generate_nodes(self) -> List[Node]:
        """
        Generates a list of nodes based on configuration.

        Returns:
            List[Node]: A list of generated Node objects.
        """
        nodes = []
        for _ in range(self.config["network"]["3g"]["count"]):
            nodes.append(self.generate_node("3G"))
        for _ in range(self.config["network"]["4g"]["count"]):
            nodes.append(self.generate_node("4G"))
        return nodes

    def save_nodes(self) -> None:
        """
        Saves generated nodes into the repository.
        """
        nodes = self.generate_nodes()
        for node in nodes:
            node_key = f"NET{uuid.uuid4().hex[:8]}"
            try:
                # Convert to a dictionary (keys with None values are excluded automatically)
                node_dict = node.to_dict()
                self.repository.add(node_key, Node(**node_dict))
            except Exception as e:
                print(f"Error saving node {node.network_type}: {e}")

class BearerService:
    def __init__(self, config: dict, bearer_repository: BearerRepository):
        """
        Initializes the BearerService with configuration and a bearer repository.

        Args:
            config (dict): The configuration dictionary containing bearer data.
            bearer_repository (BearerRepository): The repository to store and manage bearers.
        """
        self.config = config
        self.repository = bearer_repository

    def generate_bearers(self) -> List[Bearer]:
        """
        Generates a list of bearers based on the configuration.
        
        Returns:
            List[Bearer]: A list of generated Bearer objects.
        """
        bearers = []
        for bearer_type in self.config['bearer']:
            count = self.config['bearer'][bearer_type].get('count', 1)  # Number of bearers to generate
            for _ in range(count):
                bearer = BearerFactory.create_bearer(
                    bearer_id=uuid.uuid4().int,  # Unique ID for the bearer
                    bearer_type=bearer_type
                )
                bearers.append(bearer)
        return bearers

    def save_bearers(self) -> None:
        """
        Saves generated bearers into the repository.
        """
        bearers = self.generate_bearers()
        for bearer in bearers:
            bearer_key = f"BEARER{uuid.uuid4().hex[:8]}"
            try:
                self.repository.add(bearer_key, bearer)
            except Exception as e:
                print(f"Error saving bearer with ID {bearer.bearer_id}: {e}")

    def get_random_bearer(self) -> Bearer:
        """
        Fetches a random bearer from the repository.

        Returns:
            Bearer: A random bearer.
        """
        return self.repository.get_random()

    def get_all_bearers(self) -> List[Bearer]:
        """
        Retrieves all bearers from the repository.

        Returns:
            List[Bearer]: A list of all bearers.
        """
        return self.repository.get_all()
