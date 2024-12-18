from abc import ABC, abstractmethod
from typing import List, Optional

class MSISDNRepository(ABC):    
    @abstractmethod
    def get_random(self) -> Optional['MSISDN']:
        """
        Retrieve a random MSISDN entity from the repository.
        """
        pass