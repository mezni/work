class QoS:
    def __init__(self, gbr: int, mbr: int):
        self.gbr = gbr
        self.mbr = mbr

    def __repr__(self):
        return f"QoS(GBR={self.gbr} kbps, MBR={self.mbr} kbps)"

    def to_dict(self):
        return {"GBR": self.gbr, "MBR": self.mbr}
