import json
import random
from typing import List
from random import randint
from value_objects import MSISDN, IMSI, IMEI
from entities import Customer
from factories import MSISDNFactory, IMSIFactory, IMEIFactory
from interfaces import CustomerRepository

class CustomerService:
    def __init__(self, config: dict, repository: CustomerRepository):
        self.config = config
        self.repository = repository

    def generate_msisdn(self, msisdn_type: str) -> str:
        """Generates an MSISDN based on the type (home, national, or international)."""
        msisdn_config = self.config['msisdn'][msisdn_type]

        if msisdn_type == "home" or msisdn_type == "national":
            country_code = msisdn_config['country_code']
            ndc_range = msisdn_config['ndc_ranges']
            digits = msisdn_config['digits']
            count = msisdn_config['count']
            msisdns = []

            for _ in range(count):
                ndc = random.choice(ndc_range)  # Randomly select a NDC range
                msisdns.append(str(MSISDNFactory.generate(msisdn_type, country_code, ndc, digits=digits)))

            return msisdns

        elif msisdn_type == "international":
            prefix = msisdn_config['prefixes']
            digits = msisdn_config['digits']
            count = msisdn_config['count']
            msisdns = []

            for _ in range(count):
                msisdns.append(str(MSISDNFactory.generate(msisdn_type, prefix=prefix, digits=digits)))

            return msisdns

        else:
            raise ValueError(f"Invalid MSISDN type: {msisdn_type}")

    def generate_customers(self) -> List[Customer]:
        """Generates customers based on the config and returns a list of Customer objects."""
        customers = []

        for msisdn_type in self.config['msisdn']:
            msisdns = self.generate_msisdn(msisdn_type)

            for msisdn in msisdns:
                customer = Customer(
                    customer_type=msisdn_type,
                    msisdn=msisdn,
                    imsi=str(IMSI(IMSIFactory.generate())),
                    imei=str(IMEI(IMEIFactory.generate()))
                )
                customers.append(customer)

        return customers

    def save_customers(self):
        """Generates and saves customers to the repository."""
        customers = self.generate_customers()
        for customer in customers:
            print (customer)
            self.repository.add(customer)
