from abc import ABC, abstractmethod
from typing import List, Optional
from entities import Customer, Node  # Assuming Customer and Node are defined in entities.py

class CustomerRepository(ABC):
    """
    Abstract base class for a repository that manages customers.
    """
    @abstractmethod
    def add(self, customer: Customer) -> None:
        """
        Adds a customer to the repository.

        Args:
            customer (Customer): The customer entity to be added.
        """
        pass

    @abstractmethod
    def get_random(self) -> Optional[Customer]:
        """
        Retrieves a random customer from the repository.

        Returns:
            Optional[Customer]: A random customer, or None if the repository is empty.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Customer]:
        """
        Retrieves all customers in the repository.

        Returns:
            List[Customer]: A list of all customers.
        """
        pass

    @abstractmethod
    def remove(self, msisdn: str) -> None:
        """
        Removes a customer from the repository by their MSISDN.

        Args:
            msisdn (str): The MSISDN of the customer to remove.
        """
        pass


class NodeRepository(ABC):
    """
    Abstract base class for a repository that manages nodes.
    """
    @abstractmethod
    def add(self, node: Node) -> None:
        """
        Adds a node to the repository.

        Args:
            node (Node): The node entity to be added.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Node]:
        """
        Retrieves all nodes in the repository.

        Returns:
            List[Node]: A list of all nodes.
        """
        pass
    
    @abstractmethod
    def get_random(self) -> Optional[Node]:
        """
        Retrieves a random node from the repository.

        Returns:
            Optional[Node]: A random node, or None if the repository is empty.
        """
        pass