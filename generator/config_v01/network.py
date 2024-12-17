import random
from typing import Dict, Optional
from tinydb import TinyDB


# Utility function to remove keys with None values
def clean_dict(data: Dict):
    return {key: value for key, value in data.items() if value is not None}


class Address:
    def __init__(self, ip: str):
        self.ip = ip

    def to_dict(self):
        return self.ip


class NetworkIdentifier:
    def __init__(self, mcc: str, mnc: str):
        self.mcc = mcc
        self.mnc = mnc

    def to_dict(self):
        return clean_dict({"MCC": self.mcc, "MNC": self.mnc})


class Node:
    def __init__(
        self,
        rnc_id: Optional[int] = None,
        lac: Optional[int] = None,
        cell_id: Optional[int] = None,
        tac: Optional[int] = None,
        gnb_id: Optional[int] = None,
        nr_cell_id: Optional[int] = None,
        pdu_session_id: Optional[int] = None,
    ):
        self.rnc_id = rnc_id
        self.lac = lac
        self.cell_id = cell_id
        self.tac = tac
        self.gnb_id = gnb_id
        self.nr_cell_id = nr_cell_id
        self.pdu_session_id = pdu_session_id

    def to_dict(self):
        return clean_dict({
            "RNC_ID": self.rnc_id,
            "LAC": self.lac,
            "Cell_ID": self.cell_id,
            "TAC": self.tac,
            "gNB_ID": self.gnb_id,
            "NR_Cell_ID": self.nr_cell_id,
            "PDU_Session_ID": self.pdu_session_id,
        })


class NetworkComponent:
    def __init__(self, identifier: NetworkIdentifier, node: Node, addresses: Dict[str, Address]):
        self.identifier = identifier
        self.node = node
        self.addresses = addresses

    def to_dict(self):
        return clean_dict({
            "Identifier": self.identifier.to_dict(),
            "Node": self.node.to_dict(),
            "Addresses": clean_dict({key: address.to_dict() for key, address in self.addresses.items()})
        })


def generate_3g_components(mcc: str, mnc: str, num_entries: int):
    components = []
    for _ in range(num_entries):
        identifier = NetworkIdentifier(mcc, mnc)
        node = Node(
            rnc_id=random.randint(1, 65535),
            lac=random.randint(1, 65535),
            cell_id=random.randint(1, 65535),
        )
        addresses = {
            "MSC_Address": Address(f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "SGSN_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "GGSN_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
        }
        components.append(NetworkComponent(identifier, node, addresses))
    return components


def generate_4g_components(mcc: str, mnc: str, num_entries: int):
    components = []
    for _ in range(num_entries):
        identifier = NetworkIdentifier(mcc, mnc)
        node = Node(
            tac=random.randint(1, 65535),
        )
        addresses = {
            "SGW_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "PGW_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "MME_Address": Address(f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"),
        }
        components.append(NetworkComponent(identifier, node, addresses))
    return components


def generate_5g_components(mcc: str, mnc: str, num_entries: int):
    components = []
    for _ in range(num_entries):
        identifier = NetworkIdentifier(mcc, mnc)
        node = Node(
            gnb_id=random.randint(1, 65535),
            nr_cell_id=random.randint(1, 65535),
            tac=random.randint(1, 65535),
            pdu_session_id=random.randint(1, 255),
        )
        addresses = {
            "AMF_Address": Address(f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "SMF_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
            "UPF_Address": Address(f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"),
        }
        components.append(NetworkComponent(identifier, node, addresses))
    return components


def generate_json(components):
    return [component.to_dict() for component in components]


def save_to_tinydb(database_name: str, table_name: str, data: list):
    db = TinyDB(database_name)
    table = db.table(table_name)
    table.insert_multiple(data)
    print(f"Saved {len(data)} entries to {database_name} in table '{table_name}'.")


# Example Usage
if __name__ == "__main__":
    mcc = "605"  
    mnc = "01" 
    num_entries = 20
    db_name = "settings.json"
    table_name = "network"

    # Generate 3G Components
    components_3g = generate_3g_components(mcc, mnc, num_entries)
    json_3g = generate_json(components_3g)
    save_to_tinydb(db_name, table_name, json_3g)

    # Generate 4G Components
    components_4g = generate_4g_components(mcc, mnc, num_entries)
    json_4g = generate_json(components_4g)
    save_to_tinydb(db_name, table_name, json_4g)

    # Generate 5G Components
    components_5g = generate_5g_components(mcc, mnc, num_entries)
    json_5g = generate_json(components_5g)
    save_to_tinydb(db_name, table_name, json_5g)
