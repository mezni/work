from entities import Customer, Node
from persistance import TinyDBCustomerRepository,TinyDBNodeRepository

db_path = 'config.json'


# Create TinyDB repositories with specific filenames
customer_repo = TinyDBCustomerRepository(db_path)
node_repo = TinyDBNodeRepository(db_path)

customer1 = Customer("regular", "123456789", "987654321098765", "123456789012345")
customer2 = Customer("premium", "987654321", "123456789012345", "987654321098765")
customer_repo.add(customer1)
customer_repo.add(customer2)

# Add nodes
node1 = Node("5G", "RNC1", "LAC1", "CELL1", "TAC1", "GNB1", "NR_CELL1")
node2 = Node("LTE", "RNC2", "LAC2", "CELL2", "TAC2", "GNB2", "NR_CELL2")
node_repo.add(node1)
node_repo.add(node2)
