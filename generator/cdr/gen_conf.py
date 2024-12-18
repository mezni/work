from services import CustomerService, NodeService
from persistance import TidyDB

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
    }
}


# Instantiate the repository (TidyDB for this example)
repository = TidyDB('config.json','customers')

# Instantiate the CustomerService with the repository
customer_service = CustomerService(config, repository)

# Save the generated customers into the repository
customer_service.save_customers()

# Fetch and print all customers from the repository
for customer in repository.get_all():
    print(customer)

config = {
    "network": {
        "mcc": "212",
        "mnc": "01",
        "3g": {"count": 10},
        "4g": {"count": 10}
    }
}

repository = TidyDB('config.json','networks')
node_service = NodeService(config, repository)

# Generate nodes from the configuration
nodes = node_service.generate_nodes_from_config()

# Print generated nodes
for node in repository.get_all():
    print(node.to_dict())