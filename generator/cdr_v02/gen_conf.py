import logging
from services import CustomerService, NodeService
from persistance import TidyDB

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration dictionary
config = {
    "msisdn": {
        "home": {
            "country_code": "+216",
            "ndc_ranges": [[30, 35], [50, 55]],
            "digits": 6,
            "count": 10
        },
        "national": {
            "country_code": "+216",
            "ndc_ranges": [[20, 29], [90, 99]],
            "digits": 6,
            "count": 10
        },
        "international": {
            "prefixes": ["+2126", "+336", "+441", "+491"],
            "digits": 8,
            "count": 10
        }
    },
    "network": {
        "mcc": "212",
        "mnc": "01",
        "3g": {"count": 10},
        "4g": {"count": 10}
    }
}

# Database setup
db = TidyDB('config.json')

# Get repository tables
repository_customers = db.get_table('customers')
repository_networks = db.get_table('networks')

# Instantiate the CustomerService with the repository
customer_service = CustomerService(config, repository_customers)

# Save the generated customers into the repository with error handling
try:
    customer_service.save_customers()
    logging.info("Customers successfully saved.")
except Exception as e:
    logging.error(f"Error saving customers: {e}")

# Fetch and print a limited number of customers from the repository
logging.info("Fetching and displaying customers:")
# Since repository_customers is a dictionary, we iterate over its values
for customer_key, customer in list(repository_customers.items())[:5]:  # Show only the first 5 customers
    print(customer)

# Instantiate the NodeService with the repository
node_service = NodeService(config, repository_networks)

# Generate nodes from the configuration with error handling
try:
    nodes = node_service.generate_nodes_from_config()
    logging.info(f"Generated {len(nodes)} nodes successfully.")
except Exception as e:
    logging.error(f"Error generating nodes: {e}")

# Print the generated nodes
logging.info("Fetching and displaying nodes:")
# Since repository_networks is a dictionary, we iterate over its values
#for node_key, node in list(repository_networks.items())[:5]:  # Show only the first 5 nodes
#    print(node.to_dict())
