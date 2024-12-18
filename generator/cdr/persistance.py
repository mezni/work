import random
import json
from typing import List, Optional, Any
from tinydb import TinyDB, Query
from entities import Customer, Node
from interfaces import CustomerRepository, NodeRepository


class InMemoryCustomerRepository(CustomerRepository):
    """
    Concrete implementation of the CustomerRepository using in-memory storage.
    """
    def __init__(self):
        self.customers: List[Customer] = []  # Explicitly type the customers list

    def add(self, customer: Customer) -> None:
        """Add a customer to the repository."""
        self.customers.append(customer)

    def get_random(self) -> Optional[Customer]:
        """Get a random customer from the repository."""
        return random.choice(self.customers) if self.customers else None

    def get_all(self) -> List[Customer]:
        """Get all customers from the repository."""
        return self.customers

    def remove(self, msisdn: str) -> None:
        """Remove a customer by MSISDN."""
        self.customers = [customer for customer in self.customers if customer.msisdn != msisdn]


class InMemoryNodeRepository(NodeRepository):
    """
    Concrete implementation of the NodeRepository using in-memory storage.
    """
    def __init__(self):
        self.nodes: List[Node] = []  # Explicitly type the nodes list

    def add(self, node: Node) -> None:
        """Add a node to the repository."""
        self.nodes.append(node)

    def get_all(self) -> List[Node]:
        """Get all nodes from the repository."""
        return self.nodes

    def get_random(self) -> Optional[Node]:
        """Get a random node from the repository."""
        return random.choice(self.nodes) if self.nodes else None

class TinyDBCustomerRepository(CustomerRepository):
    """
    Concrete implementation of the CustomerRepository using TinyDB for persistence.
    """
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.table = self.db.table('customers')

    def add(self, customer: Customer) -> None:
        """Add a customer to the repository in TinyDB."""
        self.table.insert(customer.to_dict())

    def get_random(self) -> Optional[Customer]:
        """Get a random customer from the repository."""
        customers = self.table.all()
        return Customer(**random.choice(customers)) if customers else None

    def get_all(self) -> List[Customer]:
        """Get all customers from the repository."""
        return [Customer(**customer) for customer in self.table.all()]

    def remove(self, msisdn: str) -> None:
        """Remove a customer by MSISDN."""
        CustomerQuery = Query()
        self.table.remove(CustomerQuery.msisdn == msisdn)


class TinyDBNodeRepository(NodeRepository):
    """
    Concrete implementation of the NodeRepository using TinyDB for persistence.
    """
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.table = self.db.table('nodes')

    def add(self, node: Node) -> None:
        """Add a node to the repository in TinyDB."""
        self.table.insert(node.to_dict())

    def get_all(self) -> List[Node]:
        """Get all nodes from the repository."""
        return [Node(**node) for node in self.table.all()]

    def get_random(self) -> Optional[Node]:
        """Get a random node from the repository."""
        nodes = self.table.all()
        return Node(**random.choice(nodes)) if nodes else None