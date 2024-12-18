import json
import uuid
import random
from typing import List
from random import randint
from value_objects import MSISDN, IMSI, IMEI
from entities import Customer, Node
from factories import MSISDNFactory, IMSIFactory, IMEIFactory
from interfaces import CustomerRepository, NodeRepository

class CustomerService:
    def __init__(self, config: dict, repository: CustomerRepository):
        self.config = config
        self.repository = repository

    def generate_msisdn(self, msisdn_type: str) -> str:
        """Generates an MSISDN based on the type (home, national, or international)."""
        msisdn_config = self.config['msisdn'][msisdn_type]

        if msisdn_type == "home" or msisdn_type == "national":
            country_code = msisdn_config['country_code']
            ndc_range = msisdn_config['ndc_ranges']
            prefix = None
            digits = msisdn_config['digits']
            count = msisdn_config['count']
            msisdns = []

            for _ in range(count):
                ndc = random.choice(ndc_range)  # Randomly select a NDC range
                msisdns.append(MSISDNFactory.generate(msisdn_type, country_code, ndc, prefix,digits=digits))

            return msisdns

        elif msisdn_type == "international":
            country_code = None
            ndc = None
            prefix = msisdn_config['prefixes']
            digits = msisdn_config['digits']
            count = msisdn_config['count']
            msisdns = []

            for _ in range(count):
                msisdns.append(MSISDNFactory.generate(msisdn_type, country_code, ndc, prefix, digits=digits))

            return msisdns

        else:
            raise ValueError(f"Invalid MSISDN type: {msisdn_type}")

    def generate_customers(self) -> List[Customer]:
        """Generates customers based on the config and returns a list of Customer objects."""
        customers = []

        for msisdn_type in self.config['msisdn']:
            msisdns = self.generate_msisdn(msisdn_type)

            for msisdn in msisdns:
                customer = Customer(
                    customer_type=msisdn_type,
                    msisdn=msisdn,
                    imsi=IMSI(IMSIFactory.generate()),  # No need for str()
                    imei=IMEI(IMEIFactory.generate())   # No need for str()
                )
                customers.append(customer)

        return customers

    def save_customers(self):
        """Generates and saves customers to the repository."""
        customers = self.generate_customers()
        for customer in customers:
            # Use customer.msisdn as the key to store it in the TidyDB
            customer_key = f"CUS{uuid.uuid4().hex[:8]}"

            # Add the customer to the repository using the modified key
            self.repository.add(customer_key, customer)



class NodeService:
    def __init__(self, config: dict, repository: 'NodeRepository'):
        """
        Initializes the NodeService with configuration and repository.

        Args:
            config (dict): Configuration dictionary containing network parameters.
            repository (NodeRepository): The repository object for storing and retrieving nodes.
        """
        self.config = config
        self.repository = repository

    def generate_node(self, network_type: str, mcc: str, mnc: str, 
                      shared_3g_addresses: dict = None, shared_4g_addresses: dict = None) -> Node:
        """
        Generates a Node entity based on the provided network type, MCC, and MNC.

        Args:
            network_type (str): The network type ("3G", "4G").
            mcc (str): The MCC value from the config.
            mnc (str): The MNC value from the config.
            shared_3g_addresses (dict): Shared addresses for 3G nodes.
            shared_4g_addresses (dict): Shared addresses for 4G nodes.

        Returns:
            Node: The generated Node object with appropriate fields.
        """
        # Ensure MNC is two digits (padding with leading zero if necessary)
        mnc_padded = mnc.zfill(3)  # To handle cases like "01" (it will become "001")

        plmn = f"{mcc}{mnc_padded}"

        if network_type == "3G":
            rnc_id = random.randint(1, 65535)
            lac = random.randint(1, 65535)
            cell_id = random.randint(1, 65535)
            
            # Use the shared addresses for 3G
            MSC_Address = shared_3g_addresses["MSC_Address"]
            SGSN_Address = shared_3g_addresses["SGSN_Address"]
            GGSN_Address = shared_3g_addresses["GGSN_Address"]

            node = Node(
                network_type=network_type,
                rnc_id=str(rnc_id),
                lac=str(lac),
                cell_id=str(cell_id),
                tac="",
                gNB_ID="",
                NR_Cell_ID="",
                MSC_Address=MSC_Address,
                SGSN_Address=SGSN_Address,
                GGSN_Address=GGSN_Address,
                plmn=plmn
            )
            # Add the node to the repository
            node_key = f"NET{uuid.uuid4().hex[:8]}"
            self.repository.add(node_key,node)
            return node

        elif network_type == "4G":
            tac = random.randint(1, 65535)

            # Use the shared addresses for 4G
            SGW_Address = shared_4g_addresses["SGW_Address"]
            PGW_Address = shared_4g_addresses["PGW_Address"]
            MME_Address = shared_4g_addresses["MME_Address"]

            node = Node(
                network_type=network_type,
                rnc_id="",
                lac="",
                cell_id="",
                tac=str(tac),
                gNB_ID="",
                NR_Cell_ID="",
                MSC_Address=None,
                SGSN_Address=None,
                GGSN_Address=None,
                plmn=plmn,
                SGW_Address=SGW_Address,
                PGW_Address=PGW_Address,
                MME_Address=MME_Address
            )
            # Add the node to the repository
            node_key = f"NET{uuid.uuid4().hex[:8]}"
            self.repository.add(node_key,node)
            return node
        else:
            raise ValueError(f"Invalid network_type: {network_type}")

    def generate_nodes_from_config(self):
        """
        Generates nodes based on the provided configuration and adds them to the repository.

        Returns:
            list: List of generated nodes.
        """
        nodes = []

        # Extract MCC and MNC from config
        mcc = self.config["network"]["mcc"]
        mnc = self.config["network"]["mnc"]

        # Generate shared addresses for 3G nodes
        shared_3g_addresses = {
            "MSC_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "SGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "GGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        }

        # Generate shared addresses for 4G nodes
        shared_4g_addresses = {
            "SGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "PGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "MME_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        }

        # Generate 3G nodes and add them to the repository
        for _ in range(self.config["network"]["3g"]["count"]):
            node_3g = self.generate_node("3G", mcc, mnc, shared_3g_addresses)
            nodes.append(node_3g)

        # Generate 4G nodes and add them to the repository
        for _ in range(self.config["network"]["4g"]["count"]):
            node_4g = self.generate_node("4G", mcc, mnc, shared_3g_addresses=None, shared_4g_addresses=shared_4g_addresses)
            nodes.append(node_4g)

        return nodes
