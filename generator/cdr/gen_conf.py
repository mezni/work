import logging
from persistance import TinyDBCustomerRepository, TinyDBNodeRepository
from services import CustomerService, NodeService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main entry point
def main():
    # Configuration
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

    # Define the database path
    db_path = 'config.json'

    # Initialize the repository using the db_path variable
    customer_repo = TinyDBCustomerRepository(db_path)
    node_repo = TinyDBNodeRepository(db_path)
    customer_service = CustomerService(config,customer_repo)
    node_service = NodeService(config,node_repo)
    customer_service.save_customers()
    node_service.save_nodes()




if __name__ == "__main__":
    main()
