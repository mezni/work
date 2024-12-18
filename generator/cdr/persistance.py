import random
from typing import List, Optional
from entities import Customer
from interfaces import CustomerRepository

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers = []

    def add(self, customer: 'Customer') -> None:
        self.customers.append(customer)

    def get_random(self) -> Optional['Customer']:
        if not self.customers:
            return None
        return random.choice(self.customers)  

    def get_all(self) -> List['Customer']:
        return self.customers

    def remove(self, msisdn: str) -> None:
        self.customers = [customer for customer in self.customers if customer.msisdn != msisdn]


class TidyDB:
    def __init__(self):
        self.db = {}

    def add(self, key: str, value: Customer):
        self.db[key] = value

    def get(self, key: str) -> Customer:
        return self.db.get(key)

    def get_all(self) -> List[Customer]:
        return list(self.db.values())

    def remove(self, key: str) -> None:
        if key in self.db:
            del self.db[key]
