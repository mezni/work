import random
from tinydb import TinyDB
from typing import Dict, List, Any


# --- Configuration as a Python Dictionary ---
CONFIG = {
    "msisdn": {
        "local": {
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


# --- Value Objects ---
class IMEI:
    @staticmethod
    def generate() -> str:
        imei = [str(random.randint(0, 9)) for _ in range(14)]
        sum_digits, alternate = 0, 0
        for i in range(14):
            digit = int(imei[i])
            if alternate:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum_digits += digit
            alternate = 1 - alternate
        check_digit = (10 - (sum_digits % 10)) % 10
        imei.append(str(check_digit))
        return ''.join(imei)


class IMSI:
    @staticmethod
    def generate() -> str:
        mcc = str(random.randint(100, 999))  # Mobile Country Code
        mnc = str(random.randint(0, 999))   # Mobile Network Code
        msin = str(random.randint(0, 999999999))  # Mobile Subscriber ID
        return f"{mcc}{mnc}{msin}"


class MSISDN:
    @staticmethod
    def generate(customer_type: str, config: Dict[str, Any]) -> str:
        """
        Generate an MSISDN based on type (local, national, international)
        """
        msisdn_config = config['msisdn'][customer_type]
        digits = msisdn_config['digits']

        if customer_type in ["local", "national"]:
            country_code = msisdn_config["country_code"]
            ndc_range = random.choice(msisdn_config.get("ndc_ranges", []))
            ndc = random.randint(ndc_range[0], ndc_range[1])
            subscriber_number = random.randint(10**(digits-1), 10**digits - 1)
            return f"{country_code}{ndc}{subscriber_number}"

        elif customer_type == "international":
            prefix = random.choice(msisdn_config.get("prefixes", []))
            subscriber_number = random.randint(10**(digits-1), 10**digits - 1)
            return f"{prefix}{subscriber_number}"


# --- Entity ---
class Customer:
    def __init__(self, msisdn: str, imei: str, imsi: str):
        self.msisdn = msisdn
        self.imei = imei
        self.imsi = imsi

    def to_dict(self) -> Dict[str, str]:
        return {"msisdn": self.msisdn, "imei": self.imei, "imsi": self.imsi}


# --- Repository ---
class CustomerRepository:
    def __init__(self, db_path: str = "settings.json"):
        self.db = TinyDB(db_path)

    def save_customers(self, customers: Dict[str, List[Customer]]):
        """
        Save customers to the database under specific tables.
        """
        for customer_type, customer_list in customers.items():
            table_name = {
                "local": "customer_home",
                "national": "customer_national",
                "international": "customer_international",
            }.get(customer_type, "customer_other")

            table = self.db.table(table_name)
            for customer in customer_list:
                table.insert(customer.to_dict())

        print(f"Saved {sum(len(c) for c in customers.values())} customers to database '{self.db._storage.path}'")


# --- Service ---
class CustomerGeneratorService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_customers(self) -> Dict[str, List[Customer]]:
        """
        Generate customers for all types based on the configuration.
        """
        customers = {"local": [], "national": [], "international": []}
        for customer_type in customers.keys():
            count = self.config['msisdn'][customer_type]['count']
            for _ in range(count):
                msisdn = MSISDN.generate(customer_type, self.config)
                imei = IMEI.generate()
                imsi = IMSI.generate()
                customers[customer_type].append(Customer(msisdn, imei, imsi))
        return customers


# --- Application Logic ---
if __name__ == "__main__":
    # Initialize services
    generator_service = CustomerGeneratorService(CONFIG)
    repository = CustomerRepository(db_path="settings.json")

    # Generate customers
    customers = generator_service.generate_customers()

    # Save to database
    repository.save_customers(customers)
