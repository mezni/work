class Customer:
    def __init__(self, msisdn: MSISDN, imsi: IMSI, imei: IMEI):
        """
        Initializes a Customer entity with MSISDN, IMSI, and IMEI.

        Args:
            msisdn (MSISDN): The MSISDN value object.
            imsi (IMSI): The IMSI value object.
            imei (IMEI): The IMEI value object.
        """
        if not isinstance(msisdn, MSISDN):
            raise TypeError("Expected MSISDN value object.")
        if not isinstance(imsi, IMSI):
            raise TypeError("Expected IMSI value object.")
        if not isinstance(imei, IMEI):
            raise TypeError("Expected IMEI value object.")

        self.msisdn = msisdn
        self.imsi = imsi
        self.imei = imei

    def __str__(self):
        return f"Customer(msisdn={self.msisdn}, imsi={self.imsi}, imei={self.imei})"

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.msisdn == other.msisdn and self.imsi == other.imsi and self.imei == other.imei

    def __hash__(self):
        return hash((self.msisdn, self.imsi, self.imei))
