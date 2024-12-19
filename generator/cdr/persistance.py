from tinydb import TinyDB, Query
from typing import List, Optional
import random
from entities import Customer, Node
from interfaces import CustomerRepository, NodeRepository
 
class InMemoryCustomerRepository(CustomerRepository):
    """
    In-memory implementation of the CustomerRepository.
    """
    def __init__(self):
        self.customers: List[Customer] = []

    def add(self, key: str, customer: Customer) -> None:
        """Adds a customer to the repository."""
        self.customers.append(customer)

    def get_random(self, customer_type: str) -> Optional[Customer]:
        """Gets a random customer of a specific type."""
        filtered_customers = [customer for customer in self.customers if customer.customer_type == customer_type]
        return random.choice(filtered_customers) if filtered_customers else None

    def get_all(self) -> List[Customer]:
        """Returns all customers."""
        return self.customers

    def remove(self, msisdn: str) -> None:
        """Removes a customer by MSISDN."""
        self.customers = [customer for customer in self.customers if customer.msisdn != msisdn]


class InMemoryNodeRepository(NodeRepository):
    """
    In-memory implementation of the NodeRepository.
    """
    def __init__(self):
        self.nodes: List[Node] = []

    def add(self, key: str, node: Node) -> None:
        """Adds a node to the repository."""
        self.nodes.append(node)

    def get_all(self) -> List[Node]:
        """Returns all nodes."""
        return self.nodes

    def get_random(self, network_type: str) -> Optional[Node]:
        """Gets a random node of a specific network type."""
        filtered_nodes = [node for node in self.nodes if node.network_type == network_type]
        return random.choice(filtered_nodes) if filtered_nodes else None


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
        Retrieves all nodes in the repository.

        Returns:
            List[Node]: A list of all nodes.
        """
        return [Node(**record) for record in self.table.all()]

    def get_random(self, network_type: str) -> Optional[Node]:
        """
        Retrieves a random node from the repository by network type.

        Args:
            network_type (str): The type of network for the node.

        Returns:
            Optional[Node]: A random node of the specified network type, or None if not found.
        """
        matching_nodes = self.table.search(Query().network_type == network_type)
        if not matching_nodes:
            return None
        random_node = random.choice(matching_nodes)
        return Node(**random_node)

