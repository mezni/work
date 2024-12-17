import random
from entities.customer import Customer
from config import CONFIG

class CustomerService:
    @staticmethod
    def generate_imei():
        imei = [str(random.randint(0, 9)) for _ in range(14)]
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
        imei.append(str(check_digit))
        return ''.join(imei)

    @staticmethod
    def generate_imsi():
        mcc = str(random.randint(100, 999))
        mnc = str(random.randint(0, 999))
        msin = str(random.randint(0, 999999999))
        return f"{mcc}{mnc}{msin}"

    @staticmethod
    def generate_msisdn(msisdn_type):
        msisdn_config = CONFIG['msisdn'][msisdn_type]
        if msisdn_type == "local" or msisdn_type == "national":
            country_code = msisdn_config["country_code"]
            ndc_range = random.choice(msisdn_config["ndc_ranges"])
            ndc = random.randint(ndc_range[0], ndc_range[1])
            subscriber_number = random.randint(10**(msisdn_config["digits"]-1), 10**msisdn_config["digits"] - 1)
            return f"{country_code}{ndc}{subscriber_number}"

        elif msisdn_type == "international":
            prefix = random.choice(msisdn_config["prefixes"])
            subscriber_number = random.randint(10**(msisdn_config["digits"]-1), 10**msisdn_config["digits"] - 1)
            return f"{prefix}{subscriber_number}"

    def generate_customer(self, customer_type):
        msisdn = self.generate_msisdn(customer_type)
        imei = self.generate_imei()
        imsi = self.generate_imsi()
        return Customer(msisdn, imei, imsi)
    
    def generate_all_customers(self):
        customers = {}
        for customer_type in ['local', 'national', 'international']:
            customers[customer_type] = []
            for _ in range(CONFIG['msisdn'][customer_type]['count']):
                customer = self.generate_customer(customer_type)
                customers[customer_type].append(customer)
        return customers
