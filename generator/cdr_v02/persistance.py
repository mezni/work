import random
import json
from typing import List, Optional, Any
from entities import Customer
from interfaces import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers = {}

    def add(self, customer: 'Customer') -> None:
        """Add a customer to the repository."""
        self.customers[customer.msisdn] = customer

    def get_all(self) -> List['Customer']:
        """Get all customers from the repository."""
        return list(self.customers.values())

    def remove(self, msisdn: str) -> None:
        """Remove a customer from the repository by their MSISDN."""
        if msisdn in self.customers:
            del self.customers[msisdn]


class TidyDB:
    def __init__(self, filename: str):
        self.filename = filename
        self.db = self.load_db()

    def save_db(self):
        """Save the entire database to a JSON file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.db, file, indent=4)
        except Exception as e:
            print(f"Error saving database: {e}")

    def load_db(self):
        """Load the database from a file."""
        try:
            with open(self.filename, 'r') as file:
                data = file.read().strip()
                if not data:
                    return {}
                return json.loads(data)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            return {}

    def get_table(self, table_name: str) -> dict:
        """Retrieve the data for a specific table."""
        return self.db.get(table_name, {})

    def save_table(self, table_name: str, table_data: dict):
        """Save a specific table to the database."""
        self.db[table_name] = table_data
        self.save_db()

    def add(self, table_name: str, key: str, value: Any):
        """Add an item to a specific table."""
        table = self.get_table(table_name)
        table[key] = value.to_dict() if hasattr(value, 'to_dict') else value
        self.save_table(table_name, table)

    def get(self, table_name: str, key: str) -> Any:
        """Retrieve an item from a specific table."""
        table = self.get_table(table_name)
        return table.get(key)

    def get_all(self, table_name: str) -> List[Any]:
        """Retrieve all items from a specific table."""
        table = self.get_table(table_name)
        return [value for key, value in table.items()]

    def remove(self, table_name: str, key: str):
        """Remove an item from a specific table."""
        table = self.get_table(table_name)
        if key in table:
            del table[key]
            self.save_table(table_name, table)
