from abc import ABC, abstractmethod
from typing import List, Optional
import random
from entities import Customer

class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: 'Customer') -> None:
        """
        Adds a customer to the repository.
        
        Args:
            customer (Customer): The customer entity to be added.
        """
        pass

    @abstractmethod
    def get_random(self) -> Optional['Customer']:
        """
        Retrieves a random customer from the repository.
        
        Returns:
            Optional[Customer]: A random customer, or None if the repository is empty.
        """
        pass

    @abstractmethod
    def get_all(self) -> List['Customer']:
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
