import random
import datetime
import json
from tinydb import TinyDB, Query

# Function to read MSISDNs from TinyDB
def read_msisdns(db_path="settings.json"):
    """
    Read MSISDNs from TinyDB (local, national, and international).
    :param db_path: Path to the TinyDB database file
    :return: Dictionary of MSISDN lists for local, national, and international types
    """
    try:
        # Initialize TinyDB
        db = TinyDB(db_path)

        # Read data from the local MSISDN table
        local_table = db.table('msisdn_local')
        local_msisdns = [entry['msisdn'] for entry in local_table.all()]

        # Read data from the national MSISDN table
        national_table = db.table('msisdn_national')
        national_msisdns = [entry['msisdn'] for entry in national_table.all()]

        # Read data from the international MSISDN table
        international_table = db.table('msisdn_international')
        international_msisdns = [entry['msisdn'] for entry in international_table.all()]

        return {
            'local': local_msisdns,
            'national': national_msisdns,
            'international': international_msisdns
        }

    except FileNotFoundError:
        print("Error: The settings.json file was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the MSISDNs: {e}")
        exit(1)

# Function to generate a random call duration in seconds
def generate_call_duration():
    """
    Generate a random call duration between 30 seconds and 3600 seconds (1 hour).
    :return: Call duration in seconds
    """
    return random.randint(30, 3600)

# Function to generate a random call start time within the last 24 hours
def generate_call_start_time():
    """
    Generate a random call start time within the last 24 hours.
    :return: Random datetime object representing the call start time
    """
    now = datetime.datetime.now()
    time_diff = random.randint(0, 86400)  # 86400 seconds in a day
    call_start_time = now - datetime.timedelta(seconds=time_diff)
    return call_start_time

# Function to generate an Ericsson CDR
def generate_ericsson_cdr(caller, recipient):
    """
    Generate a simulated Ericsson Call Detail Record (CDR).
    :param caller: Caller MSISDN
    :param recipient: Recipient MSISDN
    :return: A dictionary representing the CDR
    """
    # Generate call details
    call_start_time = generate_call_start_time()
    call_duration = generate_call_duration()

    # Simulate Ericsson CDR format
    cdr = {
        "caller": caller,
        "recipient": recipient,
        "call_start_time": call_start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "call_duration_seconds": call_duration,
        "call_end_time": (call_start_time + datetime.timedelta(seconds=call_duration)).strftime("%Y-%m-%d %H:%M:%S"),
        "call_type": "voice",  # Assuming it's a voice call, can be adjusted
        "cdr_type": "interconnect",  # Example of CDR type (you can adjust this based on requirements)
        "status": "completed",  # Status of the call, e.g., completed, missed, etc.
        "record_type": "origination"  # Assuming this is an origination record
    }
    return cdr

# Function to save generated CDRs to a file
def save_cdr_to_file(cdr, filename="cdrs.json"):
    try:
        with open(filename, "a") as file:
            json.dump(cdr, file)
            file.write("\n")  # Write each CDR on a new line
        print(f"CDR saved to {filename}")
    except Exception as e:
        print(f"Error saving CDR to file: {e}")

# Main function to display MSISDNs and generate CDRs
if __name__ == "__main__":
    # Read MSISDNs from the database
    msisdns = read_msisdns("settings.json")

    # Access each MSISDN type
    local_msisdns = msisdns['local']
    national_msisdns = msisdns['national']
    international_msisdns = msisdns['international']

    # Generate 100 CDRs
    for _ in range(100):
        # Randomly decide the type of call (with the specified probabilities)
        call_type = random.choices(
            ['local_to_local', 'local_to_national', 'national_to_local', 'local_to_international', 'international_to_local'],
            weights=[60, 35, 35, 5, 5],
            k=1
        )[0]

        # Determine caller and recipient based on the call type
        if call_type == 'local_to_local':
            caller = random.choice(local_msisdns)
            recipient = random.choice(local_msisdns)
        elif call_type == 'local_to_national':
            caller = random.choice(local_msisdns)
            recipient = random.choice(national_msisdns)
        elif call_type == 'national_to_local':
            caller = random.choice(national_msisdns)
            recipient = random.choice(local_msisdns)
        elif call_type == 'local_to_international':
            caller = random.choice(local_msisdns)
            recipient = random.choice(international_msisdns)
        elif call_type == 'international_to_local':
            caller = random.choice(international_msisdns)
            recipient = random.choice(local_msisdns)

        # Generate Ericsson CDR
        cdr = generate_ericsson_cdr(caller, recipient)

        # Output the generated CDR
        print("\nGenerated Ericsson CDR:")
        for key, value in cdr.items():
            print(f"{key}: {value}")

        # Save CDR to file
        save_cdr_to_file(cdr)
