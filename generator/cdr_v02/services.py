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

    def generate_msisdn(self, msisdn_type: str) -> List[str]:
        msisdn_config = self.config['msisdn'].get(msisdn_type)
        if not msisdn_config:
            raise ValueError(f"Invalid MSISDN type: {msisdn_type}")
        
        country_code = msisdn_config['country_code']
        ndc_range = msisdn_config['ndc_ranges']
        digits = msisdn_config['digits']
        count = msisdn_config['count']

        msisdns = []
        for _ in range(count):
            ndc = random.choice(ndc_range)
            msisdns.append(MSISDNFactory.generate(msisdn_type, country_code, ndc, None, digits))
        return msisdns

    def generate_customers(self) -> List[Customer]:
        customers = []
        for msisdn_type in self.config['msisdn']:
            msisdns = self.generate_msisdn(msisdn_type)
            for msisdn in msisdns:
                customer = Customer(
                    customer_type=msisdn_type,
                    msisdn=msisdn,
                    imsi=IMSI(IMSIFactory.generate()),
                    imei=IMEI(IMEIFactory.generate())
                )
                customers.append(customer)
        return customers

    def save_customers(self):
        customers = self.generate_customers()
        for customer in customers:
            try:
                customer_key = f"CUS{uuid.uuid4().hex[:8]}"
                self.repository.add(customer_key, customer)
            except Exception as e:
                print(f"Error saving customer {customer.msisdn}: {e}")



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
    def __init__(self, config: dict, repository: NodeRepository):
        self.config = config
        self.repository = repository

    def generate_3g_addresses(self):
        return {
            "MSC_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "SGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "GGSN_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        }

    def generate_4g_addresses(self):
        return {
            "SGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "PGW_Address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "MME_Address": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        }

    def generate_node(self, network_type: str, mcc: str, mnc: str, 
                      shared_3g_addresses: dict = None, shared_4g_addresses: dict = None) -> Node:
        mnc_padded = mnc.zfill(3)
        plmn = f"{mcc}{mnc_padded}"

        if network_type == "3G":
            rnc_id = random.randint(1, 65535)
            lac = random.randint(1, 65535)
            cell_id = random.randint(1, 65535)
            addresses = self.generate_3g_addresses()
            node = Node(
                network_type=network_type,
                rnc_id=str(rnc_id),
                lac=str(lac),
                cell_id=str(cell_id),
                tac="",
                gNB_ID="",
                NR_Cell_ID="",
                MSC_Address=addresses["MSC_Address"],
                SGSN_Address=addresses["SGSN_Address"],
                GGSN_Address=addresses["GGSN_Address"],
                plmn=plmn
            )
            return node
        elif network_type == "4G":
            tac = random.randint(1, 65535)
            addresses = self.generate_4g_addresses()
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
                SGW_Address=addresses["SGW_Address"],
                PGW_Address=addresses["PGW_Address"],
                MME_Address=addresses["MME_Address"]
            )
            return node
        else:
            raise ValueError(f"Invalid network_type: {network_type}")

    def save_nodes(self, nodes: List[Node]):
        for node in nodes:
            try:
                node_key = f"NET{uuid.uuid4().hex[:8]}"
                self.repository.add(node_key, node)
            except Exception as e:
                print(f"Error saving node {node.network_type}: {e}")

