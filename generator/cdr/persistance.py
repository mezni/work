import random
import json
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
    def __init__(self, filename: str, table_name: str):
        self.filename = filename
        self.table_name = table_name  
        self.db = self.load_db()

    def save_db(self):
        """Save the current database to a JSON file."""
        try:
            with open(self.filename, 'w') as file:
                # Wrap the table data in a dictionary with the table name
                data = {self.table_name: {key: customer.to_dict() for key, customer in self.db.items()}}
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving database: {e}")

    def load_db(self):
        """Load the database from a file."""
        try:
            with open(self.filename, 'r') as file:
                data = file.read().strip()
                if not data:
                    return {}
                loaded_data = json.loads(data)
                # Retrieve the data for the specific table name
                if self.table_name in loaded_data:
                    return {key: Customer(**value) for key, value in loaded_data[self.table_name].items()}
                else:
                    return {}
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            return {}

    def add(self, key: str, value: 'Customer') -> None:
        """Adds a customer to the repository."""
        self.db[key] = value
        self.save_db()  # Save the changes to the file

    def get(self, key: str) -> 'Customer':
        """Retrieves a customer by key (MSISDN)."""
        return self.db.get(key)

    def get_all(self) -> List['Customer']:
        """Retrieves all customers in the repository."""
        return list(self.db.values())

    def remove(self, key: str) -> None:
        """Removes a customer by MSISDN."""
        if key in self.db:
            del self.db[key]
            self.save_db()  # Save the changes to the file


