from services.customer import CustomerService
from repositories.customer import CustomerRepository

def main():

    db_path = "settings.json"

    # Initialize services and repositories
    customer_service = CustomerService()
    customer_repository = CustomerRepository(db_path)

    # Generate customers
    customers = customer_service.generate_all_customers()

    # Save customers to the respective tables in TinyDB
    for customer_type, customer_list in customers.items():
        for customer in customer_list:
            customer_repository.save_customer(customer, customer_type)
    
    print("Customers saved to database!")

if __name__ == "__main__":
    main()
