from tinydb import TinyDB, Query
from typing import List, Optional
import random
from value_objects import QoS
from entities import Customer, Node, Bearer
from interfaces import CustomerRepository, NodeRepository, BearerRepository

class InMemoryCustomerRepository(CustomerRepository):
    """
    In-memory implementation of the CustomerRepository, aligned with TinyDB behavior.
    """

    def __init__(self):
        # Initialize an empty list of customers
        self.customers: List[dict] = []  # Using a dict to mimic the format used in TinyDB

    def add(self, key: str, customer: Customer) -> None:
        """
        Add a customer to the repository in memory.
        
        Args:
            key (str): Unique key for the customer.
            customer (Customer): The customer entity to be added.
        """
        # Simulating the TinyDB behavior by storing the customer as a dictionary
        if any(item.get(key) for item in self.customers):
            raise ValueError(f"Customer with key {key} already exists.")
        
        # Add customer as a dictionary similar to TinyDB format
        self.customers.append({key: customer.to_dict()})

    def get_random(self, customer_type: str) -> Optional[Customer]:
        """
        Retrieve a random customer of a specific type from the repository.
        
        Args:
            customer_type (str): The customer type to filter by.
        
        Returns:
            Optional[Customer]: A random customer matching the type, or None if no match.
        """
        # Filter customers based on the 'customer_type' field
        matching_customers = [
            Customer(**data[key]) for data in self.customers for key in data
            if data[key]["customer_type"] == customer_type
        ]
        return random.choice(matching_customers) if matching_customers else None

    def get_all(self) -> List[Customer]:
        """
        Retrieve all customers from the repository.

        Returns:
            List[Customer]: A list of all customers.
        """
        # Return all customers by converting dictionary back to Customer objects
        return [
            Customer(**data[key]) for data in self.customers for key in data
        ]

    def remove(self, key: str) -> None:
        """
        Remove a customer by key from the repository.

        Args:
            key (str): The key of the customer to remove.
        """
        # Filter out the customer with the matching key
        self.customers = [
            customer for customer in self.customers if key not in customer
        ]



class InMemoryNodeRepository(NodeRepository):
    """
    In-memory implementation of the NodeRepository, aligned with TinyDB behavior.
    """

    def __init__(self):
        # Initialize an empty list to store nodes, simulating TinyDB storage
        self.nodes: List[dict] = []  # Using dict to mimic TinyDB record structure

    def add(self, key: str, node: Node) -> None:
        """
        Add a node to the repository in memory.
        
        Args:
            key (str): Unique key for the node.
            node (Node): The node entity to be added.
        """
        # Simulate the TinyDB behavior by storing the node as a dictionary
        if any(item.get(key) for item in self.nodes):
            raise ValueError(f"Node with key {key} already exists.")
        
        # Add node as a dictionary to match TinyDB's format
        self.nodes.append({key: node.to_dict()})

    def get_random(self, network_type: str) -> Optional[Node]:
        """
        Retrieve a random node of a specific network type from the repository.
        
        Args:
            network_type (str): The network type to filter by.
        
        Returns:
            Optional[Node]: A random node matching the network type, or None if no match.
        """
        # Filter nodes by network_type and return a random node
        matching_nodes = [
            Node(**data[key]) for data in self.nodes for key in data
            if data[key]["network_type"] == network_type
        ]
        return random.choice(matching_nodes) if matching_nodes else None

    def get_all(self) -> List[Node]:
        """
        Retrieve all nodes from the repository.

        Returns:
            List[Node]: A list of all nodes.
        """
        # Convert stored dictionary data into Node objects
        return [
            Node(**data[key]) for data in self.nodes for key in data
        ]

    def remove(self, key: str) -> None:
        """
        Remove a node by key from the repository.

        Args:
            key (str): The key of the node to remove.
        """
        # Remove the node with the matching key
        self.nodes = [
            node for node in self.nodes if key not in node
        ]


class InMemoryBearerRepository(BearerRepository):
    """
    In-memory implementation of the BearerRepository, aligned with TinyDB behavior.
    """

    def __init__(self):
        # Initialize an empty list to store bearers, simulating TinyDB storage
        self.bearers: List[dict] = []  # Using dict to mimic TinyDB record structure

    def add(self, key: str, bearer: Bearer) -> None:
        """
        Add a bearer to the repository in memory.
        
        Args:
            key (str): Unique key for the bearer.
            bearer (Bearer): The bearer entity to be added.
        """
        # Simulate the TinyDB behavior by storing the bearer as a dictionary
        if any(item.get(key) for item in self.bearers):
            raise ValueError(f"Bearer with key {key} already exists.")
        
        # Add bearer as a dictionary to match TinyDB's format
        self.bearers.append({key: bearer.to_dict()})

    def get_random(self) -> Optional[Bearer]:
        """
        Retrieve a random bearer from the repository.
        
        Returns:
            Optional[Bearer]: A random bearer or None if not found.
        """
        # Convert stored bearer data into Bearer objects and return a random one
        all_bearers = [Bearer(**data[key]) for data in self.bearers for key in data]
        return random.choice(all_bearers) if all_bearers else None

    def get_all(self) -> List[Bearer]:
        """
        Retrieve all bearers from the repository.

        Returns:
            List[Bearer]: A list of all bearers.
        """
        # Convert stored dictionary data into Bearer objects
        return [
            Bearer(**data[key]) for data in self.bearers for key in data
        ]

    def remove(self, key: str) -> None:
        """
        Remove a bearer by key from the repository.

        Args:
            key (str): The key of the bearer to remove.
        """
        # Remove the bearer with the matching key
        self.bearers = [
            bearer for bearer in self.bearers if key not in bearer
        ]


