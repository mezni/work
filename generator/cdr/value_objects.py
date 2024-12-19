class MSISDN:
    def __init__(self, msisdn: str):
        if not self._validate(msisdn):
            raise ValueError(f"Invalid MSISDN: {msisdn}")
        self.msisdn = msisdn

    def _validate(self, msisdn: str) -> bool:
        """Validate the MSISDN format (should be numeric and 6-15 digits)."""
        if not msisdn.isdigit():
            raise ValueError(f"MSISDN should only contain numeric characters, got: {msisdn}")
        return 6 <= len(msisdn) <= 15

    def __str__(self):
        return self.msisdn

    def __repr__(self):
        return f"MSISDN({self.msisdn!r})"


class IMSI:
    def __init__(self, imsi: str):
        if not self._validate(imsi):
            raise ValueError(f"Invalid IMSI: {imsi}")
        self.imsi = imsi

    def _validate(self, imsi: str) -> bool:
        """Validate IMSI format (should be numeric and 15-16 digits)."""
        if not imsi.isdigit():
            raise ValueError(f"IMSI should only contain numeric characters, got: {imsi}")
        return 15 <= len(imsi) <= 16

    def __str__(self):
        return self.imsi

    def __repr__(self):
        return f"IMSI({self.imsi!r})"


class IMEI:
    def __init__(self, imei: str):
        if not self._validate(imei):
            raise ValueError(f"Invalid IMEI: {imei}")
        self.imei = imei

    def _validate(self, imei: str) -> bool:
        """Validate the IMEI format (should be numeric and 15 digits)."""
        if not imei.isdigit():
            raise ValueError(f"IMEI should only contain numeric characters, got: {imei}")
        return len(imei) == 15

    def __str__(self):
        return self.imei

    def __repr__(self):
        return f"IMEI({self.imei!r})"

class QoS:
    def __init__(self, gbr: int, mbr: int):
        if not self._validate(gbr, mbr):
            raise ValueError(f"Invalid QoS values: GBR={gbr}, MBR={mbr}")
        self.gbr = gbr  # Guaranteed Bit Rate in kbps
        self.mbr = mbr  # Maximum Bit Rate in kbps

    def _validate(self, gbr: int, mbr: int) -> bool:
        if gbr <= 0 or mbr <= 0:
            raise ValueError(f"GBR and MBR must be greater than 0. Given: GBR={gbr}, MBR={mbr}")
        return True

    def __repr__(self):
        return f"QoS(GBR={self.gbr} kbps, MBR={self.mbr} kbps)"

    def to_dict(self):
        return {"gbr": self.gbr, "mbr": self.mbr}
