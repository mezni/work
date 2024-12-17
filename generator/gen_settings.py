import random
import yaml
from tinydb import TinyDB

# Function to read MSISDNs from TinyDB
def save_msisdns_to_db(msisdns, db_path="settings.json"):
    """
    Save MSISDNs to separate TinyDB tables for local, national, and international MSISDNs.
    :param msisdns: Dictionary of MSISDN lists for different types (local, national, international)
    :param db_path: Path to the TinyDB database file
    """
    # Initialize TinyDB
    db = TinyDB(db_path)

    # Insert MSISDNs into the respective tables
    for msisdn_type, msisdn_list in msisdns.items():
        table = db.table(f"msisdn_{msisdn_type}")
        for msisdn in msisdn_list:
            table.insert({"msisdn": msisdn})

    print(f"{sum(len(msisdn_list) for msisdn_list in msisdns.values())} MSISDN(s) saved to '{db_path}'")

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

# Function to generate MSISDNs for all types (local, national, international)
def generate_all_msisdns(config):
    """
    Generate MSISDNs for all types and save them in separate lists.
    :param config: Configuration dictionary containing MSISDN generation settings
    :return: Dictionary with MSISDNs for each type
    """
    msisdns = {}

    # Generate MSISDNs for each type
    for msisdn_type in ['local', 'national', 'international']:
        msisdns[msisdn_type] = [generate_msisdn(msisdn_type, config) for _ in range(config['msisdn'][msisdn_type]['count'])]

    return msisdns

# Main function to load config and generate MSISDNs
if __name__ == "__main__":
    # Load configuration from YAML
    with open("settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Generate MSISDNs
    msisdns = generate_all_msisdns(config)

    # Save MSISDNs to TinyDB
    save_msisdns_to_db(msisdns)
