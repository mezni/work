import random
import yaml
from tinydb import TinyDB

def save_customers_to_db(customers, db_path="settings.json"):
    """
    Save customers to separate TinyDB tables for local, national, and international customers.
    :param customers: Dictionary of customer lists for different types (local, national, international)
    :param db_path: Path to the TinyDB database file
    """
    # Initialize TinyDB
    db = TinyDB(db_path)

    # Insert customers into the respective tables
    for customer_type, customer_list in customers.items():
        if customer_type == 'local':
            table = db.table('customer_home')
        elif customer_type == 'national':
            table = db.table('customer_national')
        elif customer_type == 'international':
            table = db.table('customer_international')
        for customer in customer_list:
            table.insert(customer)

    print(f"{sum(len(customer_list) for customer_list in customers.values())} customer(s) saved to '{db_path}'")

# Function to generate a valid IMEI
def generate_imei():
    """
    Generate a valid IMEI (International Mobile Equipment Identity).
    :return: IMEI as a string
    """
    # Generate the first 14 digits randomly
    imei = [str(random.randint(0, 9)) for _ in range(14)]

    # Calculate the check digit using the Luhn algorithm
    sum = 0
    alt = 0
    for i in range(14):
        digit = int(imei[i])
        if alt == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum += digit
        alt = 1 - alt
    check_digit = (10 - (sum % 10)) % 10

    # Append the check digit to the IMEI
    imei.append(str(check_digit))

    return ''.join(imei)


def generate_imsi():
    """
    Generate a valid IMSI (International Mobile Subscriber Identity).
    :return: IMSI as a string
    """
    # Generate the MCC (Mobile Country Code)
    mcc = str(random.randint(100, 999))

    # Generate the MNC (Mobile Network Code)
    mnc = str(random.randint(0, 999))

    # Generate the MSIN (Mobile Subscriber Identification Number)
    msin = str(random.randint(0, 999999999))

    # Construct the IMSI
    imsi = f"{mcc}{mnc}{msin}"

    return imsi

# Function to generate MSISDN based on the type
def generate_msisdn(msisdn_type, config):
    """
    Generate a random MSISDN (Mobile Station International Subscriber Directory Number).
    :param msisdn_type: Type of MSISDN to generate ('local', 'national', 'international')
    :param config: Configuration dictionary containing MSISDN generation settings
    :return: MSISDN as a string
    """
    # Check if the MSISDN type exists in the config
    if msisdn_type not in config['msisdn']:
        raise KeyError(f"{msisdn_type} not found in configuration!")

    # Access the relevant MSISDN settings from the config
    msisdn_config = config['msisdn'][msisdn_type]
    
    if msisdn_type == "local" or msisdn_type == "national":
        country_code = msisdn_config["country_code"]
        ndc_ranges = msisdn_config.get("ndc_ranges", [])
        digits = msisdn_config["digits"]

        # Generate NDC
        ndc_range = random.choice(ndc_ranges)
        ndc = random.randint(ndc_range[0], ndc_range[1])
        # Generate Subscriber Number
        subscriber_number = random.randint(10**(digits-1), 10**digits - 1)
        msisdn = f"{country_code}{ndc}{subscriber_number}"
        
    elif msisdn_type == "international":
        prefixes = msisdn_config.get("prefixes", [])
        digits = msisdn_config["digits"]
        
        # Generate International MSISDN
        prefix = random.choice(prefixes)
        subscriber_number = random.randint(10**(digits-1), 10**digits - 1)
        msisdn = f"{prefix}{subscriber_number}"
    
    return msisdn

def generate_all_customers(config):
    """
    Generate customers for all types.
    :param config: Configuration dictionary containing customer generation settings
    :return: Dictionary with customers for each type
    """
    customers = {}
    # Generate customers for each type
    for customer_type in ['local', 'national', 'international']:
        customers[customer_type] = []
        for _ in range(config['msisdn'][customer_type]['count']):
            msisdn = generate_msisdn(customer_type, config)
            imei = generate_imei()
            imsi = generate_imsi()
            customers[customer_type].append({"msisdn": msisdn, "imei": imei, "imsi": imsi})

    return customers

# Main function to load config and generate customers
if __name__ == "__main__":
    # Load configuration from YAML
    with open("settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Generate customers
    customers = generate_all_customers(config)

    # Save customers to TinyDB
    save_customers_to_db(customers)
