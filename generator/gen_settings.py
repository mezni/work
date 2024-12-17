import random
import yaml
from tinydb import TinyDB

# Load configuration from YAML file
def load_config(file_path="config.yaml"):
    """
    Load configuration from the given YAML file.
    :param file_path: Path to the YAML file
    :return: Parsed configuration as a dictionary
    """
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file. Details: {e}")
        exit(1)

# Generate a random NDC from the given ranges
def generate_ndc(ndc_ranges):
    """
    Generate a random NDC (National Destination Code) from specified ranges.
    :param ndc_ranges: List of tuples specifying the NDC ranges
    :return: Random NDC as an integer
    """
    range_choice = random.choice(ndc_ranges)  # Pick a random range
    return random.randint(range_choice[0], range_choice[1])  # Generate NDC within the chosen range

# Generate a random MSISDN
def generate_msisdn(country_code, ndc_ranges):
    """
    Generate a random MSISDN (Mobile Station International Subscriber Directory Number).
    :param country_code: Country code (e.g., +216)
    :param ndc_ranges: List of NDC ranges
    :return: MSISDN as a string
    """
    ndc = generate_ndc(ndc_ranges)  # Get a valid NDC
    subscriber_number = random.randint(100000, 999999)  # Generate a 6-digit subscriber number
    msisdn = f"{country_code}{ndc}{subscriber_number}"  # Combine to form the MSISDN
    return msisdn

# Generate a random international MSISDN (with a prefix from PREFIXES)
def generate_international_msisdn(prefixes):
    """
    Generate a random international MSISDN with a prefix from the given list.
    :param prefixes: List of MSISDN prefixes (e.g., +21606, +3306)
    :return: MSISDN as a string
    """
    prefix = random.choice(prefixes)  # Pick a random prefix
    subscriber_number = random.randint(10000000, 99999999)  # Generate a 8-digit subscriber number
    msisdn = f"{prefix}{subscriber_number}"  # Combine to form the international MSISDN
    return msisdn

# Generate a list of MSISDNs (both local and international)
def generate_msisdns(country_code, ndc_ranges, prefixes, local_count, international_count):
    """
    Generate a list of MSISDNs.
    :param country_code: Country code (e.g., +216)
    :param ndc_ranges: List of NDC ranges
    :param prefixes: List of MSISDN prefixes for international MSISDNs
    :param local_count: Number of local MSISDNs to generate
    :param international_count: Number of international MSISDNs to generate
    :return: Tuple (list of local MSISDNs, list of international MSISDNs)
    """
    msisdns = [generate_msisdn(country_code, ndc_ranges) for _ in range(local_count)]  # Local MSISDNs
    international_msisdns = [generate_international_msisdn(prefixes) for _ in range(international_count)]  # International MSISDNs
    return msisdns, international_msisdns

# Save MSISDNs to separate TinyDB tables
def save_to_tinydb(msisdns, international_msisdns, db_path="settings.json"):
    """
    Save the MSISDNs to separate TinyDB tables.
    :param msisdns: List of local MSISDNs to save
    :param international_msisdns: List of international MSISDNs to save
    :param db_path: Path to the TinyDB database file
    """
    # Initialize TinyDB
    db = TinyDB(db_path)

    # Table for local MSISDNs
    msisdns_table = db.table('msisdns')
    for msisdn in msisdns:
        msisdns_table.insert({"msisdn": msisdn})

    # Table for international MSISDNs
    international_table = db.table('msisdns_international')
    for msisdn in international_msisdns:
        international_table.insert({"msisdn": msisdn})

    print(f"{len(msisdns)} local MSISDN(s) and {len(international_msisdns)} international MSISDN(s) saved to '{db_path}'")

# Main function
if __name__ == "__main__":
    # Load configuration from YAML
    config = load_config("config.yaml")

    # Extract values from the configuration
    country_code = config.get("COUNTRY_CODE")
    ndc_ranges = config.get("NDC_RANGES")
    prefixes = config.get("PREFIXES")
    
    # Use default values if not specified in the config
    local_count = config.get("LOCAL_COUNT", 1000)
    international_count = config.get("INTERNATIONAL_COUNT", 1000)

    # Validate the configuration
    if not isinstance(country_code, str) or not country_code.startswith("+"):
        print("Error: Invalid COUNTRY_CODE in config.yaml. It must be a string starting with '+'.")
        exit(1)

    if not isinstance(ndc_ranges, list) or not all(isinstance(r, list) and len(r) == 2 for r in ndc_ranges):
        print("Error: Invalid NDC_RANGES in config.yaml. It must be a list of [start, end] ranges.")
        exit(1)

    if not isinstance(prefixes, list) or not all(isinstance(p, str) for p in prefixes):
        print("Error: Invalid PREFIXES in config.yaml. It must be a list of strings.")
        exit(1)

    if not isinstance(local_count, int) or local_count <= 0:
        print("Error: Invalid LOCAL_COUNT value in config.yaml. It must be a positive integer.")
        exit(1)

    if not isinstance(international_count, int) or international_count <= 0:
        print("Error: Invalid INTERNATIONAL_COUNT value in config.yaml. It must be a positive integer.")
        exit(1)

    # Generate both local and international MSISDNs
    msisdns, international_msisdns = generate_msisdns(country_code, ndc_ranges, prefixes, local_count, international_count)

    # Save MSISDNs to TinyDB
    save_to_tinydb(msisdns, international_msisdns)
