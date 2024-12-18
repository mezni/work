class Customer:
    def __init__(self, customer_type: str, msisdn: str, imsi: str, imei: str):
        """
        Initializes a Customer entity with customer_type, MSISDN, IMSI, and IMEI.

        Args:
            customer_type (str): Type of customer (e.g., "regular", "premium").
            msisdn (str): The MSISDN as a string.
            imsi (str): The IMSI as a string.
            imei (str): The IMEI as a string.
        """
        self.customer_type = customer_type
        self.msisdn = msisdn  
        self.imsi = imsi  
        self.imei = imei 

    def __str__(self):
        return f"Customer(customer_type={self.customer_type}, msisdn={self.msisdn}, imsi={self.imsi}, imei={self.imei})"

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.msisdn == other.msisdn and self.imsi == other.imsi and self.imei == other.imei

    def __hash__(self):
        return hash((self.customer_type, self.msisdn, self.imsi, self.imei))
