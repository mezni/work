class MSISDN:
    def __init__(self, number: str):
        if not isinstance(number, str):
            raise TypeError("MSISDN must be a string.")
        self.number = number

    def __str__(self):
        return self.number

    def __eq__(self, other):
        if not isinstance(other, MSISDN):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def to_dict(self):
        return {"number": self.number}

class IMEI:
    def __init__(self, number: str):
        if not isinstance(number, str):
            raise TypeError("IMEI must be a string.")
        self.number = number

    def __str__(self):
        return self.number

    def __eq__(self, other):
        if not isinstance(other, IMEI):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def to_dict(self):
        return {"number": self.number}

class IMSI:
    def __init__(self, number: str):
        if not isinstance(number, str):
            raise TypeError("IMSI must be a string.")
        self.number = number

    def __str__(self):
        return self.number

    def __eq__(self, other):
        if not isinstance(other, IMSI):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def to_dict(self):
        return {"number": self.number}