class Customer:
    def __init__(self, msisdn, imei, imsi):
        self.msisdn = msisdn
        self.imei = imei
        self.imsi = imsi

    def to_dict(self):
        return {
            "msisdn": self.msisdn,
            "imei": self.imei,
            "imsi": self.imsi
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["msisdn"], data["imei"], data["imsi"])
