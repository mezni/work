import random
from tinydb import TinyDB

# Function to generate a random MSISDN (10-digit number)
def generate_msisdn():
    # Example: a USA country code prefix (this can be modified for other countries)
    prefix = "1"
    msisdn = prefix + ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return msisdn

# Initialize the TinyDB database
db = TinyDB('db.json')

# Number of MSISDNs to generate
num_msisdn = 10  # Change this value to generate more or fewer MSISDNs

# Generate a list of MSISDNs
msisdn_list = [generate_msisdn() for _ in range(num_msisdn)]

# Save the MSISDNs to the TinyDB database
for msisdn in msisdn_list:
    db.insert({'msisdn': msisdn})

# Display the generated MSISDNs
print(f"Generated MSISDN List: {msisdn_list}")