class TinyDBCustomerRepository(CustomerRepository):
    """
    Concrete implementation of the CustomerRepository using TinyDB for persistence.
    """
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.table = self.db.table('customers')

    def add(self, key: str, customer: Customer) -> None:
        """
        Add a customer to the repository in TinyDB using the key as the primary identifier.

        Args:
            key (str): Unique key for the customer.
            customer (Customer): Customer entity to be added.
        """
        if key in self.table:
            raise ValueError(f"Customer with key {key} already exists.")

        self.table.insert({key: customer.to_dict()})

    def get_random(self, customer_type: str) -> Optional[Customer]:
        """
        Get a random customer of a specific type from the repository.

        Args:
            customer_type (str): The type of customer to retrieve.

        Returns:
            Optional[Customer]: A random customer or None if not found.
        """
        matching_customers = [
            Customer(**data[key]) for data in self.table.all()
            for key in data if data[key]["customer_type"] == customer_type
        ]
        return random.choice(matching_customers) if matching_customers else None

    def get_all(self) -> List[Customer]:
        """
        Retrieve all customers from the repository.

        Returns:
            List[Customer]: A list of all customers.
        """
        return [
            Customer(**data[key]) for data in self.table.all() for key in data
        ]

    def remove(self, key: str) -> None:
        """
        Remove a customer by key.

        Args:
            key (str): The key of the customer to remove.
        """
        self.table.remove(doc_ids=[
            doc.doc_id for doc in self.table.all() if key in doc
        ])


class TinyDBNodeRepository(NodeRepository):
    """
    Concrete implementation of the NodeRepository using TinyDB for persistence.
    """
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.table = self.db.table('nodes')

    def add(self, key: str, node: Node) -> None:
        """
        Adds a node to the repository.

        Args:
            key (str): The unique identifier for the node.
            node (Node): The node entity to be added.
        """
        if key in self.table:
            raise ValueError(f"Customer with key {key} already exists.")

        self.table.insert({key: node.to_dict()})

    def get_all(self) -> List[Node]:
        """
        Retrieves all nodes from the repository.
        
        Returns:
            List[Node]: A list of all Node objects.
        """
        # Assuming that the table contains records with a primary key and other node attributes
        return [
            Node(**data[key]) for data in self.table.all() for key in data
        ]

    def get_random(self, network_type: str) -> Optional[Node]:
        """
        Retrieves a random node from the repository by network type.

        Args:
            network_type (str): The type of network for the node.

        Returns:
            Optional[Node]: A random node of the specified network type, or None if not found.
        """
        matching_nodes = [
            Node(**data[key]) for data in self.table.all()
            for key in data if data[key]["network_type"] == network_type
        ]
        return random.choice(matching_nodes) if matching_nodes else None

class TinyDBBearerRepository(BearerRepository):
    """
    Concrete implementation of the BearerRepository using TinyDB for persistence.
    """

    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.table = self.db.table('bearers')

    def add(self, key: str, bearer: Bearer) -> None:
        """
        Add a bearer to the repository in TinyDB using the key as the primary identifier.

        Args:
            key (str): Unique key for the bearer.
            bearer (Bearer): Bearer entity to be added.
        """
        if key in self.table:
            raise ValueError(f"Bearer with key {key} already exists.")

        self.table.insert({key: bearer.to_dict()})

    def get_random(self) -> Optional[Bearer]:
        """
        Get a random bearer from the repository.

        Returns:
            Optional[Bearer]: A random bearer or None if not found.
        """
        all_bearers = [Bearer(**data[key]) for data in self.table.all() for key in data]
        return random.choice(all_bearers) if all_bearers else None

    def get_all(self):
        return [
            Bearer(
                bearer_id=record_data.get('Bearer_ID', 1),  
                bearer_type=record_data.get('Bearer_Type', 'Default Bearer'),  
                qos=QoS(
                    gbr=record_data.get('QoS', {}).get('gbr', 1),  
                    mbr=record_data.get('QoS', {}).get('mbr', 1000)  
                )
            )
            for record in self.table.all()  # Assuming self.table.all() returns data like the structure you've shown
            for record_key, record_data in record.items()  # Iterate through each record in the data
        ]


    def remove(self, key: str) -> None:
        """
        Remove a bearer by key.

        Args:
            key (str): The key of the bearer to remove.
        """
        self.table.remove(doc_ids=[
            doc.doc_id for doc in self.table.all() if key in doc
        ])
