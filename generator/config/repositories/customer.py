from tinydb import TinyDB

class CustomerRepository:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def save_customer(self, customer, customer_type):
        table = self.db.table(customer_type)
        table.insert(customer.to_dict())

    def get_all_customers(self, customer_type):
        table = self.db.table(customer_type)
        return [customer for customer in table.all()]
