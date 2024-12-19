from abc import ABC, abstractmethod
from typing import List, Optional
from entities import Customer, Node, Bearer

class CustomerRepository(ABC):
    """
    Abstract base class for a repository that manages customers.
    """
    @abstractmethod
    def add(self, key: str, customer: Customer) -> None: 
        """
        Adds a customer to the repository.

        Args:
            key (str): The unique identifier for the customer.
            customer (Customer): The customer entity to be added.
        """
        pass

    @abstractmethod
    def get_random(self, customer_type: str) -> Optional[Customer]:
        """
        Retrieves a random customer from the repository by type.

        Args:
            customer_type (str): The type of customer to retrieve.

        Returns:
            Optional[Customer]: A random customer of the specified type, or None if not found.
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
    def add(self, key: str, node: Node) -> None:
        """
        Adds a node to the repository.

        Args:
            key (str): The unique identifier for the node.
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
    def get_random(self, network_type: str) -> Optional[Node]:
        """
        Retrieves a random node from the repository by network type.

        Args:
            network_type (str): The type of network for the node.

        Returns:
            Optional[Node]: A random node of the specified network type, or None if not found.
        """
        pass


class BearerRepository(ABC):
    """
    Abstract base class for a repository that manages Bearer objects.
    """

    @abstractmethod
    def add(self, key: str, bearer: Bearer) -> None:
        """
        Adds a Bearer object to the repository.

        Args:
            key (str): The unique identifier for the bearer.
            bearer (Bearer): The Bearer object to be added.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Bearer]:
        """
        Retrieves all Bearer objects in the repository.

        Returns:
            List[Bearer]: A list of all Bearer objects.
        """
        pass

    @abstractmethod
    def get_random(self) -> Optional[Bearer]:
        """
        Retrieves a Bearer object by its ID.

        Args:
            bearer_id (int): The unique ID of the bearer.

        Returns:
            Optional[Bearer]: The Bearer object with the specified ID, or None if not found.
        """
        pass

