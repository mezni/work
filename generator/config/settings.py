import random
from typing import List
from tinydb import TinyDB, Query

# Value Object for QoS (Quality of Service)
class QoS:
    def __init__(self, gbr: int, mbr: int):
        self.gbr = gbr  # Guaranteed Bit Rate in kbps
        self.mbr = mbr  # Maximum Bit Rate in kbps

    def __repr__(self):
        return f"QoS(GBR={self.gbr} kbps, MBR={self.mbr} kbps)"

    def to_dict(self):
        """Convert the QoS object to a dictionary for storage in TinyDB"""
        return {"GBR": self.gbr, "MBR": self.mbr}

# Entity for EPS Bearer
class Bearer:
    def __init__(self, bearer_id: int, bearer_type: str, qos: QoS):
        self.bearer_id = bearer_id
        self.bearer_type = bearer_type
        self.qos = qos

    def __repr__(self):
        return f"Bearer(ID={self.bearer_id}, Type={self.bearer_type}, QoS={self.qos})"

    def to_dict(self):
        """Convert the Bearer object to a dictionary for storage in TinyDB"""
        return {
            "Bearer_ID": self.bearer_id,
            "Bearer_Type": self.bearer_type,
            "QoS": self.qos.to_dict()
        }

    def apply_qos(self, qos: QoS):
        """Method to apply new QoS to a bearer."""
        self.qos = qos

# Aggregate for managing a collection of Bearers
class BearerAggregate:
    def __init__(self):
        self.bearers = []

    def add_bearer(self, bearer: Bearer):
        self.bearers.append(bearer)

    def get_all_bearers(self) -> List[Bearer]:
        return self.bearers

# Factory for creating Bearers
class BearerFactory:
    @staticmethod
    def generate_qos() -> QoS:
        """Generate random QoS values for a bearer."""
        gbr = random.randint(100, 1000)  # Guaranteed Bit Rate (GBR) in kbps
        mbr = random.randint(1000, 10000)  # Maximum Bit Rate (MBR) in kbps
        return QoS(gbr, mbr)

    @staticmethod
    def create_bearer(bearer_id: int, bearer_type: str) -> Bearer:
        """Create a new bearer with random QoS."""
        qos = BearerFactory.generate_qos()
        return Bearer(bearer_id, bearer_type, qos)

# Example of using the DDD style to generate bearers
def generate_bearers(num_bearers: int) -> List[Bearer]:
    bearer_aggregate = BearerAggregate()

    # Add default bearer (ID 5)
    default_bearer = BearerFactory.create_bearer(5, "Default")
    bearer_aggregate.add_bearer(default_bearer)

    # Add dedicated bearers (IDs 6 onwards)
    for i in range(6, 6 + num_bearers - 1):
        bearer_type = "Dedicated (VoLTE)" if i % 2 == 0 else "Dedicated (Video Streaming)"
        dedicated_bearer = BearerFactory.create_bearer(i, bearer_type)
        bearer_aggregate.add_bearer(dedicated_bearer)

    return bearer_aggregate.get_all_bearers()

# Save bearers to TinyDB
def save_bearers_to_tinydb(bearers: List[Bearer]):
    db = TinyDB('bearers_db.json')
    table = db.table('bearers')

    for bearer in bearers:
        # Insert each bearer as a new document in the table
        table.insert(bearer.to_dict())

    print(f"Saved {len(bearers)} bearers to TinyDB.")

# Example usage
num_bearers = 5  # Number of bearers to generate
generated_bearers = generate_bearers(num_bearers)

# Save to TinyDB
save_bearers_to_tinydb(generated_bearers)

# Optional: Retrieve and print the saved data from TinyDB
db = TinyDB('settings.json')
table = db.table('bearers')
for doc in table.all():
    print(doc)
